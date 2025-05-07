import os

# 获取用户输入的搜索内容
search_text = input("请输入你想查找的文字内容喵～：")

# 存放匹配到的文件名
matched_files = []

# 设定目录和文件范围
articles_dir = "articles"
start_num = 1
end_num = 355

# 遍历文件
for i in range(start_num, end_num + 1):
    filename = f"{i}.md"
    filepath = os.path.join(articles_dir, filename)

    # 如果文件存在就打开看看
    if os.path.isfile(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            if search_text in content:
                matched_files.append(filename)

# 输出结果
if matched_files:
    print("找到包含该文字内容的文件有喵～：")
    for fname in matched_files:
        print(fname)
else:
    print("喵呜，没有找到包含这个内容的文件喵～")
