import os, secrets, hashlib, hmac, smtplib
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText
from fastapi import FastAPI
from fastapi import Response, Request, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from numpy import var
import ollama
import subprocess
import tempfile
import os
import pymysql
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import requests as http_requests
from dotenv import load_dotenv
import jwt
from fastapi.responses import FileResponse
import random
import os
import uuid
from fastapi import File, Form, UploadFile
import json
import base64
import fitz  # PyMuPDF
import re
import time
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

class ProfileIn(BaseModel):
    user_id: int
    id_student: str
    name: str
    surname: str

class TermIn(BaseModel):
    semester: int      # 1 หรือ 2
    year: int          # เช่น 2569
    day_sob: str       # "2026-08-27" (YYYY-MM-DD)
    start_time: str    # "13:00"
    end_time: str      # "16:00"


app = FastAPI()
load_dotenv()

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")

JWT_SECRET = os.environ.get("JWT_SECRET", "") 
app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

messages = []

@app.post("/chat")
async def chat(data: dict):
        question = data.get("message", "")
        messages.append({"role": "user", "content": question})

        def generate():
            full_response = ""
            stream = ollama.chat(
                model="gemma3:4b",
                messages=messages,
                stream=True
            )
            for chunk in stream:
                token = chunk["message"]["content"]
                full_response += token
                yield token

            messages.append({"role": "assistant", "content": full_response})

        return StreamingResponse(generate(), media_type="text/plain")


  
    # ---------------------------------------------------------
    # 1. เส้น API สำหรับ Compile อย่างเดียว (รวดเร็ว ไม่รอ AI)
    # ---------------------------------------------------------
@app.post("/compile")
async def compile_cpp(data: dict):
        code = data.get("code", "")

        try:
            with tempfile.TemporaryDirectory() as tmp:
                cpp_file = os.path.join(tmp, "main.cpp")
                exe_file = os.path.join(tmp, "main.exe")

                with open(cpp_file, "w", encoding="utf8") as f:
                    f.write(code)

                # 1. รัน g++ คอมไพล์โค้ด
                compile_result = subprocess.run(
                    ["g++", cpp_file, "-o", exe_file],
                    capture_output=True,
                    text=True
                )

                # 2. ถ้าเจอ Compile Error (คอมไพล์ไม่ผ่าน)
                if compile_result.returncode != 0:
                    raw_error = compile_result.stderr
                    return {
                        "success": False,
                        "error": raw_error,        # ส่ง Error ดิบๆ กลับไปให้ Flutter เก็บไว้
                        "output": ""
                    }

                # 3. ถ้าคอมไพล์ผ่าน -> สั่งรันไฟล์ .exe
                try:
                    run_result = subprocess.run(
                        [exe_file],
                        capture_output=True,
                        text=True,
                        timeout=5  # กันโค้ดติด Infinite Loop
                    )

                    return {
                        "success": True,
                        "output": run_result.stdout, 
                        "error": run_result.stderr,  # กรณีเกิด Runtime Error
                    }

                except subprocess.TimeoutExpired:
                    return {
                        "success": False,
                        "error": "Time Limit Exceeded: โปรแกรมใช้เวลานานเกินไป อาจมี Infinite Loop",
                        "output": ""
                    }

        except Exception as e:
            return {
                "success": False,
                "error": f"Server Exception: {str(e)}",
                "output": ""
            }

    # ---------------------------------------------------------
    # 2. เส้น API สำหรับให้ AI วิเคราะห์ Error (เรียกใช้เมื่อกดปุ่ม)
    # ---------------------------------------------------------
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODELS = [
    m.strip().replace("models/", "")
    for m in os.environ.get(
        "GEMINI_MODELS",
        "gemini-3.8-flash,gemini-3.6-flash,gemini-3.5-flash-lite",
    ).split(",")
    if m.strip()
]


def call_gemini(prompt: str):
    """ลองทีละรุ่นตามลำดับ คืน (ข้อความ, ข้อความ error ล่าสุด)"""
    last_err = ""
    for model in GEMINI_MODELS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        body = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.2},
        }
        try:
            r = http_requests.post(
                url,
                headers={"x-goog-api-key": GEMINI_API_KEY},
                json=body,
                timeout=10,
            )
        except Exception as e:
            last_err = f"{model}: {type(e).__name__}"
            print("Gemini error:", last_err)
            continue

        if r.status_code == 200:
            try:
                parts = r.json()["candidates"][0]["content"]["parts"]
                text = "".join(p.get("text", "") for p in parts).strip()
            except (KeyError, IndexError, TypeError):
                text = ""
            if text:
                print(f"Gemini OK: {model} ใช้เวลา {r.elapsed.total_seconds():.1f} วินาที")
                return text, ""
            last_err = f"{model}: ตอบกลับว่าง"
            print("Gemini error:", last_err)
            continue

        last_err = f"{model}: HTTP {r.status_code}"
        print("Gemini error:", last_err, r.text[:200])
        if r.status_code in (400, 401, 403):
            break  # คีย์/สิทธิ์ผิด ลองรุ่นอื่นก็ไม่ช่วย
    return "", last_err


@app.post("/useai")
def use_ai(data: dict):
    raw_error = data.get("error", "")
    code = data.get("code", "")

    if not raw_error:
        return {"success": False, "ai_explanation": "ไม่พบข้อความ Error สำหรับวิเคราะห์"}
    if not GEMINI_API_KEY:
        return {"success": False, "ai_explanation": "ยังไม่ได้ตั้ง GEMINI_API_KEY ใน .env"}

    prompt = (
        "คุณเป็นติวเตอร์ภาษา C ที่ใจดี สอนนักเรียนมือใหม่ที่เพิ่งเริ่มเรียนเขียนโปรแกรม\n"
        "ตอบเป็นภาษาไทย ใช้คำง่ายๆ ไม่ใช้ศัพท์ยากโดยไม่อธิบาย "
        "ถ้าต้องใช้ศัพท์เทคนิค ให้ใส่คำอธิบายสั้นๆ ในวงเล็บ\n"
        "ตอบตามหัวข้อนี้ ไม่เกิน 6 บรรทัดรวม:\n"
        "1) ปัญหาคืออะไร (อธิบายด้วยภาษาคนทั่วไป 1-2 ประโยค)\n"
        "2) เกิดที่บรรทัดไหน หรือตรงส่วนไหนของโค้ด\n"
        "3) วิธีแก้ (บอกแนวทาง และยกตัวอย่างบรรทัดที่แก้แล้วได้ "
        "แต่ไม่ต้องเขียนโปรแกรมทั้งหมดให้)\n\n"
        f"ข้อความ Error จากคอมไพเลอร์:\n{raw_error}"
    )
    if code:
        prompt += f"\n\nโค้ดของนักเรียน:\n{code}"

    text, err = call_gemini(prompt)
    if text:
        return {"success": True, "ai_explanation": text}
    return {
        "success": False,
        "ai_explanation": "AI ไม่ว่างในขณะนี้ กรุณาลองใหม่อีกครั้งในอีกสักครู่",
    }





        #Database connection
        # ... (โค้ด app, CORS, และ API ของ Ollama / Compiler เดิมของคุณ) ...

    # ตั้งค่าการเชื่อมต่อ Database XAMPP
DB_CONFIG = {
        'host': 'localhost',
        'user': 'root',
        'password': '', # รหัสผ่าน XAMPP ปกติจะว่างเปล่า
        'database': 'testailearn', # 🔴 เปลี่ยนเป็นชื่อ Database ของคุณใน XAMPP
        'cursorclass': pymysql.cursors.DictCursor # สำคัญ! ตัวนี้ทำให้ผลลัพธ์ออกมาเป็น JSON (Dict) ทันที
    }

@app.get("/get_progress")
def get_progress():
        try:
            # 1. เชื่อมต่อฐานข้อมูล
            connection = pymysql.connect(**DB_CONFIG)
            
            with connection.cursor() as cursor:
                # 2. เขียนคำสั่ง SQL ดึงข้อมูลจากตารางของคุณ
                # 🔴 เปลี่ยน 'course_progress' เป็นชื่อตารางจริงของคุณ
                sql = "SELECT * FROM chapterlearn" 
                cursor.execute(sql)
                
                # 3. ดึงข้อมูลทั้งหมด
                result = cursor.fetchall()
                
            connection.close()

            # 4. ส่งกลับเป็น JSON 
            return {
                
                "data": result  # FastAPI จะแปลงก้อนนี้เป็น JSON Array ให้อัตโนมัติ
            }


        except Exception as e:
            return {
                "success": False, 
                "error": f"Database Error: {str(e)}"
            }

@app.get("/getlab/{lab_id}")
def get_lab(lab_id: str):
        try:
            # 1. เชื่อมต่อฐานข้อมูล
            connection = pymysql.connect(**DB_CONFIG)
            
            with connection.cursor() as cursor:
                # 2. เขียนคำสั่ง SQL ดึงข้อมูลจากตารางของคุณ
                # 🔴 เปลี่ยน 'course_progress' เป็นชื่อตารางจริงของคุณ
                sql = "SELECT * FROM lab WHERE lab_ofchapter = %s"
                cursor.execute(sql, (lab_id,))
                
                # 3. ดึงข้อมูลทั้งหมด
                result = cursor.fetchall()
                
            connection.close()

            # 4. ส่งกลับเป็น JSON 
            return {
                
                "data": result  # FastAPI จะแปลงก้อนนี้เป็น JSON Array ให้อัตโนมัติ
            }

        except Exception as e:
            return {
                "success": False, 
                "error": f"Database Error: {str(e)}"
            }
        
OTP_TTL = 120          # วินาที
RESEND_COOLDOWN = 60   # วินาที
MAX_ATTEMPTS = 5

SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_APP_PASSWORD = os.environ.get("SMTP_APP_PASSWORD", "")

def generate_code() -> str:
    return f"{secrets.randbelow(10000):04d}"

def hash_code(pending_token: str, code: str) -> str:
    return hashlib.sha256(f"{pending_token}:{code}".encode()).hexdigest()

def mask_email(email: str) -> str:
    local, domain = email.split("@", 1)
    return f"{local[0]}***@{domain}"

DEV_MODE = False

def send_otp_email(to_email: str, code: str):
    if DEV_MODE:
        print(f"[DEV] OTP for {to_email}: {code}")
        return
    msg = MIMEText(
        f"รหัสยืนยัน CodeLearn ของคุณคือ {code}\nรหัสนี้หมดอายุใน 2 นาที",
        "plain", "utf-8",
    )
    msg["Subject"] = "CodeLearn verification code"
    msg["From"] = SMTP_USER
    msg["To"] = to_email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=15) as s:
            s.starttls()
            s.login(SMTP_USER, SMTP_APP_PASSWORD)
            s.send_message(msg)
    except Exception as e:
        print("send_otp_email failed:", e)

GOOGLE_CLIENT_ID = "881235919126-ujqt791nd9jffe38udomnbbbg6ocgho3.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")
@app.post("/auth/google/code")
def google_login_code(data: dict):
    code = data.get("code", "")
    if not code:
        return {"success": False, "error": "ไม่พบ code"}

    try:
        # 1. แลก code เป็น token กับ Google
        token_res = http_requests.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uri": "postmessage",
                "grant_type": "authorization_code",
            },
            timeout=10,
        )
        token_json = token_res.json()
        if "id_token" not in token_json:
            return {"success": False, "error": f"แลก code ไม่สำเร็จ: {token_json}"}

        # 2. ตรวจ ID Token
        idinfo = id_token.verify_oauth2_token(
            token_json["id_token"],
            google_requests.Request(),
            GOOGLE_CLIENT_ID,
        )
        if not idinfo.get("email_verified"):
            return {"success": False, "error": "อีเมลยังไม่ได้รับการยืนยัน"}

        google_id = idinfo["sub"]
        email = idinfo["email"]
        name = idinfo.get("name", "")
        picture = idinfo.get("picture", "")

    except Exception as e:
        return {"success": False, "error": f"Google Error: {str(e)}"}

    try:
        # 3. บันทึกผู้ใช้
        connection = pymysql.connect(**DB_CONFIG)
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO users (google_id, email, name, picture)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE name = VALUES(name), picture = VALUES(picture)
                """,
                (google_id, email, name, picture),
            )
            cursor.execute("SELECT user_id FROM users WHERE google_id = %s", (google_id,))
            user_id = cursor.fetchone()["user_id"]

            # 4. สร้าง OTP แล้วเก็บแบบแฮช
            pending_token = secrets.token_urlsafe(32)[:64]
            code_plain = generate_code()
            now = datetime.now()
            cursor.execute(
                """
                INSERT INTO otp_codes
                    (pending_token, user_id, code_hash, expires_at, last_sent_at)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (pending_token, user_id, hash_code(pending_token, code_plain),
                 now + timedelta(seconds=OTP_TTL), now),
            )
            connection.commit()
        connection.close()

        # 5. ส่งเมลไปที่อีเมลที่ Google ยืนยันแล้วเท่านั้น
        send_otp_email(email, code_plain)

        return {
            "success": True,
            "pending": True,
            "pending_token": pending_token,
            "email_masked": mask_email(email),
            "expires_in": OTP_TTL,
        }

    except Exception as e:
        return {"success": False, "error": f"OTP Error: {str(e)}"}

@app.post("/auth/otp/verify")
def otp_verify(data: dict, response: Response):
    token = data.get("pending_token", "")
    code = str(data.get("code", ""))
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as c:
            c.execute("SELECT * FROM otp_codes WHERE pending_token = %s", (token,))
            row = c.fetchone()
            if not row:
                return {"success": False, "error": "คำขอไม่ถูกต้อง กรุณาล็อกอินใหม่"}

            if datetime.now() > row["expires_at"]:
                c.execute("DELETE FROM otp_codes WHERE id = %s", (row["id"],))
                conn.commit()
                return {"success": False, "error": "รหัสหมดอายุ"}

            if row["attempts"] >= MAX_ATTEMPTS:
                c.execute("DELETE FROM otp_codes WHERE id = %s", (row["id"],))
                conn.commit()
                return {"success": False, "error": "กรอกผิดเกินกำหนด กรุณาล็อกอินใหม่"}

            if not hmac.compare_digest(row["code_hash"], hash_code(token, code)):
                c.execute("UPDATE otp_codes SET attempts = attempts + 1 WHERE id = %s", (row["id"],))
                conn.commit()
                return {"success": False, "error": "รหัสไม่ถูกต้อง"}

            c.execute("SELECT * FROM users WHERE user_id = %s", (row["user_id"],))
            user = c.fetchone()
            c.execute("DELETE FROM otp_codes WHERE id = %s", (row["id"],))
            conn.commit()

        if not user:
            return {"success": False, "error": "ไม่พบผู้ใช้ กรุณาล็อกอินใหม่"}

        # ตาราง users ใช้ user_id เป็นคีย์หลัก
        uid = user["user_id"]
        user["id"] = uid  # ใส่ id เพิ่มให้หน้าเว็บที่อ่าน user.id ยังใช้ได้

        if not JWT_SECRET:
            return {"success": False, "error": "เซิร์ฟเวอร์ยังไม่ได้ตั้ง JWT_SECRET"}
        jwt_token = jwt.encode(
            {
                "user_id": uid,
                "exp": datetime.now(timezone.utc) + timedelta(days=7),
            },
            JWT_SECRET,
            algorithm="HS256",
        )
        response.set_cookie(
            key="token",
            value=jwt_token,
            httponly=True,
            samesite="lax",
            max_age=7 * 24 * 3600,
        )
        return {"success": True, "user": user}
    finally:
        conn.close()


@app.post("/auth/otp/resend")
def otp_resend(data: dict):
    token = data.get("pending_token", "")
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as c:
            c.execute(
                """SELECT o.*, u.email FROM otp_codes o
                   JOIN users u ON u.user_id = o.user_id
                   WHERE o.pending_token = %s""",
                (token,),
            )
            row = c.fetchone()
            if not row:
                return {"success": False, "error": "คำขอไม่ถูกต้อง กรุณาล็อกอินใหม่"}

            now = datetime.now()
            if (now - row["last_sent_at"]).total_seconds() < RESEND_COOLDOWN:
                return {"success": False, "error": "ขอรหัสใหม่บ่อยเกินไป"}

            code_plain = generate_code()
            c.execute(
                """UPDATE otp_codes
                   SET code_hash = %s, expires_at = %s, last_sent_at = %s, attempts = 0
                   WHERE id = %s""",
                (hash_code(token, code_plain), now + timedelta(seconds=OTP_TTL), now, row["id"]),
            )
            conn.commit()
        send_otp_email(row["email"], code_plain)
        return {"success": True, "expires_in": OTP_TTL}
    finally:
        conn.close()

def get_conn():
    return pymysql.connect(**DB_CONFIG)


# ---------- 1) กลุ่มเรียน: เข้าห้องด้วยรหัส ----------
@app.post("/classes/join")
def join_class(data: dict):
    user_id = data.get("user_id")
    join_code = str(data.get("join_code", "")).strip().upper()
    if not user_id or not join_code:
        return {"success": False, "error": "ข้อมูลไม่ครบ"}

    conn = get_conn()
    try:
        with conn.cursor() as c:
            c.execute("SELECT * FROM class_groups WHERE join_code = %s", (join_code,))
            cls = c.fetchone()
            if not cls:
                return {"success": False, "error": "รหัสห้องเรียนไม่ถูกต้อง"}

            # INSERT IGNORE: ถ้าเคยเข้าแล้ว จะไม่เพิ่มซ้ำและไม่ error
            c.execute(
                "INSERT IGNORE INTO enrollments (user_id, class_group_id) VALUES (%s, %s)",
                (user_id, cls["id"]),
            )
            conn.commit()
            return {"success": True, "class": cls}
    except Exception as e:
        return {"success": False, "error": f"Database Error: {str(e)}"}
    finally:
        conn.close()


# ---------- 2) กลุ่มเรียน: ออกจากห้อง ----------
@app.post("/classes/leave")
def leave_class(data: dict):
    user_id = data.get("user_id")
    class_group_id = data.get("class_group_id")
    if not user_id or not class_group_id:
        return {"success": False, "error": "ข้อมูลไม่ครบ"}

    conn = get_conn()
    try:
        with conn.cursor() as c:
            c.execute(
                "DELETE FROM enrollments WHERE user_id = %s AND class_group_id = %s",
                (user_id, class_group_id),
            )
            conn.commit()
            return {"success": True}
    except Exception as e:
        return {"success": False, "error": f"Database Error: {str(e)}"}
    finally:
        conn.close()


# ---------- 3) กลุ่มเรียน: รายวิชาของฉัน ----------
@app.get("/classes/my/{user_id}")
def my_classes(user_id: int):
    conn = get_conn()
    try:
        with conn.cursor() as c:
            c.execute(
                """SELECT g.* FROM class_groups g
                   JOIN enrollments e ON e.class_group_id = g.id
                   WHERE e.user_id = %s
                   ORDER BY e.joined_at DESC""",
                (user_id,),
            )
            return {"success": True, "data": c.fetchall()}
    except Exception as e:
        return {"success": False, "error": f"Database Error: {str(e)}"}
    finally:
        conn.close()


# ---------- 4) กลุ่มเรียน: รายละเอียดห้องเดียว ----------
@app.get("/classes/{class_id}")
def class_detail(class_id: int):
    conn = get_conn()
    try:
        with conn.cursor() as c:
            c.execute("SELECT * FROM class_groups WHERE id = %s", (class_id,))
            cls = c.fetchone()
            if not cls:
                return {"success": False, "error": "ไม่พบห้องเรียน"}
            return {"success": True, "class": cls}
    except Exception as e:
        return {"success": False, "error": f"Database Error: {str(e)}"}
    finally:
        conn.close()


# ---------- 5) ภาค: กลางภาค / ปลายภาค ของห้องนี้ ----------
@app.get("/classes/{class_id}/sections")
def get_sections(class_id: int):
    conn = get_conn()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cur:
            cur.execute(
                """
                SELECT section_id as id, class_group_id, name,
                       day_sob,
                       TIME_FORMAT(start_sob_time, '%%H:%%i') AS start_sob_time,
                       TIME_FORMAT(end_sob_time, '%%H:%%i') AS end_sob_time
                FROM sections
                WHERE class_group_id = %s
                ORDER BY sort_order Asc
                """,
                (class_id,),
            )
            rows = cur.fetchall()
        for r in rows:
            r["day_sob"] = r["day_sob"].isoformat() if r["day_sob"] else None
        return {"success": True, "sections": rows}
    finally:
        conn.close()


# ---------- 6) บท: บทในภาคนี้ พร้อมสถานะติ๊กถูกของนักเรียน ----------
SLIDES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads", "slides")


@app.get("/chapters/{chapter_id}/slides")
def get_chapter_slides(chapter_id: int):
    conn = get_conn()
    try:
        with conn.cursor() as c:
            c.execute(
                """SELECT slide_id, title, file_name
                   FROM slides
                   WHERE chapter_id = %s
                   ORDER BY slide_id""",
                (chapter_id,),
            )
            return {"success": True, "slides": c.fetchall()}
    except Exception as e:
        return {"success": False, "error": f"Database Error: {str(e)}"}
    finally:
        conn.close()


@app.get("/slides/{slide_id}/file")
def get_slide_file(slide_id: int, download: int = 0):
    conn = get_conn()
    try:
        with conn.cursor() as c:
            c.execute("SELECT file_name FROM slides WHERE slide_id = %s", (slide_id,))
            row = c.fetchone()
    finally:
        conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="ไม่พบสไลด์")

    # basename กันการใส่ path แปลกๆ ออกนอกโฟลเดอร์
    name = os.path.basename(row["file_name"])
    path = os.path.join(SLIDES_DIR, name)
    if not os.path.isfile(path):
        raise HTTPException(status_code=404, detail="ไม่พบไฟล์ PDF บนเซิร์ฟเวอร์")

    return FileResponse(
        path,
        media_type="application/pdf",
        filename=name,
        content_disposition_type="attachment" if download else "inline",
    )

# ---------- 7) ความคืบหน้า: บันทึกว่าส่ง Quiz / Lab แล้ว ----------
@app.post("/progress/update")
def update_progress(data: dict):
    user_id = data.get("user_id")
    chapter_id = data.get("chapter_id")
    quiz_done = 1 if data.get("quiz_done") else 0
    lab_done = 1 if data.get("lab_done") else 0
    if not user_id or not chapter_id:
        return {"success": False, "error": "ข้อมูลไม่ครบ"}

    conn = get_conn()
    try:
        with conn.cursor() as c:
            c.execute(
                """INSERT INTO chapter_progress (user_id, chapter_id, quiz_done, lab_done)
                   VALUES (%s, %s, %s, %s)
                   ON DUPLICATE KEY UPDATE quiz_done = VALUES(quiz_done),
                                           lab_done  = VALUES(lab_done)""",
                (user_id, chapter_id, quiz_done, lab_done),
            )
            conn.commit()
            return {"success": True}
    except Exception as e:
        return {"success": False, "error": f"Database Error: {str(e)}"}
    finally:
        conn.close()

def get_current_user(request: Request) -> int:
    token = request.cookies.get("token")
    if not token:
        raise HTTPException(status_code=401, detail="ยังไม่ได้ล็อกอิน")
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="token ไม่ถูกต้องหรือหมดอายุ")
    return payload["user_id"]


@app.get("/auth/me")
def auth_me(user_id: int = Depends(get_current_user)):
    conn = get_conn()
    try:
        with conn.cursor() as c:
            c.execute("SELECT user_id, name, email, picture FROM users WHERE user_id = %s", (user_id,))
            user = c.fetchone()
        return {"success": True, "user": user}
    finally:
        conn.close()


@app.post("/auth/logout")
def auth_logout(response: Response):
    response.delete_cookie("token")
    return {"success": True}

@app.get("/sections/{section_id}")
def get_section(section_id: int):
    conn = get_conn()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cur:
            cur.execute(
                """
                SELECT s.section_id AS id,
                       s.name,
                       s.class_group_id AS class_id,
                       c.course_title
                FROM sections s
                JOIN class_groups c ON c.id = s.class_group_id
                WHERE s.section_id = %s
                """,
                (section_id,),
            )
            row = cur.fetchone()
        if not row:
            return {"success": False, "error": "ไม่พบเนื้อหานี้"}
        return {"success": True, "section": row}
    finally:
        conn.close()


@app.get("/sections/{section_id}/chapters")
def get_chapters(section_id: int, user_id: int = 0):
    conn = get_conn()
    try:
        with conn.cursor() as c:
            c.execute(
                """SELECT ch.*,
                          COALESCE(p.quiz_done, 0) AS quiz_done,
                          COALESCE(p.lab_done, 0)  AS lab_done
                   FROM chapters ch
                   LEFT JOIN chapter_progress p
                          ON p.chapter_id = ch.id AND p.user_id = %s
                   WHERE ch.section_id = %s
                   ORDER BY ch.chapter_no""",
                (user_id, section_id),
            )
            return {"success": True, "data": c.fetchall()}
    except Exception as e:
        return {"success": False, "error": f"Database Error: {str(e)}"}
    finally:
        conn.close()

@app.get("/chapters/{chapter_id}")
def get_chapter(chapter_id: int):
    conn = get_conn()
    try:
        with conn.cursor() as c:
            c.execute(
                """SELECT ch.id, ch.chapter_no, ch.title, ch.section_id,
                          s.name AS section_name
                   FROM chapters ch
                   JOIN sections s ON s.section_id = ch.section_id
                   WHERE ch.id = %s""",
                (chapter_id,),
            )
            row = c.fetchone()
        if not row:
            return {"success": False, "error": "ไม่พบบทเรียน"}
        return {"success": True, "chapter": row}
    except Exception as e:
        return {"success": False, "error": f"Database Error: {str(e)}"}
    finally:
        conn.close()
@app.get("/chapters/{chapter_id}/labs")
def get_chapter_labs(chapter_id: int):
    conn = get_conn()
    try:
        with conn.cursor() as c:
            c.execute(
                "SELECT * FROM lab WHERE lab_ofchapter = %s",
                (chapter_id,),
            )
            return {"success": True, "labs": c.fetchall()}
    except Exception as e:
        return {"success": False, "error": f"Database Error: {str(e)}"}
    finally:
        conn.close()

@app.get("/admin/teachers")
def list_teachers(user_id: int = Depends(get_current_user)):
    # TODO: ตรวจว่าผู้เรียกเป็นแอดมินจริง (ตอนนี้แค่ต้องล็อกอิน)
    conn = get_conn()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cur:
            cur.execute(
                """
                SELECT u.user_id AS id,
                       u.email,
                       u.name,
                       u.picture,
                       GROUP_CONCAT(DISTINCT cg.group_name
                                    ORDER BY cg.group_name SEPARATOR ', ') AS group_names,
                       GROUP_CONCAT(DISTINCT cg.term
                                    ORDER BY cg.term SEPARATOR ', ') AS term_list
                FROM users u
                LEFT JOIN class_groups cg ON cg.teacher_name = u.name
                WHERE u.role = 1
                GROUP BY u.user_id, u.email, u.name, u.picture
                ORDER BY u.name
                """
            )
            rows = cur.fetchall()
        return {"success": True, "data": rows}
    finally:
        conn.close()

@app.post("/admin/teachers")
def create_teacher(data: dict):
    conn = get_conn()
    try:
        with conn.cursor() as c:
            c.execute(
                "INSERT INTO users (email, name, picture, role) VALUES (%s, %s, '', 2)",
                (data["email"], data["name"] + " " + data["surname"]),
            )
            conn.commit()
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": f"Database Error: {str(e)}"}
    finally:
        conn.close()
@app.get("/admin/class-groups")
def list_class_groups():
    conn = get_conn()
    try:
        with conn.cursor() as c:
            c.execute(
                """
                SELECT id, group_name, term,
                       teacher_name AS teacher,
                       	teacher_assist AS assistant
                FROM class_groups
                ORDER BY term, group_name
                """
            )
            rows = c.fetchall()
        return {"success": True, "data": rows}
    except Exception as e:
        return {"success": False, "error": f"Database Error: {str(e)}"}
    finally:
        conn.close()



@app.post("/admin/insert-class-groups")
def create_class_group(data: dict):
    join_code = str(random.randint(1000, 9999))
    assistant = data.get("assistant") or None
    conn = get_conn()
    try:
        with conn.cursor() as c:
            c.execute(
                """
                INSERT INTO class_groups
                (join_code, course_title, term, group_name, teacher_name, teacher_assist)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (join_code, data["detail"], data["term"], data["group_name"], data["teacher"], assistant),
            )
        conn.commit()
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": f"Database Error: {str(e)}"}
    finally:
        conn.close()
@app.get("/admin/terms")
def term_options():
    conn = get_conn()
    try:
        with conn.cursor() as c:
            c.execute("SELECT id_term, term FROM term ORDER BY id_term")
            rows = c.fetchall()
        return {"success": True, "data": rows}
    except Exception as e:
        return {"success": False, "error": f"Database Error: {str(e)}"}
    finally:
        conn.close()
@app.get("/admin/teacher-options")
def teacher_options():
    conn = get_conn()
    try:
        with conn.cursor() as c:
            c.execute("SELECT user_id, name FROM users WHERE role = 1 ORDER BY name")
            rows = c.fetchall()
        return {"success": True, "data": rows}
    except Exception as e:
        return {"success": False, "error": f"Database Error: {str(e)}"}
    finally:
        conn.close()


@app.post("/admin/upload-file")
def upload_file(
    chapter_id: int = Form(...),
    term: str = Form(...),
    video_url: str = Form(""),
    file: UploadFile = File(None),
):
    if file is None:
        return {"success": False, "error": "กรุณาเลือกไฟล์ PDF"}
    if not file.filename.lower().endswith(".pdf"):
        return {"success": False, "error": "รองรับเฉพาะไฟล์ .pdf"}

    content = file.file.read()
    if len(content) > 50 * 1024 * 1024:
        return {"success": False, "error": "ไฟล์ใหญ่เกิน 50MB"}

    slides_dir = os.path.join(UPLOAD_DIR, "slides")
    os.makedirs(slides_dir, exist_ok=True)
    stored_name = uuid.uuid4().hex + ".pdf"
    with open(os.path.join(slides_dir, stored_name), "wb") as f:
        f.write(content)

    conn = get_conn()
    try:
        with conn.cursor() as c:
            c.execute(
                """
                INSERT INTO slides (chapter_id, title, file_name, video_url, term)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (chapter_id, file.filename, stored_name, video_url or None, term),
            )
        conn.commit()
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": f"Database Error: {str(e)}"}
    finally:
        conn.close()




@app.post("/admin/train-ai/upload")
def upload_train_ai(files: list[UploadFile] = File(...)):
    # ตรวจทุกไฟล์ก่อน ถ้ามีไฟล์ไม่ผ่านจะไม่บันทึกเลย
    items = []
    for file in files:
        name = os.path.basename(file.filename)
        if not name.lower().endswith(".pdf"):
            return {"success": False, "error": f"{name} ไม่ใช่ไฟล์ .pdf"}
        content = file.file.read()
        if len(content) > 50 * 1024 * 1024:
            return {"success": False, "error": f"{name} ใหญ่เกิน 50MB"}
        items.append((name, content))

    train_dir = os.path.join(UPLOAD_DIR, "trainAI")
    os.makedirs(train_dir, exist_ok=True)

    conn = get_conn()
    try:
        with conn.cursor() as c:
            for name, content in items:
                stored_name = uuid.uuid4().hex[:8] + "_" + name
                with open(os.path.join(train_dir, stored_name), "wb") as f:
                    f.write(content)
                c.execute(
                    "INSERT INTO trainpdf (filename) VALUES (%s)",
                    (stored_name,),
                )
        conn.commit()
        return {"success": True, "count": len(items)}
    except Exception as e:
        return {"success": False, "error": f"Database Error: {str(e)}"}
    finally:
        conn.close()



@app.get("/admin/chapter-options")
def chapter_options():
    conn = get_conn()
    try:
        with conn.cursor() as c:
            c.execute(
                """
                SELECT chapters.id, chapters.chapter_no, chapters.title,
                       sections.name AS section_name
                FROM chapters
                JOIN sections ON sections.section_id = chapters.section_id
                ORDER BY sections.sort_order, chapters.chapter_no
                """
            )
            rows = c.fetchall()
        return {"success": True, "data": rows}
    except Exception as e:
        return {"success": False, "error": f"Database Error: {str(e)}"}
    finally:
        conn.close()

@app.get("/admin/labs")
def list_labs():
    conn = get_conn()
    try:
        with conn.cursor() as c:
            c.execute(
                """
                SELECT id_lab, namelab, lab_ofchapter
                FROM lab
                ORDER BY lab_ofchapter, id_lab
                """
            )
            rows = c.fetchall()
        return {"success": True, "data": rows}
    except Exception as e:
        return {"success": False, "error": f"Database Error: {str(e)}"}
    finally:
        conn.close()

@app.post("/admin/labs")
def create_lab(data: dict):
    conn = get_conn()
    try:
        with conn.cursor() as c:
            c.execute(
                "INSERT INTO lab (namelab, detail, lab_ofchapter) VALUES (%s, %s, %s)",
                (data["namelab"], data["detail"], data["chapter_id"]),
            )
        conn.commit()
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": f"Database Error: {str(e)}"}
    finally:
        conn.close()

@app.get("/admin/quiz-questions")
def list_quiz_questions():
    conn = get_conn()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as c:
            c.execute(
                """
                SELECT q.question_id, q.chapter_id, q.question,
                       ch.chapter_no, ch.title AS chapter_title,
                       s.name AS section_name,
                       g.term
                FROM quiz_questions q
                LEFT JOIN chapters ch ON ch.id = q.chapter_id
                LEFT JOIN sections s ON s.section_id = ch.section_id
                LEFT JOIN class_groups g ON g.id = s.class_group_id
                ORDER BY g.term, s.sort_order, ch.chapter_no, q.question_id
                """
            )
            return {"success": True, "data": c.fetchall()}
    except Exception as e:
        return {"success": False, "error": f"Database Error: {str(e)}"}
    finally:
        conn.close()
        
QUIZ_UPLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads", "quiz")

os.makedirs(QUIZ_UPLOAD_DIR, exist_ok=True)
app.mount("/uploads/quiz", StaticFiles(directory=QUIZ_UPLOAD_DIR), name="quiz_images")


@app.post("/admin/quiz-questions")
def create_quiz_question(
    chapter_id: int = Form(...),
    question: str = Form(...),
    choice_a: str = Form(""),
    choice_b: str = Form(""),
    choice_c: str = Form(""),
    choice_d: str = Form(""),
    correct_choice: str = Form(...),
    explanation: str = Form(""),
    explanation_wrong: str = Form(""),
    image: UploadFile | None = File(None),
):
    if correct_choice not in ("a", "b", "c", "d"):
        return {"success": False, "error": "คำตอบที่ถูกต้องไม่ถูกต้อง"}

    quiz_dir = os.path.join(UPLOAD_DIR, "quiz")

    # รูปโจทย์ (ถ้ามี): รับเฉพาะ png/jpg/jpeg ไม่เกิน 50MB เก็บชื่อสุ่มบนดิสก์ กันชื่อซ้ำ/path อันตราย
    image_file = None
    if image and image.filename:
        ext = os.path.splitext(image.filename)[1].lower()
        if ext not in (".png", ".jpg", ".jpeg"):
            return {"success": False, "error": "รองรับเฉพาะไฟล์ .png .jpg .jpeg"}
        limit = 50 * 1024 * 1024
        data = image.file.read(limit + 1)
        if len(data) > limit:
            return {"success": False, "error": "ไฟล์ใหญ่เกิน 50MB"}
        os.makedirs(quiz_dir, exist_ok=True)
        image_file = uuid.uuid4().hex + ext
        with open(os.path.join(quiz_dir, image_file), "wb") as f:
            f.write(data)

    conn = get_conn()
    try:
        with conn.cursor() as c:
            c.execute(
                "INSERT INTO quiz_questions (chapter_id, question, choice_a, choice_b, choice_c, "
                "choice_d, correct_choice, image_file, explanation, explanation_wrong) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (chapter_id, question, choice_a, choice_b, choice_c, choice_d,
                 correct_choice, image_file, explanation, explanation_wrong),
            )
            conn.commit()
        return {"success": True}
    except Exception as e:
        if image_file:  # บันทึก DB ไม่สำเร็จ ลบรูปที่เพิ่งเก็บทิ้ง
            try:
                os.remove(os.path.join(quiz_dir, image_file))
            except OSError:
                pass
        return {"success": False, "error": f"Database Error: {str(e)}"}
    finally:
        conn.close()


def save_quiz_image(f):
    """บันทึกรูปลง uploads/quiz คืนค่า (ชื่อไฟล์ที่เก็บ, ข้อความ error)"""
    if not f or not f.filename:
        return None, None
    ext = os.path.splitext(f.filename)[1].lower()
    if ext not in (".png", ".jpg", ".jpeg"):
        return None, "รองรับเฉพาะไฟล์ .png .jpg .jpeg"
    limit = 50 * 1024 * 1024
    data = f.file.read(limit + 1)
    if len(data) > limit:
        return None, "ไฟล์ใหญ่เกิน 50MB"
    os.makedirs(QUIZ_UPLOAD_DIR, exist_ok=True)
    name = uuid.uuid4().hex + ext
    with open(os.path.join(QUIZ_UPLOAD_DIR, name), "wb") as out:
        out.write(data)
    return name, None


@app.post("/admin/quiz-questions")
def create_quiz_question(
    chapter_id: int = Form(...),
    question: str = Form(...),
    choice_type: str = Form("text"),
    choice_a: str = Form(""),
    choice_b: str = Form(""),
    choice_c: str = Form(""),
    choice_d: str = Form(""),
    correct_choice: str = Form(...),
    explanation: str = Form(""),
    explanation_wrong: str = Form(""),
    image: UploadFile | None = File(None),
    choice_image_a: UploadFile | None = File(None),
    choice_image_b: UploadFile | None = File(None),
    choice_image_c: UploadFile | None = File(None),
    choice_image_d: UploadFile | None = File(None),
):
    if choice_type not in ("text", "image"):
        return {"success": False, "error": "ชนิดตัวเลือกไม่ถูกต้อง"}
    if correct_choice not in ("a", "b", "c", "d"):
        return {"success": False, "error": "คำตอบที่ถูกต้องไม่ถูกต้อง"}

    saved = []  # ไฟล์ที่เพิ่งเก็บ ไว้ลบทิ้งถ้าบันทึกไม่สำเร็จ

    def cleanup():
        for n in saved:
            try:
                os.remove(os.path.join(QUIZ_UPLOAD_DIR, n))
            except OSError:
                pass

    # รูปโจทย์ (ถ้ามี)
    image_file, err = save_quiz_image(image)
    if err:
        return {"success": False, "error": err}
    if image_file:
        saved.append(image_file)

    choices = {"a": choice_a, "b": choice_b, "c": choice_c, "d": choice_d}

    # ถ้าตัวเลือกเป็นรูป: เก็บไฟล์แล้วใส่ชื่อไฟล์ลงช่อง choice_x แทนข้อความ
    if choice_type == "image":
        for letter, f in (("a", choice_image_a), ("b", choice_image_b),
                          ("c", choice_image_c), ("d", choice_image_d)):
            name, err = save_quiz_image(f)
            if err:
                cleanup()
                return {"success": False, "error": err}
            if name:
                saved.append(name)
            choices[letter] = name or ""

    if not choices[correct_choice]:
        cleanup()
        return {"success": False, "error": "คำตอบที่ถูกต้องต้องเป็นตัวเลือกที่มีข้อมูล"}

    conn = get_conn()
    try:
        with conn.cursor() as c:
            c.execute(
                "INSERT INTO quiz_questions (chapter_id, question, choice_type, choice_a, choice_b, "
                "choice_c, choice_d, correct_choice, image_file, explanation, explanation_wrong) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (chapter_id, question, choice_type, choices["a"], choices["b"], choices["c"],
                 choices["d"], correct_choice, image_file, explanation, explanation_wrong),
            )
            conn.commit()
        return {"success": True}
    except Exception as e:
        cleanup()
        return {"success": False, "error": f"Database Error: {str(e)}"}
    finally:
        conn.close()

@app.get("/admin/train-pdfs")
def list_train_pdfs():
    conn = get_conn()
    try:
        with conn.cursor() as c:
            c.execute(
                "SELECT id_file, filename, created_at FROM trainpdf ORDER BY id_file DESC"
            )
            rows = c.fetchall()
        return {"success": True, "data": rows}
    except Exception as e:
        return {"success": False, "error": f"Database Error: {str(e)}"}
    finally:
        conn.close()

# =====================================================
#  สร้างโจทย์ด้วย AI จากเอกสาร (trainpdf)
# =====================================================
TRAIN_DIR = os.path.join(UPLOAD_DIR, "trainAI")

MAX_DOC_CHARS = 700000      # ข้อความรวมที่ส่งให้ AI ยิ่งน้อยยิ่งเร็ว (เดิม 700000)
MAX_IMAGES = 10             # จำนวนภาพแนบสูงสุด (เดิม 8)
IMAGE_DPI = 80             # ความละเอียดภาพ (เดิม 110)
GEMINI_TIMEOUT = (10, 60)  # (รอเชื่อมต่อ, รอคำตอบ) วินาที ต่อ 1 โมเดล (เดิม 180)

# ตัวควบอักษร (ligature) ใน PDF เช่น ﬃ ให้แปลงกลับเป็น ffi
# ห้ามใช้ NFKC เพราะจะทำให้สระ "ำ" ในภาษาไทยเพี้ยน
LIGATURES = str.maketrans(
    {"\ufb00": "ff", "\ufb01": "fi", "\ufb02": "fl", "\ufb03": "ffi", "\ufb04": "ffl"}
)


def content_image_xrefs(doc):
    """xref ของรูปที่เป็นเนื้อหาจริง
    ตัดรูปเล็ก (โลโก้/ไอคอน) และรูปที่ซ้ำเกือบทุกหน้า (พื้นหลังสไลด์) ออก"""
    pages_of = {}
    for i, page in enumerate(doc):
        for img in page.get_images(full=True):
            xref, w, h = img[0], img[2], img[3]
            if w < 200 or h < 150:
                continue
            pages_of.setdefault(xref, set()).add(i)
    n = max(len(doc), 1)
    keep = set()
    for xref, pgs in pages_of.items():
        if len(pgs) >= 3 and len(pgs) / n > 0.3:
            continue  # ซ้ำเกือบทุกหน้า = พื้นหลัง
        keep.add(xref)
    return keep


def page_has_content_image(page, keep):
    return any(img[0] in keep for img in page.get_images(full=True))


def pdf_to_markdown(pdf_path):
    """ถอดข้อความทุกหน้าเป็น markdown แบ่งด้วย ## หน้า N"""
    doc = fitz.open(pdf_path)
    keep = content_image_xrefs(doc)
    parts = []
    total = 0
    for i, page in enumerate(doc, start=1):
        text = page.get_text().translate(LIGATURES).strip()
        total += len(text)
        note = ""
        if page_has_content_image(page, keep):
            note = "\n(หน้านี้มีรูปภาพ ข้อความด้านบนไม่รวมเนื้อหาในรูป)"
        parts.append(f"## หน้า {i}\n{text}{note}")
    n = len(doc)
    doc.close()
    if n == 0 or total / n < 50:
        raise ValueError("ไฟล์นี้น่าจะเป็นไฟล์สแกน ดึงข้อความไม่ได้")
    return "\n\n".join(parts)


def get_doc_text(filename):
    """อ่านจากไฟล์ .md ถ้ามี ไม่งั้นสร้างจาก PDF แล้วเก็บไว้ข้างไฟล์ PDF"""
    pdf_path = os.path.join(TRAIN_DIR, os.path.basename(filename))
    md_path = os.path.splitext(pdf_path)[0] + ".md"
    if os.path.isfile(md_path):
        with open(md_path, "r", encoding="utf-8") as f:
            return f.read()
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"ไม่พบไฟล์ {filename} บนเซิร์ฟเวอร์")
    text = pdf_to_markdown(pdf_path)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(text)
    return text


def trim_pages(text, budget, start_page=1):
    """เริ่มเก็บจากหน้า start_page จนเต็มงบตัวอักษร คืน (ข้อความ, เลขหน้าสุดท้ายที่เก็บไว้)"""
    pages = re.split(r"\n\n(?=## หน้า \d+\n)", text)
    kept, size, last_no = [], 0, start_page - 1
    for p in pages:
        m = re.match(r"## หน้า (\d+)\n", p)
        if not m or int(m.group(1)) < start_page:
            continue
        if kept and size + len(p) > budget:
            break
        kept.append(p)
        size += len(p)
        last_no = int(m.group(1))
    return "\n\n".join(kept), last_no


MIN_W_PT = 90        # ความกว้างขั้นต่ำของรูปที่วางจริงบนหน้า (หน่วย pt)
MIN_H_PT = 60        # ความสูงขั้นต่ำ
MAX_PAGE_RATIO = 0.80  # รูปที่กินพื้นที่เกินนี้ถือเป็นพื้นหลัง/หน้าปก
MERGE_GAP = 8        # รูปที่ห่างกันไม่เกินนี้ (pt) ให้รวมเป็นกรอบเดียว
CLIP_PAD = 4         # เผื่อขอบกันตัดเฉียดเนื้อหา


def merge_rects(rects, gap=MERGE_GAP):
    """รวมกรอบที่ซ้อนทับ/อยู่ติดกันให้เป็นกรอบเดียว (ใช้แก้รูปที่ถูกหั่นเป็นชิ้น)"""
    rects = [fitz.Rect(r) for r in rects]
    changed = True
    while changed:
        changed = False
        result = []
        while rects:
            a = rects.pop()
            i = 0
            while i < len(rects):
                grown = fitz.Rect(a.x0 - gap, a.y0 - gap, a.x1 + gap, a.y1 + gap)
                if grown.intersects(rects[i]):
                    a = a | rects.pop(i)
                    changed = True
                else:
                    i += 1
            result.append(a)
        rects = result
    return rects


def render_image_pages(pdf_path, max_images, first_page, last_page):
    """ครอปรูปเนื้อหาจริง: รวมชิ้นที่ติดกัน, ตัดเศษเล็ก, ตัดรูปเต็มหน้า
    คืน list ของ (เลขหน้า, ลำดับรูปในหน้า เริ่ม 0, bytes)"""
    doc = fitz.open(pdf_path)
    keep = content_image_xrefs(doc)
    out = []
    for i, page in enumerate(doc, start=1):
        if i < first_page:
            continue
        if i > last_page or len(out) >= max_images:
            break

        page_area = page.rect.width * page.rect.height
        rects = []
        for img in page.get_images(full=True):
            xref = img[0]
            if xref not in keep:
                continue
            try:
                for r in page.get_image_rects(xref):   # เอาทุกตำแหน่ง ไม่ใช่แค่ [0]
                    r = r & page.rect
                    if not r.is_empty:
                        rects.append(r)
            except Exception:
                continue

        merged = merge_rects(rects)
        merged.sort(key=lambda r: (round(r.y0), r.x0))  # เรียงบน->ล่าง ซ้าย->ขวา

        idx = 0
        for r in merged:
            if r.width < MIN_W_PT or r.height < MIN_H_PT:
                continue                                   # เศษเล็ก
            if (r.width * r.height) / page_area > MAX_PAGE_RATIO:
                continue                                   # พื้นหลัง/หน้าปก
            clip = fitz.Rect(r.x0 - CLIP_PAD, r.y0 - CLIP_PAD,
                             r.x1 + CLIP_PAD, r.y1 + CLIP_PAD) & page.rect
            pix = page.get_pixmap(dpi=IMAGE_DPI, clip=clip)
            try:
                data = pix.tobytes("jpeg", jpg_quality=70)
            except TypeError:
                data = pix.tobytes("jpeg")
            out.append((i, idx, data))
            idx += 1
            if len(out) >= max_images:
                break
    doc.close()
    return out

def thinking_config(model):
    """ปิด/ลดการคิดของโมเดลเพื่อให้ตอบเร็ว"""
    if "gemini-3" in model:
        return {"thinkingLevel": "minimal"}
    if "2.5" in model and "pro" not in model:
        return {"thinkingBudget": 0}
    return None


def call_gemini_quiz(prompt, images):
    """ส่งข้อความ + ภาพ ให้ Gemini ตอบเป็น JSON คืน (ข้อความ, error)
    ถ้าโมเดลไหนล่ม (503/429 ฯลฯ) ข้ามไปโมเดลถัดไปทันที แล้วลองอีก 1 รอบ"""
    parts = [{"text": prompt}]
    for ref, img in images:
        parts.append({"text": f"ภาพของหน้า {ref}:"})
        parts.append({"inline_data": {
            "mime_type": "image/jpeg",
            "data": base64.b64encode(img).decode(),
        }})

    last_err = ""
    for attempt in range(2):
        if attempt:
            time.sleep(2)
        for model in GEMINI_MODELS:
            think = thinking_config(model)
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
            # ลองพร้อม thinkingConfig ก่อน ถ้า 400 (โมเดลไม่รองรับ) ลองซ้ำแบบไม่ใส่
            for use_think in ((True, False) if think else (False,)):
                gen = {"temperature": 0.3, "responseMimeType": "application/json"}
                if use_think:
                    gen["thinkingConfig"] = think
                body = {"contents": [{"parts": parts}], "generationConfig": gen}
                try:
                    r = http_requests.post(
                        url, headers={"x-goog-api-key": GEMINI_API_KEY},
                        json=body, timeout=GEMINI_TIMEOUT,
                    )
                except Exception as e:
                    last_err = f"{model}: {type(e).__name__}"
                    print("Gemini quiz error:", last_err)
                    break  # โมเดลถัดไป

                if r.status_code == 200:
                    try:
                        ps = r.json()["candidates"][0]["content"]["parts"]
                        text = "".join(p.get("text", "") for p in ps).strip()
                    except (KeyError, IndexError, TypeError):
                        text = ""
                    if text:
                        print(f"Gemini quiz OK: {model} thinking={'on' if use_think else 'off'} "
                              f"ใช้เวลา {r.elapsed.total_seconds():.1f} วินาที")
                        return text, ""
                    last_err = f"{model}: ตอบกลับว่าง"
                    break

                last_err = f"{model}: HTTP {r.status_code}"
                print("Gemini quiz error:", last_err, r.text[:200])
                if r.status_code == 400 and use_think:
                    continue  # ลองโมเดลเดิมอีกครั้งโดยไม่ใส่ thinkingConfig
                if r.status_code in (401, 403):
                    return "", last_err  # คีย์ผิด ลองต่อก็ไม่มีประโยชน์
                break  # 503/429/อื่นๆ -> โมเดลถัดไปทันที
    return "", last_err


@app.post("/admin/quiz-ai/generate")
def generate_quiz_ai(data: dict):
    if not GEMINI_API_KEY:
        return {"success": False, "error": "ยังไม่ได้ตั้ง GEMINI_API_KEY ใน .env"}

    file_ids = data.get("file_ids") or []
    if not file_ids:
        return {"success": False, "error": "กรุณาเลือกเอกสารอย่างน้อย 1 ไฟล์"}
    try:
        count = max(1, min(int(data.get("count", 10)), 20))
    except (TypeError, ValueError):
        count = 10

    # ชนิดตัวเลือกที่ครูเลือกในหน้าเพิ่มโจทย์
    # text = ข้อความล้วน (ไม่ใช้รูปเลย) / image = ทุกข้อใช้รูป (โจทย์มีรูป + ตัวเลือกเป็นรูป)
    choice_type = data.get("choice_type", "text")
    if choice_type not in ("text", "image"):
        choice_type = "text"
    image_mode = choice_type == "image"
    with_images = image_mode

    try:
        start_page = max(1, int(data.get("start_page", 1)))
    except (TypeError, ValueError):
        start_page = 1

    t0 = time.time()

    # 1) หาชื่อไฟล์จากตาราง trainpdf
    names = []
    conn = get_conn()
    try:
        with conn.cursor() as c:
            for fid in file_ids:
                c.execute("SELECT filename FROM trainpdf WHERE id_file = %s", (fid,))
                row = c.fetchone()
                if not row:
                    return {"success": False, "error": f"ไม่พบเอกสาร id {fid}"}
                names.append(row["filename"])
    finally:
        conn.close()

    # 2) ถอดข้อความ (เริ่มจากหน้า start_page ตัดตามงบตัวอักษร) + ครอปรูปเฉพาะหน้าที่ส่งข้อความไป
    doc_text = ""
    images = []  # (อ้างอิง "ไฟล์:หน้า" หรือ "ไฟล์:หน้า.ลำดับรูป", jpeg bytes)
    budget = MAX_DOC_CHARS // len(names)
    try:
        for k, name in enumerate(names, start=1):
            text, last_page = trim_pages(get_doc_text(name), budget, start_page)
            doc_text += f"\n\n# ไฟล์ {k}: {name}\n" + text
            if with_images and len(images) < MAX_IMAGES:
                pdf_path = os.path.join(TRAIN_DIR, os.path.basename(name))
                for page_no, idx, img in render_image_pages(
                    pdf_path, MAX_IMAGES - len(images), start_page, last_page
                ):
                    ref = f"{k}:{page_no}" if idx == 0 else f"{k}:{page_no}.{idx + 1}"
                    images.append((ref, img))
    except Exception as e:
        return {"success": False, "error": f"อ่านเอกสารไม่สำเร็จ: {str(e)}"}
    t1 = time.time()

    if image_mode and not images:
        return {
            "success": False,
            "error": f"ไม่พบรูปภาพในเอกสารช่วงที่อ่าน (เริ่มหน้า {start_page}) "
                     "ลองเปลี่ยนเอกสาร หรือเลือกตัวเลือกแบบข้อความ",
        }

    # 3) สร้าง prompt
    if not image_mode:
        prompt = (
            f"คุณเป็นอาจารย์สอนภาษา C ออกข้อสอบปรนัยจำนวน {count} ข้อ จากเนื้อหาในเอกสารด้านล่างเท่านั้น\n"
            "ตอบเป็นภาษาไทย ตัวเลือก 4 ข้อ (ข้อจริง/เท็จใช้ 2 ตัวเลือกได้) มีคำตอบถูกเพียงข้อเดียว\n"
            "ไม่มีภาพแนบ ห้ามออกข้อที่ต้องดูรูป\n"
            "ตอบเป็น JSON array เท่านั้น แต่ละข้อมีฟิลด์:\n"
            '  "question": โจทย์,\n'
            '  "choices": [ตัวเลือก...],\n'
            '  "answer": ลำดับตัวเลือกที่ถูก เริ่มที่ 0,\n'
            '  "explanation": อธิบายว่าทำไมข้อที่ถูกจึงถูก (สั้น 1-2 ประโยค),\n'
            '  "explanation_wrong": อธิบายว่าข้อที่ผิดผิดเพราะอะไร (สั้น 1-2 ประโยค)\n'
        )
    else:
        refs = ", ".join(ref for ref, _ in images)
        prompt = (
            f"คุณเป็นอาจารย์สอนภาษา C ออกข้อสอบปรนัยจำนวน {count} ข้อ จากเนื้อหาในเอกสารด้านล่างเท่านั้น\n"
            "ตอบเป็นภาษาไทย มีคำตอบถูกเพียงข้อเดียว\n"
            f"มีภาพจากเอกสารแนบมา (อ้างอิง: {refs} รูปแบบ ไฟล์:หน้า หรือ ไฟล์:หน้า.ลำดับรูป)\n"
            "ทุกข้อต้องใช้ภาพ โดยออกผสมกัน 2 แบบ ประมาณครึ่งต่อครึ่ง:\n"
            '  แบบ A (โจทย์มีรูปประกอบ): ใส่ "image_ref" เป็นอ้างอิงของภาพ เขียนโจทย์ให้อ้างถึง "ภาพที่แนบ" '
            '"choices" เป็นข้อความ 4 ข้อ และ "choice_images" เป็น null\n'
            '  แบบ B (ตัวเลือกเป็นรูป): ถามให้เลือกภาพที่ตรงกับคำอธิบาย (เช่น "ภาพใดแสดง ...") '
            'ใส่ "choice_images" เป็นอ้างอิงของภาพ 2-4 ภาพที่ต่างกัน (ภาพที่ถูกต้องรวมอยู่ด้วย) '
            '"choices" เป็น [] และ "image_ref" เป็น null\n'
            "ในแบบ B ห้ามใช้ภาพเดียวกันซ้ำในข้อเดียวกัน ถ้ามีภาพแนบน้อยกว่า 2 ภาพ ห้ามออกแบบ B\n"
            "ภาพเดียวกันใช้ซ้ำข้ามข้อได้ แต่ต้องถามคนละประเด็น\n"
            "ตอบเป็น JSON array เท่านั้น แต่ละข้อมีฟิลด์:\n"
            '  "question": โจทย์,\n'
            '  "choices": [ตัวเลือกข้อความ...] (แบบ B ให้เป็น []),\n'
            '  "answer": ลำดับตัวเลือกที่ถูก เริ่มที่ 0 (แบบ B นับตามลำดับใน choice_images),\n'
            '  "explanation": อธิบายว่าทำไมข้อที่ถูกจึงถูก (สั้น 1-2 ประโยค),\n'
            '  "explanation_wrong": อธิบายว่าข้อที่ผิดผิดเพราะอะไร (สั้น 1-2 ประโยค),\n'
            '  "image_ref": อ้างอิงภาพ (แบบ A) หรือ null,\n'
            '  "choice_images": [อ้างอิงภาพ...] (แบบ B) หรือ null\n'
        )
    prompt += f"\n===== เอกสาร =====\n{doc_text}"

    # 4) เรียก Gemini
    text, err = call_gemini_quiz(prompt, images)
    t2 = time.time()
    if not text:
        return {"success": False, "error": f"AI ไม่ตอบกลับ ({err})"}

    # 5) แกะ JSON และตรวจแต่ละข้อ
    text = text.replace("```json", "").replace("```", "").strip()
    try:
        items = json.loads(text)
    except Exception:
        return {"success": False, "error": "AI ตอบผิดรูปแบบ ลองใหม่อีกครั้ง"}
    if isinstance(items, dict):
        items = items.get("questions")
    if not isinstance(items, list):
        return {"success": False, "error": "AI ตอบผิดรูปแบบ ลองใหม่อีกครั้ง"}

    img_by_ref = dict(images)
    saved_img = {}  # อ้างอิงภาพ -> ชื่อไฟล์ที่เซฟแล้ว (ใช้ภาพเดียวกันไม่เซฟซ้ำ)

    def save_ref(ref):
        if ref not in saved_img:
            os.makedirs(QUIZ_UPLOAD_DIR, exist_ok=True)
            fname = uuid.uuid4().hex + ".jpg"
            with open(os.path.join(QUIZ_UPLOAD_DIR, fname), "wb") as f:
                f.write(img_by_ref[ref])
            saved_img[ref] = fname
        return saved_img[ref]

    questions = []
    for q in items:
        if not isinstance(q, dict) or not q.get("question"):
            continue
        answer = q.get("answer")
        base = {
            "question": q["question"],
            "explanation": q.get("explanation", ""),
            "explanation_wrong": q.get("explanation_wrong", ""),
        }

        # แบบ B: ตัวเลือกเป็นรูป (เฉพาะโหมดรูปภาพ)
        refs_b = q.get("choice_images")
        if image_mode and isinstance(refs_b, list) and refs_b:
            ok = (
                2 <= len(refs_b) <= 4
                and all(isinstance(r, str) and r in img_by_ref for r in refs_b)
                and len(set(refs_b)) == len(refs_b)
                and isinstance(answer, int)
                and 0 <= answer < len(refs_b)
            )
            if ok:
                questions.append({
                    **base,
                    "choice_type": "image",
                    "choices": [save_ref(r) for r in refs_b],
                    "answer": answer,
                    "image_file": None,
                })
            continue

        # แบบ A และโหมดข้อความ: ตัวเลือกเป็นข้อความ
        choices = q.get("choices")
        if not isinstance(choices, list):
            continue
        if not (2 <= len(choices) <= 4) or not all(isinstance(x, str) and x.strip() for x in choices):
            continue
        if not isinstance(answer, int) or not (0 <= answer < len(choices)):
            continue

        image_file = None
        if image_mode:
            ref = q.get("image_ref")
            if not (isinstance(ref, str) and ref in img_by_ref):
                continue  # โหมดรูปภาพ: ทุกข้อต้องใช้รูป
            image_file = save_ref(ref)

        questions.append({
            **base,
            "choice_type": "text",
            "choices": choices,
            "answer": answer,
            "image_file": image_file,
        })

    print(f"[quiz-ai] โหมด {choice_type} | เริ่มหน้า {start_page} | ถอดข้อความ+เตรียมภาพ {t1 - t0:.1f}s | "
          f"Gemini {t2 - t1:.1f}s | รวม {time.time() - t0:.1f}s | ภาพแนบ {len(images)} | "
          f"ได้ {len(questions)} ข้อ")

    return {
        "success": True,
        "choice_type": choice_type,
        "files": [os.path.basename(n).split("_", 1)[-1] for n in names],
        "questions": questions,
    }

    # 2) ถอดข้อความ (ตัดตามงบตัวอักษร) + เตรียมภาพเฉพาะหน้าที่ส่งข้อความไป
    doc_text = ""
    images = []  # (อ้างอิง "ไฟล์:หน้า", jpeg bytes)
    budget = MAX_DOC_CHARS // len(names)
    try:
        for k, name in enumerate(names, start=1):
            text, last_page = trim_pages(get_doc_text(name), budget)
            doc_text += f"\n\n# ไฟล์ {k}: {name}\n" + text
            if with_images and len(images) < MAX_IMAGES:
                pdf_path = os.path.join(TRAIN_DIR, os.path.basename(name))
                for page_no, img in render_image_pages(pdf_path, MAX_IMAGES - len(images), last_page):
                    images.append((f"{k}:{page_no}", img))
    except Exception as e:
        return {"success": False, "error": f"อ่านเอกสารไม่สำเร็จ: {str(e)}"}
    t1 = time.time()

    # 3) สร้าง prompt (ให้คำอธิบายสั้น เพื่อให้ AI สร้างเสร็จเร็ว)
    prompt = (
        f"คุณเป็นอาจารย์สอนภาษา C ออกข้อสอบปรนัยจำนวน {count} ข้อ จากเนื้อหาในเอกสารด้านล่างเท่านั้น\n"
        "ตอบเป็นภาษาไทย ตัวเลือก 4 ข้อ (ข้อจริง/เท็จใช้ 2 ตัวเลือกได้) มีคำตอบถูกเพียงข้อเดียว\n"
        "ตอบเป็น JSON array เท่านั้น แต่ละข้อมีฟิลด์:\n"
        '  "question": โจทย์,\n'
        '  "choices": [ตัวเลือก...],\n'
        '  "answer": ลำดับตัวเลือกที่ถูก เริ่มที่ 0,\n'
        '  "explanation": อธิบายว่าทำไมข้อที่ถูกจึงถูก (สั้น 1-2 ประโยค),\n'
        '  "explanation_wrong": อธิบายว่าข้อที่ผิดผิดเพราะอะไร (สั้น 1-2 ประโยค),\n'
        '  "image_ref": ดูกฎด้านล่าง\n'
    )
    if images:
        refs = ", ".join(ref for ref, _ in images)
        prompt += (
            f"\nมีภาพของบางหน้าแนบมา (อ้างอิง: {refs} รูปแบบ ไฟล์:หน้า)\n"
            "ถ้าโจทย์ข้อไหนต้องดูภาพประกอบ (เช่น ผังงาน) ให้ใส่ image_ref เป็นอ้างอิงของภาพนั้น "
            'และเขียนโจทย์ให้อ้างถึง "ภาพที่แนบ" ส่วนข้อที่ไม่ต้องดูภาพให้ใส่ null\n'
        )
    else:
        prompt += '\nไม่มีภาพแนบ ห้ามออกข้อที่ต้องดูรูป และให้ใส่ image_ref เป็น null ทุกข้อ\n'
    prompt += f"\n===== เอกสาร =====\n{doc_text}"

    # 4) เรียก Gemini
    text, err = call_gemini_quiz(prompt, images)
    t2 = time.time()
    if not text:
        return {"success": False, "error": f"AI ไม่ตอบกลับ ({err})"}

    # 5) แกะ JSON และตรวจแต่ละข้อ
    text = text.replace("```json", "").replace("```", "").strip()
    try:
        items = json.loads(text)
    except Exception:
        return {"success": False, "error": "AI ตอบผิดรูปแบบ ลองใหม่อีกครั้ง"}
    if isinstance(items, dict):
        items = items.get("questions")
    if not isinstance(items, list):
        return {"success": False, "error": "AI ตอบผิดรูปแบบ ลองใหม่อีกครั้ง"}

    img_by_ref = dict(images)
    saved_img = {}  # อ้างอิงภาพ -> ชื่อไฟล์ที่เซฟแล้ว (ข้อที่ใช้ภาพเดียวกันไม่เซฟซ้ำ)
    questions = []
    for q in items:
        if not isinstance(q, dict):
            continue
        choices = q.get("choices")
        answer = q.get("answer")
        if not q.get("question") or not isinstance(choices, list):
            continue
        if not (2 <= len(choices) <= 4) or not all(isinstance(x, str) and x.strip() for x in choices):
            continue
        if not isinstance(answer, int) or not (0 <= answer < len(choices)):
            continue

        # ถ้าข้อนี้อ้างภาพ -> เซฟ JPEG ลงโฟลเดอร์ quiz
        image_file = None
        ref = q.get("image_ref")
        if isinstance(ref, str) and ref in img_by_ref:
            if ref not in saved_img:
                os.makedirs(QUIZ_UPLOAD_DIR, exist_ok=True)
                name = uuid.uuid4().hex + ".jpg"
                with open(os.path.join(QUIZ_UPLOAD_DIR, name), "wb") as f:
                    f.write(img_by_ref[ref])
                saved_img[ref] = name
            image_file = saved_img[ref]

        questions.append({
            "question": q["question"],
            "choices": choices,
            "answer": answer,
            "explanation": q.get("explanation", ""),
            "explanation_wrong": q.get("explanation_wrong", ""),
            "image_file": image_file,
        })

    print(f"[quiz-ai] ถอดข้อความ+เตรียมภาพ {t1 - t0:.1f}s | Gemini {t2 - t1:.1f}s | "
          f"รวม {time.time() - t0:.1f}s | ภาพแนบ {len(images)} | ได้ {len(questions)} ข้อ")

    return {
        "success": True,
        "files": [os.path.basename(n).split("_", 1)[-1] for n in names],
        "questions": questions,
    }

@app.get("/admin/chapters")
def list_chapters():
    conn = get_conn()
    try:
        with conn.cursor() as c:
            c.execute(
                """
                SELECT ch.id, ch.chapter_no, ch.title,
                       s.section_id, s.name AS section_name,
                       g.term
                FROM chapters ch
                JOIN sections s ON s.section_id = ch.section_id
                JOIN class_groups g ON g.id = s.class_group_id
                ORDER BY g.term, s.sort_order, ch.chapter_no
                """
            )
            rows = c.fetchall()
        return {"success": True, "data": rows}
    except Exception as e:
        return {"success": False, "error": f"Database Error: {str(e)}"}
    finally:
        conn.close()


@app.get("/admin/term-summary")
def term_summary():
    conn = get_conn()  # <- เปลี่ยนให้ตรงกับของจริง
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                  t.id_term,
                  t.term,
                  TRIM(SUBSTRING_INDEX(t.term,'/',-1)) AS year,
                  SUBSTRING_INDEX(TRIM(SUBSTRING_INDEX(t.term,'/',1)),' ',-1) AS sem,
                  m.day_sob AS midterm_date, m.start_sob_time AS midterm_start, m.end_sob_time AS midterm_end,
                  f.day_sob AS final_date,   f.start_sob_time AS final_start,   f.end_sob_time AS final_end,
                  (SELECT COUNT(*) FROM class_groups c WHERE c.term = t.term) AS group_count
                FROM term t
                LEFT JOIN term m ON TRIM(SUBSTRING_INDEX(m.term,'/',-1)) = TRIM(SUBSTRING_INDEX(t.term,'/',-1))
                                AND SUBSTRING_INDEX(TRIM(SUBSTRING_INDEX(m.term,'/',1)),' ',-1) = '1'
                LEFT JOIN term f ON TRIM(SUBSTRING_INDEX(f.term,'/',-1)) = TRIM(SUBSTRING_INDEX(t.term,'/',-1))
                                AND SUBSTRING_INDEX(TRIM(SUBSTRING_INDEX(f.term,'/',1)),' ',-1) = '2'
                ORDER BY year DESC, sem DESC
            """)
            rows = cur.fetchall()
        return {"success": True, "data": [
            {k: (str(v) if v is not None and k not in ("group_count", "id_term") else v) for k, v in r.items()}
            for r in rows
        ]}
    finally:
        conn.close()

@app.post("/auth/profile")
def update_profile(body: ProfileIn):
    id_student = body.id_student.strip()
    full_name = f"{body.name.strip()} {body.surname.strip()}".strip()
    if not id_student or not body.name.strip() or not body.surname.strip():
        return {"success": False, "error": "กรุณากรอกข้อมูลให้ครบ"}

    conn = get_conn()  # <- เปลี่ยนให้ตรงกับของจริง
    try:
        with conn.cursor() as cur:
            # รหัสนักศึกษาห้ามซ้ำกับคนอื่น
            cur.execute(
                "SELECT user_id FROM users WHERE id_student = %s AND user_id <> %s",
                (id_student, body.user_id),
            )
            if cur.fetchone():
                return {"success": False, "error": "รหัสนักศึกษานี้ถูกใช้แล้ว"}

            cur.execute(
                "UPDATE users SET id_student = %s, name = %s WHERE user_id = %s",
                (id_student, full_name, body.user_id),
            )
            if cur.rowcount == 0:
                return {"success": False, "error": "ไม่พบผู้ใช้"}
        conn.commit()
        return {"success": True, "id_student": id_student, "name": full_name}
    finally:
        conn.close()

@app.post("/admin/term-create")
def create_term(body: TermIn):
    if body.semester not in (1, 2):
        return {"success": False, "error": "เทอมต้องเป็น 1 หรือ 2"}
    if not (2500 <= body.year <= 2700):
        return {"success": False, "error": "ปีการศึกษาไม่ถูกต้อง"}
    if body.start_time >= body.end_time:
        return {"success": False, "error": "เวลาเริ่มต้องน้อยกว่าเวลาสิ้นสุด"}

    # รูปแบบต้องตรงกับข้อมูลเดิม: "เทอมที่ 1 / 2569"
    term_name = f"เทอมที่ {body.semester} / {body.year}"

    conn = get_conn()  # <- เปลี่ยนให้ตรงกับของจริง
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id_term FROM term WHERE term = %s", (term_name,))
            if cur.fetchone():
                return {"success": False, "error": f"{term_name} มีอยู่แล้ว"}
            cur.execute(
                """INSERT INTO term (term, day_sob, start_sob_time, end_sob_time, section)
                   VALUES (%s, %s, %s, %s, %s)""",
                (term_name, body.day_sob, body.start_time, body.end_time, body.semester),
            )
            new_term_id = cur.lastrowid
            cur.execute(
                """INSERT INTO sections (class_group_id, name, day_sob, start_sob_time, end_sob_time, sort_order, id_term)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (None, "กลางภาค" if body.semester == 1 else "ปลายภาค",
                 body.day_sob, body.start_time, body.end_time, body.semester, new_term_id),
            )
        conn.commit()
        return {"success": True, "term": term_name}
    finally:
        conn.close()

@app.get("/admin/term-chapters")
def term_chapters(id_term: int):
    conn = get_conn()  # <- เปลี่ยนให้ตรงกับของจริง
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT s.section_id, s.name, s.sort_order, s.id_term, t.term
                FROM sections s
                JOIN term t ON t.id_term = s.id_term
                WHERE s.id_term = %s
                ORDER BY s.sort_order
            """, (id_term,))
            sections = cur.fetchall()
        return {"success": True, "data": sections}
    finally:
        conn.close()


class ChapterIn(BaseModel):
    section_id: int
    title: str

@app.post("/admin/chapter-create")
def chapter_create(body: ChapterIn):
    title = body.title.strip()
    if not title:
        return {"success": False, "error": "กรุณากรอกชื่อบท"}
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COALESCE(MAX(chapter_no),0)+1 AS n FROM chapters WHERE section_id=%s", (body.section_id,))
            n = cur.fetchone()["n"]
            cur.execute(
                "INSERT INTO chapters (section_id, chapter_no, title) VALUES (%s,%s,%s)",
                (body.section_id, n, title),
            )
        conn.commit()
        return {"success": True, "chapter_no": n}
    finally:
        conn.close()

@app.delete("/admin/chapter-delete/{chapter_id}")
def chapter_delete(chapter_id: int):
    conn = get_conn()  # <- เปลี่ยนให้ตรงกับของจริง
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) AS n FROM quiz_questions WHERE chapter_id=%s", (chapter_id,))
            if cur.fetchone()["n"] > 0:
                return {"success": False, "error": "บทนี้มีข้อสอบอยู่ ลบไม่ได้"}
            cur.execute("DELETE FROM chapters WHERE id=%s", (chapter_id,))
        conn.commit()
        return {"success": True}
    finally:
        conn.close()

import os, re

SLIDE_DIR = "uploads/slides"
TRAIN_DIR = "uploads/trainAI"

@app.get("/admin/documents")
def list_documents():
    conn = get_conn()  # <- เปลี่ยนให้ตรงกับของจริง
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id_file, filename, created_at FROM trainpdf")
            train = cur.fetchall()
            cur.execute("SELECT slide_id, title, file_name, created_at FROM slides WHERE file_name IS NOT NULL AND file_name <> ''")
            slides = cur.fetchall()

        def size_of(folder, fn):
            p = os.path.join(folder, fn)
            return os.path.getsize(p) if os.path.isfile(p) else None

        data = []
        for r in train:
            fn = r["filename"]
            data.append({
                "key": f"train-{r['id_file']}",
                "source": "train",
                "id": r["id_file"],
                "display_name": re.sub(r"^[0-9a-f]{8}_", "", fn),  # ตัด prefix สุ่ม 8 ตัว
                "size": size_of(TRAIN_DIR, fn),
                "url": f"/uploads/trainAI/{fn}",
                "created_at": str(r["created_at"]),
            })
        for r in slides:
            fn = r["file_name"]
            data.append({
                "key": f"slide-{r['slide_id']}",
                "source": "slide",
                "id": r["slide_id"],
                "display_name": r["title"] or fn,
                "size": size_of(SLIDE_DIR, fn),
                "url": f"/uploads/slides/{fn}",
                "created_at": str(r["created_at"]),
            })
        data.sort(key=lambda x: x["created_at"], reverse=True)
        return {"success": True, "data": data}
    finally:
        conn.close()


@app.delete("/admin/documents/{source}/{doc_id}")
def delete_document(source: str, doc_id: int):
    if source not in ("train", "slide"):
        return {"success": False, "error": "ประเภทไม่ถูกต้อง"}
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            if source == "train":
                cur.execute("SELECT filename AS fn FROM trainpdf WHERE id_file=%s", (doc_id,))
                folder, table, key = TRAIN_DIR, "trainpdf", "id_file"
            else:
                cur.execute("SELECT file_name AS fn FROM slides WHERE slide_id=%s", (doc_id,))
                folder, table, key = SLIDE_DIR, "slides", "slide_id"
            row = cur.fetchone()
            if not row:
                return {"success": False, "error": "ไม่พบเอกสาร"}
            cur.execute(f"DELETE FROM {table} WHERE {key}=%s", (doc_id,))
        conn.commit()
        path = os.path.join(folder, row["fn"])
        if os.path.isfile(path):
            os.remove(path)
        return {"success": True}
    finally:
        conn.close()