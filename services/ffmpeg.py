import os
import subprocess


def extract_audio(input_video: str, output_audio: str):
    """
    input_video (例: "input.mp4")
    output_audio (例: "output.aac" や "output.mp3")
    """
    root, ext = os.path.splitext(input_video)
    print(ext)
    if ext == ".mov" or ext == ".MOV":
        output_video = f"{root}.mp4"
        command = [
            "ffmpeg",
            "-i",
            input_video,
            # コーデック指定 (再エンコード例)
            "-c:v",
            "libx264",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            output_video,
        ]
        subprocess.run(command, check=True)
        input_video = output_video
    command = [
        "ffmpeg",
        "-i",
        input_video,
        "-vn",
        "-acodec",
        "libmp3lame",
        "-q:a",
        "2",
        output_audio,
    ]
    subprocess.run(command, check=True)


# 実行例
if __name__ == "__main__":
    # 拡張子を .mp3 にする
    extract_audio(
        "/app/assets/tmp/test.mp4",
        "/app/assets/tmp/test.mp3",
    )
