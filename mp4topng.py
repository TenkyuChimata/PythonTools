import cv2
import os

def extract_frames(video_path, output_folder, frame_interval=30):
    """
    从MP4视频中每隔 frame_interval 帧提取一张图片并保存为 PNG
    :param video_path: 视频文件路径
    :param output_folder: 保存图片的文件夹
    :param frame_interval: 每隔多少帧保存一次
    """
    # 确保输出文件夹存在喵～
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 打开视频文件
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("无法打开视频文件喵～")
        return

    frame_count = 0  # 记录总帧数
    saved_count = 0  # 记录保存的图片数

    while True:
        ret, frame = cap.read()
        if not ret:
            break  # 读取失败或者结束就退出喵～

        if frame_count % frame_interval == 0:
            img_path = os.path.join(output_folder, f"frame_{frame_count:06d}.png")
            cv2.imwrite(img_path, frame)
            saved_count += 1
            print(f"保存帧 {frame_count} 为 {img_path} 喵～")

        frame_count += 1

    cap.release()
    print(f"提取完成，共保存 {saved_count} 张图片喵！ฅ^•ﻌ•^ฅ")

# 使用示例：
video_file = "input.mp4"  # 这里换成你的视频文件喵～
output_dir = "frames_output"  # 这里是保存的文件夹喵～
frame_interval = 5

extract_frames(video_file, output_dir, frame_interval)
