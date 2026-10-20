import os, smtplib

user = os.environ.get("SMTP_USER", "")
pw = os.environ.get("SMTP_APP_PASSWORD", "")
print("USER:", repr(user), "| PASSWORD length:", len(pw))

# ทดสอบพอร์ต 587 (STARTTLS)
try:
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=15) as s:
        s.starttls()
        s.login(user, pw)
    print("587 OK")
except Exception as e:
    print("587 FAIL:", repr(e))

# ทดสอบพอร์ต 465 (SSL)
try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=15) as s:
        s.login(user, pw)
    print("465 OK")
except Exception as e:
    print("465 FAIL:", repr(e))