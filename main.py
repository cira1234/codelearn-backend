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

app = FastAPI()
load_dotenv()



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