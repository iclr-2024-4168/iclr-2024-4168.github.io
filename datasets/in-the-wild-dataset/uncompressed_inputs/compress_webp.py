import io
import os

from PIL import Image
from tqdm import tqdm


def compress_animated_webp(input_path, output_path, quality=80, method=4, frame_reduction_factor=1):
    # Open the animated WebP file
    with Image.open(input_path) as img:
        # Ensure it's an animated image
        if not getattr(img, "is_animated", False):
            raise ValueError("Input is not an animated image")

        # Get all frames
        frames = []
        durations = []
        for frame in tqdm(range(0, img.n_frames, frame_reduction_factor)):
            img.seek(frame)
            durations.append(img.info.get('duration', 100)
                             * frame_reduction_factor)
            frames.append(img.copy())

    # Adjust durations if we've reduced frames
    if frame_reduction_factor > 1:
        total_duration = sum(img.info.get('duration', 100)
                             for _ in range(img.n_frames))
        new_total_duration = sum(durations)
        duration_factor = total_duration / new_total_duration
        durations = [int(d * duration_factor) for d in durations]

    # Save the compressed animated WebP
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        format='WebP',
        quality=quality,
        method=method,
        lossless=False,
        exact=False
    )

    # Check file sizes
    input_size = os.path.getsize(input_path)
    output_size = os.path.getsize(output_path)

    print(f"Input file size: {input_size} bytes")
    print(f"Output file size: {output_size} bytes")
    print(f"Compression ratio: {output_size / input_size:.2f}")
    print(f"Frames reduced from {img.n_frames} to {len(frames)}")

    if output_size >= input_size:
        print("Warning: Compressed file is larger than or equal to the original.")
        print(
            "Consider adjusting quality, reducing more frames, or using the original file.")


# Set your parameters
quality = 80  # 0 to 100 (lowest to highest)
frame_reduction_factor = 8
size_threshold = 1024 * 1024  # 1 MB in bytes

# Get all .webp files in the current directory
files = [f for f in os.listdir(".") if f.endswith(".webp")]

# Process each file
for input_file in files:
    input_path = input_file
    output_path = f'../inputs/{input_file}'

    # Check if file size exceeds the threshold
    if os.path.getsize(input_path) > size_threshold and not (os.path.exists(output_path) and os.path.getsize(output_path) < size_threshold):
        print(f"Processing {input_file}...")
        compress_animated_webp(input_path, output_path, quality=quality,
                               method=4, frame_reduction_factor=frame_reduction_factor)
    # else:
    #     print(f"Skipping {input_file} (size below threshold)")
    #     # Optionally, copy the file to the output directory without compression
    #     import shutil
    #     shutil.copy2(input_path, output_path)
