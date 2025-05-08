#!/usr/bin/env python3
"""
脚本：merge_seis_records.py
用途：将旧 SQLite 数据库（sqlite_v4_old.db）中所有 as_seis_records_x 表的记录合并到新数据库（sqlite_v4.db）对应的表中。
注意：不会处理 as_sys_users 和 as_user_settings 表。
用法：
    python merge_seis_records.py sqlite_v4_old.db sqlite_v4.db
"""
import sqlite3
import sys

def merge_records(old_db_path, new_db_path):
    # 连接旧数据库和新数据库
    old_conn = sqlite3.connect(old_db_path)
    new_conn = sqlite3.connect(new_db_path)
    old_cur = old_conn.cursor()
    new_cur = new_conn.cursor()

    # 获取所有 as_seis_records_x 表名，排除用户设置表
    old_cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'as_seis_records_%'"
    )
    tables = [row[0] for row in old_cur.fetchall()]

    for table in tables:
        print(f"Processing table {table}...")

        # 获取旧表的列信息
        old_cur.execute(f"PRAGMA table_info({table})")
        cols = [info[1] for info in old_cur.fetchall()]

        # 选择 timestamp 或 record_time 作为新表的 record_time
        if 'timestamp' in cols:
            time_col = 'timestamp'
        elif 'record_time' in cols:
            time_col = 'record_time'
        else:
            print(f"  Skipping {table}: no timestamp or record_time column")
            continue

        # 判断 created_at 列是否存在
        if 'created_at' in cols:
            created_col = 'created_at'
        else:
            created_col = 'NULL'

        # 查询旧表数据
        try:
            old_cur.execute(
                f"SELECT {created_col}, {time_col}, sample_rate, channel_data FROM {table}"
            )
            rows = old_cur.fetchall()
        except sqlite3.OperationalError as e:
            print(f"  Skipping {table}: {e}")
            continue

        # 插入到新表
        for created_at, record_time, sample_rate, channel_data in rows:
            try:
                new_cur.execute(
                    f"INSERT OR IGNORE INTO {table} (created_at, record_time, sample_rate, channel_data)"
                    " VALUES (?, ?, ?, ?)",
                    (created_at, record_time, sample_rate, channel_data)
                )
            except sqlite3.Error as e:
                print(f"  Error inserting into {table}: {e}")

        new_conn.commit()

    # 关闭连接
    old_conn.close()
    new_conn.close()

if name == 'main':
    if len(sys.argv) != 3:
        print("Usage: python merge_seis_records.py <old_db_path> <new_db_path>")
        sys.exit(1)
    merge_records(sys.argv[1], sys.argv[2])
