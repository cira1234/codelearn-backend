import os, secrets, hashlib, hmac, smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from fastapi import FastAPI
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

app = FastAPI()
load_dotenv()
   
app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ],
        allow_credentials=False,
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
@app.post("/useai")
async def use_ai(data: dict):
        # รับ Error ดิบที่ Flutter เก็บไว้ ส่งมาให้เส้นนี้
        raw_error = data.get("error", "")
        code = data.get("code", "") # (Optional) รับโค้ดมาด้วยเพื่อให้ AI เข้าใจบริบทมากขึ้น

        if not raw_error:
            return {"ai_explanation": "ไม่พบข้อความ Error สำหรับวิเคราะห์"}

        try:
            # สามารถใส่โค้ดเข้าไปใน Prompt ด้วยเพื่อให้ AI บอกบรรทัดที่ผิดได้แม่นยำขึ้น
            ai_prompt = f"ช่วยอธิบาย C++ Error ต่อไปนี้เป็นภาษาไทยให้กระชับ สั้นๆ เข้าใจง่าย พร้อมบอกวิธีแก้:\n\nError:\n{raw_error}"
            if code:
                ai_prompt += f"\n\nCode:\n{code}"

            ai_response = ollama.chat(
                model="gemma3:4b",
                messages=[{"role": "user", "content": ai_prompt}],
                stream=False,
                options={
                    "num_predict": 150,  # บังคับให้ตอบไม่เกิน ~150 tokens (ประมาณ 3-4 บรรทัด)
                    "temperature": 0.2   # ลดความ Creative ลง ทำให้ AI คิดคำตอบที่ตรงไปตรงมาได้เร็วขึ้น
                }
            )
            ai_explanation = ai_response["message"]["content"]
            
            return {
                "success": True,
                "ai_explanation": ai_explanation
            }
        except Exception as e:
            return {
                "success": False,
                "ai_explanation": f"ไม่สามารถดึงคำอธิบายจาก AI ได้ (ระบบอาจมีปัญหา): {str(e)}"
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
    print("SMTP_USER =", repr(SMTP_USER), "| pw length =", len(SMTP_APP_PASSWORD))
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
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=15) as s:
        s.starttls()
        s.login(SMTP_USER, SMTP_APP_PASSWORD)
        s.send_message(msg)

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
            cursor.execute("SELECT id FROM users WHERE google_id = %s", (google_id,))
            user_id = cursor.fetchone()["id"]

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
def otp_verify(data: dict):
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

            c.execute("SELECT * FROM users WHERE id = %s", (row["user_id"],))
            user = c.fetchone()
            c.execute("DELETE FROM otp_codes WHERE id = %s", (row["id"],))  # ใช้ได้ครั้งเดียว
            conn.commit()
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
                   JOIN users u ON u.id = o.user_id
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