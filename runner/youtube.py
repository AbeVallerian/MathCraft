import argparse

from pytubefix import YouTube
from pytubefix.cli import on_progress


def download_youtube(url: str, output_path: str) -> None:
    yt: YouTube = YouTube(url, on_progress_callback=on_progress)
    print("Youtube title :", yt.title)

    ys = yt.streams.get_highest_resolution()
    ys.download(output_path=output_path)
    print("Download completed")


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("--url", type=str, required=True)
    parser.add_argument(
        "--output_path", type=str, default="/Users/abevallerian/Downloads"
    )
    args: argparse.Namespace = parser.parse_args()

    print("Downloading from", args.url)
    print("Saving to", args.output_path)
    download_youtube(url=args.url, output_path=args.output_path)
