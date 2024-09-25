import os
import subprocess
from moviepy.editor import VideoFileClip


def crop_video(input_file, output_file, target_width, target_height):
    # Load the video clip
    clip = VideoFileClip(input_file)

    # Get the original dimensions
    width, height = clip.w, clip.h

    # Calculate the cropping coordinates
    x1 = (width - target_width) // 2
    y1 = (height - target_height) // 2
    x2 = x1 + target_width
    y2 = y1 + target_height

    # Crop the video
    cropped_clip = clip.crop(x1=x1, y1=y1, x2=x2, y2=y2)

    # Write the output file
    cropped_clip.write_videofile(output_file, codec="libx264")

    # Close the clips
    clip.close()
    cropped_clip.close()


def process_directory(input_dir, output_dir, target_width, target_height):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Process all .mp4 files in the input directory
    for filename in os.listdir(input_dir):
        # if filename.endswith(".mp4") and filename.startswith("aug"):
        if filename.endswith(".mp4") and filename.startswith("pred"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, f"{filename}")
            if os.path.exists(output_path):
                continue
            crop_video(input_path, output_path, target_width, target_height)
            print(f"Processed: {filename}")


input_file = "pred_aug_fridge.mp4"
output_file = f"cropped_videos/{input_file}"
target_width = 640  # Adjust as needed
target_height = 480  # Adjust as needed
# crop_video(input_file, output_file, target_width, target_height)

process_directory(".", "cropped_videos",
                  target_width, target_height)
