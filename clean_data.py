import json
import os


# 清洗数据函数
def clean_data(data, fields_to_remove):
    cleaned_data = []

    for record in data:
        cleaned_record = {key: value for key, value in record.items() if key not in fields_to_remove}
        if 'history' in record:  # 处理嵌套的 'history' 字段
            cleaned_record['history'] = {key: value for key, value in record['history'].items() if
                                         key not in fields_to_remove}
        cleaned_data.append(cleaned_record)

    return cleaned_data


# 保存清洗后的数据为JSON文件
def save_cleaned_data_by_date(cleaned_data, original_file_path, base_folder='cleaned_history_by_date'):
    # 提取文件的日期信息
    parts = original_file_path.split(os.sep)
    year = parts[-3]
    month = parts[-2]
    day_file = parts[-1]

    # 生成新的文件夹路径
    cleaned_folder = os.path.join(base_folder, year, month)

    if not os.path.exists(cleaned_folder):
        os.makedirs(cleaned_folder)

    cleaned_file_path = os.path.join(cleaned_folder, day_file)

    # 保存清洗后的数据
    with open(cleaned_file_path, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=4)

    print(f"清洗后的数据已保存到 {cleaned_file_path}")


# 读取分割的日期文件夹中的所有数据
def load_all_history_files(base_folder='history_by_date'):
    all_data = []
    file_paths = []  # 保存所有文件路径
    print("正在遍历历史记录文件夹...")

    if not os.path.exists(base_folder):
        print("本地历史记录文件夹不存在，无法加载数据。")
        return [], []

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
                                all_data.append(daily_data)
                                file_paths.append(day_path)

    print(f"共加载 {len(all_data)} 个文件的记录。")
    return all_data, file_paths


# 主函数：加载、清理并保存数据
def main():
    # 加载所有历史记录数据
    history_data_list, file_paths = load_all_history_files()

    if not history_data_list:
        print("没有找到历史记录数据，无需清理。")
        return

    # 想要删减的字段
    fields_to_remove = ['long_title', 'uri', 'badge', 'current', 'total', 'new_desc', 'is_finish', 'live_status']

    # 针对每个文件单独清洗和保存
    for history_data, file_path in zip(history_data_list, file_paths):
        cleaned_data = clean_data(history_data, fields_to_remove)
        save_cleaned_data_by_date(cleaned_data, file_path)


if __name__ == '__main__':
    main()
