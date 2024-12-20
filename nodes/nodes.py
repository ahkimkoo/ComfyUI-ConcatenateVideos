import os
import subprocess
import tempfile
import random
import time
import folder_paths

class ConcatenateVideos:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video_urls": ("STRING", {"multiline": True, "default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "concatenate_videos"
    CATEGORY = "🧩 Videos Nodes"

    def concatenate_videos(self, video_urls):
        # 将输入的多行字符串分割成视频网址列表
        urls = video_urls.strip().split("\n")

        # 检查是否有视频网址
        if not urls or len(urls) < 1:
            raise ValueError("至少需要一个视频网址进行合并。")

        # 创建一个临时目录来存储下载的视频
        with tempfile.TemporaryDirectory() as temp_dir:
            local_files = []

            # 下载每个视频
            for url in urls:
                timestamp = int(time.time())
                random_number = random.randint(1000, 9999)
                local_file_name = f"video_{timestamp}_{random_number}.mp4"
                local_file_path = os.path.join(temp_dir, local_file_name)
                download_command = ["ffmpeg", "-i", url, "-c", "copy", local_file_path]
                try:
                    subprocess.run(download_command, check=True)
                    local_files.append(local_file_path)
                except subprocess.CalledProcessError as e:
                    raise RuntimeError(f"下载视频失败: {e}")

            # 生成 input.txt 文件名：当前时间戳 + 随机数
            timestamp = int(time.time())
            random_number = random.randint(1000, 9999)
            input_file_name = f"input_{timestamp}_{random_number}.txt"
            temp_input_file_path = os.path.join(temp_dir, input_file_name)

            # 在临时目录下创建一个文件来存储视频文件路径
            with open(temp_input_file_path, 'w') as f:
                for local_file in local_files:
                    f.write(f"file '{local_file}'\n")

            # 生成输出文件名：当前时间戳 + 随机数
            timestamp = int(time.time())
            random_number = random.randint(1000, 9999)
            output_file_name = f"merged_video_{timestamp}_{random_number}.mp4"
            output_file_path = os.path.join(folder_paths.get_output_directory(), output_file_name)

            # FFmpeg 命令，用于合并视频
            ffmpeg_command = [
                "ffmpeg",
                "-f", "concat",
                "-safe", "0",
                "-i", temp_input_file_path,
                "-c", "copy",
                output_file_path
            ]

            # 执行 FFmpeg 命令
            try:
                subprocess.run(ffmpeg_command, check=True)
            except subprocess.CalledProcessError as e:
                raise RuntimeError(f"FFmpeg 执行失败: {e}")

            # 返回输出文件名（不包括路径）
            return (output_file_name,)
