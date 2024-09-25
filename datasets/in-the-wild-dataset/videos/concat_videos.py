from moviepy.editor import VideoFileClip, CompositeVideoClip, vfx
import os
from moviepy.editor import VideoFileClip, clips_array, vfx


def adjust_clip_speed(clip, target_duration):
    """Adjust the speed of a clip to match the target duration."""
    speed_factor = clip.duration / target_duration
    return clip.speedx(speed_factor)


def create_video_grid(input_files, output_file, ncols, nrows, strategy='shortest'):
    # Load all video clips
    clips = [VideoFileClip(f).resize(width=640)
             for f in input_files]  # Resize for consistency

    if strategy == 'longest':
        target_duration = max(clip.duration for clip in clips)
    elif strategy == 'shortest':
        target_duration = min(clip.duration for clip in clips)
    else:
        raise ValueError("Invalid strategy. Choose 'longest' or 'shortest'.")

    print("Target duration:", target_duration)
    # Adjust clip speeds
    adjusted_clips = [adjust_clip_speed(
        clip, target_duration) for clip in clips]

    # Ensure we have enough clips to fill the grid
    num_clips = ncols * nrows
    if len(adjusted_clips) < num_clips:
        # Create a blank clip to fill empty spaces
        blank_clip = VideoFileClip(
            "path/to/blank_video.mp4").resize(width=640).fx(vfx.loop, duration=target_duration)
        adjusted_clips.extend([blank_clip] * (num_clips - len(adjusted_clips)))
    elif len(adjusted_clips) > num_clips:
        # Truncate the list if we have too many clips
        adjusted_clips = adjusted_clips[:num_clips]

    # Create a 2D list representing the grid
    grid = [adjusted_clips[i:i+ncols]
            for i in range(0, len(adjusted_clips), ncols)]

    # Create the final composition
    final_clip = clips_array(grid)

    # Write the output file
    final_clip.write_videofile(output_file, codec="libx264")

    # Close all clips
    for clip in clips + adjusted_clips:
        clip.close()
    final_clip.close()


def resize_clip(clip, target_width, target_height):
    """
    Resize a clip to fit within the target dimensions while maintaining aspect ratio.
    If necessary, add black bars to fill the target dimensions.
    """
    target_aspect = target_width / target_height
    clip_aspect = clip.w / clip.h

    if clip_aspect > target_aspect:
        new_width = target_width
        new_height = int(target_width / clip_aspect)
    else:
        new_height = target_height
        new_width = int(target_height * clip_aspect)

    resized_clip = clip.resize((new_width, new_height))
    bg = CompositeVideoClip([resized_clip.set_position('center')],
                            size=(target_width, target_height))
    return bg


def adjust_clip_speed(clip, target_duration):
    """Adjust the speed of a clip to match the target duration."""
    speed_factor = clip.duration / target_duration
    return clip.speedx(factor=speed_factor)


def create_video_grid_with_zoom(input_files, output_file, ncols=5, nrows=3,
                                strategy='shortest', target_width=3200, target_height=3456):
    # Load all video clips and resize them
    clips = [VideoFileClip(f) for f in input_files]
    cell_width = target_width // ncols
    cell_height = target_height // nrows
    clips = [resize_clip(clip, cell_width, cell_height) for clip in clips]

    if strategy == 'longest':
        target_duration = max(clip.duration for clip in clips)
    elif strategy == 'shortest':
        target_duration = min(clip.duration for clip in clips)
    else:
        raise ValueError("Invalid strategy. Choose 'longest' or 'shortest'.")

    # Adjust clip speeds
    adjusted_clips = [adjust_clip_speed(
        clip, target_duration) for clip in clips]

    # Ensure we have enough clips to fill the grid
    num_clips = ncols * nrows
    if len(adjusted_clips) < num_clips:
        blank_clip = CompositeVideoClip(
            [], size=(cell_width, cell_height), duration=target_duration)
        adjusted_clips.extend([blank_clip] * (num_clips - len(adjusted_clips)))
    elif len(adjusted_clips) > num_clips:
        adjusted_clips = adjusted_clips[:num_clips]

    # Create the grid composition
    clips_with_positions = []
    for i, clip in enumerate(adjusted_clips):
        row = i // ncols
        col = i % ncols
        x_position = col * cell_width
        y_position = row * cell_height
        clips_with_positions.append(
            clip.set_position((x_position, y_position)))

    grid_clip = CompositeVideoClip(
        clips_with_positions, size=(target_width, target_height))

    # Create the zoom effect
    # Middle clip (row 2, column 3)
    center_clip = adjusted_clips[ncols + ncols//2]
    center_clip_fullscreen = center_clip.resize(height=target_height,
                                                width=target_width)

    def zoom(t):
        progress = t / target_duration
        scale = 1 + (target_width / center_clip_fullscreen.w -
                     1) * (1 - progress)
        return scale

    def move(t):
        progress = t / target_duration
        start_x = target_width/2 - center_clip_fullscreen.w/2
        start_y = target_height/2 - center_clip_fullscreen.h/2
        end_x = (ncols//2) * cell_width
        end_y = (nrows//2) * cell_height
        x = start_x + (end_x - start_x) * progress
        y = start_y + (end_y - start_y) * progress
        return (x, y)

    zoomed_clip = center_clip_fullscreen.resize(
        lambda t: zoom(t)).set_position(move)

    final_clip = CompositeVideoClip([grid_clip, zoomed_clip])

    # Write the output file
    final_clip.write_videofile(output_file, codec="libx264")

    # Close all clips
    for clip in clips + adjusted_clips:
        clip.close()
    final_clip.close()


def main():
    # Example usage
    # output_file = "pred_grid_video.mp4"
    output_file = "grid_zoom_video.mp4"
    ncols = 5  # Number of columns in the grid
    nrows = 3  # Number of rows in the grid

    # # Get all MP4 files from the input directory
    # # input_directory = "path/to/input/directory"
    # input_files = [os.path.join(input_directory, f) for f in os.listdir(
    #     input_directory) if f.endswith('.mp4')]
    input_dir = "cropped_videos"
    input_files = [
        "aug_box.mp4",
        "aug_simple_drawer.mp4",
        "aug_microwave.mp4",
        "aug_door.mp4",
        "aug_laptop.mp4",
        "aug_chair.mp4",
        "aug_oven.mp4",
        "aug_lab_toilet.mp4",
        "aug_washing_machine.mp4",
        "aug_fridge.mp4",
        "aug_door.mp4",
        "aug_monitor.mp4",
        "aug_kitchen_pot.mp4",
        "aug_dishwasher.mp4",
        "aug_suitcase.mp4",
    ]
    input_files = [os.path.join(input_dir, "pred_" + f) for f in input_files]

    # Sort the files to ensure consistent ordering
    # input_files.sort()

    # Create the video grid
    # create_video_grid(input_files, output_file, ncols, nrows)
    create_video_grid_with_zoom(input_files, output_file, ncols, nrows)

    print(f"Grid video created: {output_file}")


if __name__ == "__main__":
    main()
