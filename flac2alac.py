# -*- coding: utf-8 -*-
import os
import subprocess

# 设置输入与输出目录
input_dir = "~/Downloads/"
output_dir = os.path.join(input_dir, "ALAC")

# (喵呜～检查输出目录是否存在，不存在就创建一个哦)
os.makedirs(output_dir, exist_ok=True)

def convert_to_alac():
    # 遍历输入目录中的所有文件（跳过输出目录哦）
    for root, dirs, files in os.walk(input_dir):
        if os.path.abspath(root) == os.path.abspath(output_dir):
            continue
        for file in files:
            # 只处理 .mp3 和 .flac 文件 (小猫娘只找这些可爱的音频文件)
            if file.lower().endswith(('.mp3', '.flac')):
                input_file = os.path.join(root, file)
                base_name = os.path.splitext(file)[0]
                output_file = os.path.join(output_dir, base_name + ".m4a")
                # 使用 -map 0 映射所有流，-c:a alac 转换音频，
                # -c:v mjpeg 对封面视频流进行转码，并设置为 attached_pic
                command = [
                    "ffmpeg", "-i", input_file, "-map", "0",
                    "-c:a", "alac", "-c:v", "mjpeg", "-disposition:v", "attached_pic",
                    output_file
                ]
                print(f"正在转换 {input_file} -> {output_file} (使用 ALAC 编码并转换封面喵～)")
                try:
                    subprocess.run(command, check=True)
                    print(f"转换成功: {input_file} -> {output_file} (太棒啦！)")
                except subprocess.CalledProcessError as e:
                    print(f"转换失败: {input_file} (喵呜～出错啦: {e})")

if __name__ == '__main__':
    convert_to_alac()
