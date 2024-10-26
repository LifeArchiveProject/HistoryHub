import json
import os
from scripts.utils import load_config, get_base_path

config = load_config()

def clean_history_data():
    base_path = get_base_path()
    full_input_folder = os.path.join(base_path, config['input_folder'])
    full_output_folder = os.path.join(base_path, config['output_folder'])

    if not os.path.exists(full_input_folder):
        print(f"输入文件夹 '{full_input_folder}' 不存在。")
        return {"status": "error", "message": f"输入文件夹 '{full_input_folder}' 不存在。"}

    cleaned_files = 0
    for year in os.listdir(full_input_folder):
        year_path = os.path.join(full_input_folder, year)
        if os.path.isdir(year_path) and year.isdigit():
            for month in os.listdir(year_path):
                month_path = os.path.join(year_path, month)
                if os.path.isdir(month_path) and month.isdigit():
                    for day_file in os.listdir(month_path):
                        if day_file.endswith('.json'):
                            input_file = os.path.join(month_path, day_file)
                            output_file = os.path.join(full_output_folder, year, month, day_file)

                            # 确保输出目录存在
                            os.makedirs(os.path.dirname(output_file), exist_ok=True)

                            with open(input_file, 'r', encoding='utf-8') as f:
                                data = json.load(f)

                            # 清理数据
                            cleaned_data = clean_data(data, config['fields_to_remove'])

                            # 保存清理后的数据
                            with open(output_file, 'w', encoding='utf-8') as f:
                                json.dump(cleaned_data, f, ensure_ascii=False, indent=4)
                            
                            cleaned_files += 1

    message = f"数据清理完成。共处理 {cleaned_files} 个文件。"
    return {"status": "success", "message": message}

def clean_data(data, fields_to_remove):
    cleaned_data = []
    for item in data:
        cleaned_item = {key: value for key, value in item.items() if key not in fields_to_remove}
        if 'history' in item:
            cleaned_item['history'] = {key: value for key, value in item['history'].items() if key not in fields_to_remove}
        cleaned_data.append(cleaned_item)
    return cleaned_data

if __name__ == "__main__":
    result = clean_history_data()
    print(result["message"])
