import argparse
from typing import List, Tuple

import pysrt
from moviepy.editor import CompositeVideoClip, TextClip, VideoFileClip


def time_to_seconds(time_obj: pysrt.srttime.SubRipTime) -> float:
    return (
        time_obj.hours * 3600
        + time_obj.minutes * 60
        + time_obj.seconds
        + time_obj.milliseconds / 1000
    )


def create_subtitle_clips(
    subtitles: List[pysrt.srttime.SubRipTime],
    videosize: List[int],
    fontsize: int = 24,
    font: str = "Arial",
    color: str = "white",
    debug: bool = False,
) -> List[TextClip]:
    subtitle_clips = []

    for subtitle in subtitles:
        start_time: float = time_to_seconds(subtitle.start)
        end_time: float = time_to_seconds(subtitle.end)
        duration: float = end_time - start_time

        video_width, video_height = videosize

        text_clip: TextClip = (
            TextClip(
                subtitle.text,
                fontsize=fontsize,
                font=font,
                color=color,
                bg_color="black",
                size=(video_width * 3 / 4, None),
                method="caption",
            )
            .set_start(start_time)
            .set_duration(duration)
        )

        subtitle_x_position: str = "center"
        subtitle_y_position: float = video_height * 4 / 5
        text_position: Tuple[str, float] = (subtitle_x_position, subtitle_y_position)

        subtitle_clips.append(text_clip.set_position(text_position))

    return subtitle_clips


def add_subtitle_to_movie(mp4filename: str, srtfilename) -> CompositeVideoClip:
    print("Video path:", mp4filename)
    print("Subtitle path:", srtfilename)
    video: VideoFileClip = VideoFileClip(mp4filename)
    subtitles: List[pysrt.srttime.SubRipTime] = pysrt.open(srtfilename)

    begin, _ = mp4filename.split(".mp4")
    output_video_file: str = begin + "_subtitled" + ".mp4"

    subtitle_clips: List[TextClip] = create_subtitle_clips(subtitles, video.size)

    final_video: CompositeVideoClip = CompositeVideoClip([video] + subtitle_clips)
    final_video.write_videofile(output_video_file)

    return final_video


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("--mp4_path", type=str, required=True)
    parser.add_argument("--srt_path", type=str, required=True)
    args: argparse.Namespace = parser.parse_args()

    add_subtitle_to_movie(mp4filename=args.mp4_path, srtfilename=args.srt_path)
