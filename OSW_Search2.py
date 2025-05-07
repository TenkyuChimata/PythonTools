import os

# 获取用户输入的关键词1和关键词2
keyword1 = input("请输入第一个你想查找的关键词喵～：")
keyword2 = input("请输入第二个你想查找的关键词喵～：")

# 存放匹配到关键词1和关键词2的文件名
matched_files_stage1 = []
matched_files_stage2 = []

# 设定目录和文件范围
articles_dir = "articles"
start_num = 1
end_num = 355

# 第一次遍历：查找包含关键词1的文件
for i in range(start_num, end_num + 1):
    filename = f"{i}.md"
    filepath = os.path.join(articles_dir, filename)

    if os.path.isfile(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            if keyword1 in content:
                matched_files_stage1.append((filename, content))  # 顺便存下内容喵～

# 第二次筛选：在包含关键词1的文件中查找关键词2
for fname, content in matched_files_stage1:
    if keyword2 in content:
        matched_files_stage2.append(fname)

# 输出结果
if matched_files_stage2:
    print("喵呜～找到同时包含两个关键词的文件如下喵～：")
    for fname in matched_files_stage2:
        print(fname)
else:
    print("呜呜，没有找到同时包含这两个关键词的文件喵～")
