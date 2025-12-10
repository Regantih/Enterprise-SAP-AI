from moviepy import *
import os

# Load assets
scenes = []
for i in range(1, 6):
    audio_path = f"assets/scene_{i}.mp3"
    image_path = f"assets/scene_{i}.png"
    
    # Create audio clip
    audio_clip = AudioFileClip(audio_path)
    duration = audio_clip.duration + 0.5 # Add padding
    
    # Create image clip
    img_clip = ImageClip(image_path).with_duration(duration)
    
    # Set audio
    video_clip = img_clip.with_audio(audio_clip)
    
    # Add fade in/out
    video_clip = video_clip.with_effects([vfx.FadeIn(0.5), vfx.FadeOut(0.5)])
    
    scenes.append(video_clip)

# Concatenate all clips
final_video = concatenate_videoclips(scenes, method="compose")

# Write output
final_video.write_videofile("miraitec_promo.mp4", fps=24)
print("Video generated: miraitec_promo.mp4")
