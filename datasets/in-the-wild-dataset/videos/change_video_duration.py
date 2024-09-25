import os
from moviepy.editor import VideoFileClip, clips_array, vfx


# file_path = "cropped_videos/aug_lab_toilet.mp4"
file_path = "pred_grid_video.mp4"
clip = VideoFileClip(file_path)
final_duration = 2  # seconds
clip = clip.speedx(final_duration=final_duration)

output_file = f"duration_adjusted_video/{os.path.basename(file_path)}"
clip.write_videofile(output_file, codec="libx264")
