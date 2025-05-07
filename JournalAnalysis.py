import json
from collections import defaultdict

def calculate_total_doses(json_path):
    # 读取 JSON 数据
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 用于累计剂量的字典
    totals = defaultdict(float)
    # 用于记录每种药物对应的单位（假设同一种药物单位一致）
    units = {}

    # 遍历每一次“experiences”
    for experience in data.get('experiences', []):
        # 对每一次的“ingestions”列表
        for ingestion in experience.get('ingestions', []):
            name = ingestion.get('substanceName')
            dose = ingestion.get('dose', 0)
            unit = ingestion.get('units', '')

            # 累加剂量
            totals[name] += dose
            # 记录单位
            units[name] = unit

    # 返回统计结果
    return {name: f"{totals[name]} {units[name]}" for name in totals}

if __name__ == "__main__":
    json_file = "Journal 29 Apr 2025.json"  # 请根据实际路径修改
    results = calculate_total_doses(json_file)
    for substance, total in results.items():
        print(f"{substance}: {total}")
