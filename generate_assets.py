import os
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import random

# Ensure assets directory exists
os.makedirs("assets", exist_ok=True)

# Script Data
scenes = [
    {
        "text": "MIRAI. Contactless Health Monitoring for Seniors. Where seniors' independence meets family peace of mind.",
        "filename": "scene_1",
        "bg_color": (40, 60, 100), # Calming Blue
        "text_color": (255, 255, 255)
    },
    {
        "text": "Wellbeing made simple.",
        "filename": "scene_2",
        "bg_color": (240, 240, 240), # Clean White
        "text_color": (40, 60, 100)
    },
    {
        "text": "MIRAI detects vital signs, falls, and environmental conditions.",
        "filename": "scene_3",
        "bg_color": (40, 100, 60), # Safety Green tone
        "text_color": (255, 255, 255)
    },
    {
        "text": "Timely intervention for seniors living alone. Peace of mind for caregivers.",
        "filename": "scene_4",
        "bg_color": (100, 40, 40), # Alert/Care tone (warm)
        "text_color": (255, 255, 255)
    },
    {
        "text": "Independence. Privacy. Safety. MIRAI.",
        "filename": "scene_5",
        "bg_color": (255, 255, 255),
        "text_color": (0, 0, 0)
    }
]

def create_image(text, filename, bg_color, text_color):
    img = Image.new('RGB', (1920, 1080), color=bg_color)
    d = ImageDraw.Draw(img)
    
    # Try to load a font, fallback to default
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
    except:
        font = ImageFont.load_default()

    # Text wrapping (simple)
    margin = 100
    offset = 400
    for line in text.split('. '):
        d.text((margin, offset), line, font=font, fill=text_color)
        offset += 100
        
    img.save(f"assets/{filename}.png")
    print(f"Generated image: assets/{filename}.png")

def create_audio(text, filename):
    tts = gTTS(text=text, lang='en')
    tts.save(f"assets/{filename}.mp3")
    print(f"Generated audio: assets/{filename}.mp3")

for scene in scenes:
    create_image(scene["text"], scene["filename"], scene["bg_color"], scene["text_color"])
    create_audio(scene["text"], scene["filename"])

print("Asset generation complete.")
