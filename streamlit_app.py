import streamlit as st
import pyshorteners
import qrcode
from PIL import Image
from io import BytesIO

# URL을 줄이는 함수
def shorten_url(long_url):
    s = pyshorteners.Shortener()
    try:
        short_url = s.tinyurl.short(long_url)
        return short_url
    except Exception as e:
        return "Error: URL shortening failed."

# QR 코드를 생성하는 함수
def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    # 이미지를 메모리 버퍼에 저장
    img = qr.make_image(fill="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

# Streamlit 앱 UI
st.title("URL Shortener with QR Code")

# 사용자에게 URL 입력 받기
url = st.text_input("Enter the URL you want to shorten:")

# URL 입력을 받은 후 처리
if st.button("Shorten URL and Generate QR Code"):
    if url:
        # URL 줄이기
        shortened_url = shorten_url(url)
        if "Error" not in shortened_url:
            st.success(f"Shortened URL: {shortened_url}")
            
            # QR 코드 생성
            qr_image = generate_qr_code(shortened_url)
            img = Image.open(qr_image)
            
            # QR 코드 이미지 보여주기
            st.image(img, caption="QR Code for the shortened URL")
        else:
            st.error(shortened_url)
    else:
        st.error("Please enter a valid URL.")
