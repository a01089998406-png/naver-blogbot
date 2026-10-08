import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google import genai

# Secrets 설정값 불러오기
API_KEY = os.environ.get("OPENAI_API_KEY")
NAVER_EMAIL = os.environ.get("NAVER_EMAIL")
NAVER_PASSWORD = os.environ.get("NAVER_PASSWORD")

def generate_blog_post():
    client = genai.Client(api_key=API_KEY)
    prompt = "네이버 블로그에 포스팅할 만한 매력적이고 유익한 글 1편을 작성해줘."
    
    # 올바른 최신 모델 지정
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return response.text

def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = NAVER_EMAIL
    msg['To'] = NAVER_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    server = smtplib.SMTP_SSL('smtp.naver.com', 465)
    server.login(NAVER_EMAIL, NAVER_PASSWORD)
    server.sendmail(NAVER_EMAIL, NAVER_EMAIL, msg.as_string())
    server.quit()

if __name__ == "__main__":
    blog_content = generate_blog_post()
    send_email("[오늘의 블로그 자동 생성 원고]", blog_content)
    print("발송 완료!")
