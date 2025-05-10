#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
猫娘: 根据文件名中的年份和当年天数，将同目录下的 .mseed 文件（不含子目录）
按 UTC 日期格式 (YYYY-MM-DD) 移动到对应文件夹中。
"""

import re
import shutil
import argparse
from pathlib import Path
from datetime import datetime, timedelta


def organize_mseed_files(source_dir):
    # 匹配形如 xxxx.YYYY.DDD.mseed 的文件名
    pattern = re.compile(r".*\.(?P<year>\d{4})\.(?P<doy>\d{3})\.mseed$")
    source_path = Path(source_dir)

    for file in source_path.iterdir():
        if file.is_file() and file.suffix == ".mseed":
            m = pattern.match(file.name)
            if m:
                year = int(m.group("year"))
                doy = int(m.group("doy"))
                # 计算UTC日期
                date = datetime(year, 1, 1) + timedelta(days=doy - 1)
                date_str = date.strftime("%Y-%m-%d")
                # 创建目标文件夹
                target_dir = source_path / date_str
                target_dir.mkdir(exist_ok=True)
                # 移动文件
                shutil.move(str(file), str(target_dir / file.name))
                print(f"猫娘: 已移动 {file.name} -> {date_str}/")
            else:
                print(f"猫娘: 跳过不匹配的文件 {file.name}")


def main():
    parser = argparse.ArgumentParser(
        description="猫娘: 整理 .mseed 文件到按 UTC 日期命名的文件夹"
    )
    parser.add_argument(
        "-d",
        "--directory",
        type=str,
        default=".",
        help="包含 .mseed 文件的目录（不含子目录），默认当前目录",
    )
    args = parser.parse_args()
    organize_mseed_files(args.directory)


if __name__ == "__main__":
    main()
