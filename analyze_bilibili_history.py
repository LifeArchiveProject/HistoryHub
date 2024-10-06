import json
import os
from datetime import datetime
from collections import defaultdict


# 读取分割的日期文件夹中的所有数据
def load_all_history_files(base_folder='history_by_date'):
    all_data = []
    print("正在遍历历史记录文件夹...")

    if not os.path.exists(base_folder):
        print("本地历史记录文件夹不存在，无法加载数据。")
        return []

    for year in os.listdir(base_folder):
        year_path = os.path.join(base_folder, year)
        if os.path.isdir(year_path) and year.isdigit():
            for month in os.listdir(year_path):
                month_path = os.path.join(year_path, month)
                if os.path.isdir(month_path) and month.isdigit():
                    for day_file in os.listdir(month_path):
                        if day_file.endswith('.json'):
                            day_path = os.path.join(month_path, day_file)
                            print(f"正在加载文件: {day_path}")
                            with open(day_path, 'r', encoding='utf-8') as f:
                                daily_data = json.load(f)
                                all_data.extend(daily_data)

    print(f"共加载 {len(all_data)} 条记录。")
    return all_data


# 保存每天的观看数量到 JSON 文件
def save_daily_count_to_json(daily_count, year, output_folder='daily_count'):
    # 检查并创建输出文件夹
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_file = os.path.join(output_folder, f'daily_count_{year}.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(daily_count, f, ensure_ascii=False, indent=4)
    print(f"每天观看数量已保存到 {output_file}")


# 主函数
def main():
    # 加载所有历史记录数据
    history_data = load_all_history_files()

    if not history_data:
        print("没有找到历史记录数据。")
        return

    # 获取当前年份
    current_year = datetime.now().year

    # 将数据按天分组
    daily_data = defaultdict(list)
    monthly_count = defaultdict(int)
    daily_count = defaultdict(int)  # 记录每天的视频观看数量

    for entry in history_data:
        # 将 view_at 转换为日期
        view_time = datetime.fromtimestamp(entry['view_at'])
        if view_time.year != current_year:
            continue  # 只处理当前年份的数据

        date_str = view_time.strftime('%Y-%m-%d')  # 按天分组
        month_str = view_time.strftime('%Y-%m')  # 按月计数
        daily_data[date_str].append(view_time)
        monthly_count[month_str] += 1
        daily_count[date_str] += 1  # 增加每天的观看数量

    # 统计每天的视频数量，最早和最晚的观看时间
    for date, times in daily_data.items():
        times.sort()
        first_view = times[0].strftime('%H:%M:%S')
        last_view = times[-1].strftime('%H:%M:%S')
        print(f"{date}: 看了 {len(times)} 个视频，最早是 {first_view}，最晚是 {last_view}")

    # 输出每月的视频观看统计
    print("\n每月观看视频数量：")
    for month, count in monthly_count.items():
        print(f"{month}: {count} 个视频")

    # 保存每天的观看数量到 JSON 文件
    save_daily_count_to_json(daily_count, current_year)


if __name__ == '__main__':
    main()