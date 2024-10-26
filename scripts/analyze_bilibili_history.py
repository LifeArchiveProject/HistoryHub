import json
import os
from datetime import datetime
from collections import defaultdict
from scripts.utils import load_config, get_base_path

config = load_config()

# 读取分割的日期文件夹中的所有数据
def load_all_history_files():
    base_path = get_base_path()
    full_base_folder = os.path.join(base_path, config['input_folder'])
    all_data = []
    print("正在遍历历史记录文件夹...")

    if not os.path.exists(full_base_folder):
        print("本地历史记录文件夹不存在，无法加载数据。")
        return []

    for year in os.listdir(full_base_folder):
        year_path = os.path.join(full_base_folder, year)
        if os.path.isdir(year_path) and year.isdigit():
            for month in os.listdir(year_path):
                month_path = os.path.join(year_path, month)
                if os.path.isdir(month_path) and month.isdigit():
                    for day_file in os.listdir(month_path):
                        if day_file.endswith('.json'):
                            day_path = os.path.join(month_path, day_file)
                            with open(day_path, 'r', encoding='utf-8') as f:
                                daily_data = json.load(f)
                                all_data.extend(daily_data)

    print(f"共加载 {len(all_data)} 条记录。")
    return all_data


# 保存每天的观看数量到 JSON 文件
def save_daily_count_to_json(daily_count, year):
    base_path = get_base_path()
    full_output_folder = os.path.join(base_path, 'daily_count')
    if not os.path.exists(full_output_folder):
        os.makedirs(full_output_folder)

    output_file = os.path.join(full_output_folder, f'daily_count_{year}.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(daily_count, f, ensure_ascii=False, indent=4)
    print(f"每天观看数量已保存到 {output_file}")


# 统计每天和每月的视频观看数量
def calculate_video_counts(history_data):
    current_year = datetime.now().year
    daily_count = defaultdict(int)
    monthly_count = defaultdict(int)

    for entry in history_data:
        view_time = datetime.fromtimestamp(entry['view_at'])
        if view_time.year != current_year:
            continue

        date_str = view_time.strftime('%Y-%m-%d')
        month_str = view_time.strftime('%Y-%m')
        daily_count[date_str] += 1
        monthly_count[month_str] += 1

    return daily_count, monthly_count


# 单独获取每日观看数量
def get_daily_counts():
    history_data = load_all_history_files()
    if not history_data:
        return {"error": "没有找到历史记录数据。"}

    daily_count, _ = calculate_video_counts(history_data)
    return daily_count


# 单独获取每月观看数量
def get_monthly_counts():
    history_data = load_all_history_files()
    if not history_data:
        return {"error": "没有找到历史记录数据。"}

    _,monthly_count = calculate_video_counts(history_data)
    return monthly_count


# 手动更新观看计数
def update_counts():
    history_data = load_all_history_files()
    if not history_data:
        return "没有找到历史记录数据。"

    return "视频观看计数已更新。"


# 主函数
def main():
    history_data = load_all_history_files()

    if not history_data:
        print("没有找到历史记录数据。")
        return

    daily_count, monthly_count = calculate_video_counts(history_data)

    # 输出每月的视频观看统计
    print("\n每月观看视频数量：")
    for month, count in monthly_count.items():
        print(f"{month}: {count} 个视频")

    # 保存每天的观看数量到 JSON 文件
    current_year = datetime.now().year
    save_daily_count_to_json(daily_count, current_year)


# 供外部接口调用的函数
def get_daily_and_monthly_counts():
    history_data = load_all_history_files()
    if not history_data:
        return {"error": "没有找到历史记录数据。"}

    daily_count, monthly_count = calculate_video_counts(history_data)
    return {"daily_count": daily_count, "monthly_count": monthly_count}


# 如果该脚本直接运行，则调用 main()
if __name__ == '__main__':
    main()
