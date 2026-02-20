"""
QR코드 생성 스크립트
사용법: python gen_qr.py [URL]
URL이 없으면 GitHub Pages 기본 URL 사용
"""
import sys
import subprocess

def install_and_import(package):
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

install_and_import('qrcode')
install_and_import('PIL')

import qrcode
from PIL import Image, ImageDraw, ImageFont
import os

# ── 설정 ──────────────────────────────────────
# GitHub Pages URL (저장소 만든 후 이 값을 업데이트하세요)
DEFAULT_URL = "https://kjs40404040-lgtm.github.io/wedding-invitation"

url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL

print(f"🔗 QR코드 생성 URL: {url}")

# ── QR코드 생성 ───────────────────────────────
qr = qrcode.QRCode(
    version=3,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)
qr.add_data(url)
qr.make(fit=True)

# 골드 컬러 QR코드
img = qr.make_image(fill_color="#5c3d2e", back_color="#fdf8f2")
img = img.convert("RGB")

# 크기 조정
img = img.resize((400, 400), Image.LANCZOS)

# 테두리 추가 (골드)
bordered = Image.new("RGB", (440, 480), "#fdf8f2")
bordered.paste(img, (20, 20))

# 텍스트 추가
draw = ImageDraw.Draw(bordered)
try:
    font_title = ImageFont.truetype("C:/Windows/Fonts/malgun.ttf", 18)
    font_sub   = ImageFont.truetype("C:/Windows/Fonts/malgun.ttf", 13)
except:
    font_title = ImageFont.load_default()
    font_sub   = ImageFont.load_default()

draw.text((220, 432), "📱 스캔하여 청첩장 보기", fill="#c9a96e", font=font_title, anchor="mm")
draw.text((220, 460), url[:45] + ('…' if len(url) > 45 else ''), fill="#7a6a5a", font=font_sub, anchor="mm")

# 골드 테두리선
draw.rectangle([10, 10, 429, 469], outline="#c9a96e", width=2)

# 저장
output_path = os.path.join(os.path.dirname(__file__), "wedding_qr.png")
bordered.save(output_path, "PNG", dpi=(300, 300))

print(f"✅ QR코드 저장 완료: {output_path}")
print("📌 바탕화면에도 복사합니다...")

import shutil
desktop_path = os.path.join(os.environ.get('USERPROFILE', ''), 'OneDrive', '바탕 화면', 'wedding_qr.png')
try:
    shutil.copy2(output_path, desktop_path)
    print(f"✅ 바탕화면 저장: {desktop_path}")
except:
    print("⚠️ 바탕화면 복사 실패 (파일은 프로젝트 폴더에 있습니다)")
