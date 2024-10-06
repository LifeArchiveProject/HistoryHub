import os
import requests
import json
import time
from datetime import datetime

# 切换到正确的工作目录
os.chdir('/www/wwwroot/python')
print(f"当前工作目录: {os.getcwd()}")

# 读取本地cookie文件
def load_cookie(file_path='cookie.txt'):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()  # 去除首尾空白字符
    else:
        print(f"Cookie文件{file_path}不存在，无法继续执行。")
        exit(1)

# 设置请求头，包括从文件读取的Cookie
cookie = load_cookie()

headers = {
    'Cookie': "SESSDATA=" + cookie,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'Referer': 'https://www.bilibili.com',
}
# 初始化参数
params = {
    'ps': 30,  # 每页数量，默认为 20，最大 30
    'max': '',  # 初始为空
    'view_at': '',  # 初始为空
    'business': '',  # 可选参数，默认为空表示获取所有类型
}


# 游标记录文件路径
cursor_file = 'cursor_history.json'


# 读取游标记录
def load_cursor_history():
    if os.path.exists(cursor_file):
        with open(cursor_file, 'r', encoding='utf-8') as f:
            return set(json.load(f))  # 将游标记录存储为集合，方便查找
    return set()


# 保存游标记录
def save_cursor_history(cursor_history):
    with open(cursor_file, 'w', encoding='utf-8') as f:
        json.dump(list(cursor_history), f, ensure_ascii=False, indent=4)
    print(f"游标历史保存成功，共{len(cursor_history)}条记录。")


# 查找本地最新的日期文件并加载数据
def find_latest_local_history(base_folder='history_by_date'):
    print("正在查找本地最新的历史记录...")
    if not os.path.exists(base_folder):
        print("本地历史记录文件夹不存在，将从头开始同步。")
        return []

    latest_history = []
    try:
        latest_year = max([int(year) for year in os.listdir(base_folder) if year.isdigit()], default=None)

        if latest_year:
            latest_month = max(
                [int(month) for month in os.listdir(os.path.join(base_folder, str(latest_year))) if month.isdigit()],
                default=None)

            if latest_month:
                latest_day = max([int(day.split('.')[0]) for day in
                                  os.listdir(os.path.join(base_folder, str(latest_year), f"{latest_month:02}")) if
                                  day.endswith('.json')], default=None)

                if latest_day:
                    latest_file = os.path.join(base_folder, str(latest_year), f"{latest_month:02}",
                                               f"{latest_day:02}.json")
                    print(f"找到最新历史记录文件: {latest_file}")
                    with open(latest_file, 'r', encoding='utf-8') as f:
                        latest_history = json.load(f)
    except ValueError:
        print("历史记录目录格式不正确，可能尚未创建任何文件。")

    return latest_history


# 保存更新后的历史记录
def save_history(history_data, base_folder='history_by_date'):
    print(f"开始保存{len(history_data)}条新历史记录...")
    for entry in history_data:
        timestamp = entry['view_at']
        dt_object = datetime.fromtimestamp(timestamp)
        year = dt_object.strftime('%Y')
        month = dt_object.strftime('%m')
        day = dt_object.strftime('%d')

        # 创建文件夹路径 年/月/日
        folder_path = os.path.join(base_folder, year, month)
        os.makedirs(folder_path, exist_ok=True)

        # 文件名为当天的日期
        file_path = os.path.join(folder_path, f"{day}.json")

        # 如果文件已存在，读取并合并数据
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                daily_data = json.load(f)
        else:
            daily_data = []

        # 将新数据追加到当天的数据中
        daily_data.append(entry)

        # 将数据保存回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(daily_data, f, ensure_ascii=False, indent=4)
    print(f"历史记录保存完成。")


# 获取新历史记录并与本地记录对比
def fetch_and_compare_history(headers, params, local_history, cursor_history):
    print("正在从B站API获取历史记录...")
    url = 'https://api.bilibili.com/x/web-interface/history/cursor'
    all_data = []
    local_oids = {entry['history']['oid'] for entry in local_history}
    duplicate_count = 0
    stop_threshold = 30

    while True:
        print("发送请求获取数据...")
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            try:
                data = response.json()
            except json.JSONDecodeError:
                print("JSON Decode Error: 无法解析服务器响应")
                break

            # 检查code是否为0
            if data['code'] != 0:
                print(f"API请求失败，错误码: {data['code']}, 错误信息: {data['message']}")
                break

            # 检查数据中的list
            if 'data' in data and 'list' in data['data']:
                print(f"获取到{len(data['data']['list'])}条记录，进行对比...")

                # 打印获取到的数据
                for entry in data['data']['list']:
                    print(f"标题: {entry['title']}, 观看时间: {datetime.fromtimestamp(entry['view_at'])}")

                for entry in data['data']['list']:
                    if entry['history']['oid'] in local_oids:
                        duplicate_count += 1
                        if duplicate_count >= stop_threshold:
                            print(f"连续{stop_threshold}条记录已存在，停止请求。")
                            return all_data
                    else:
                        all_data.append(entry)
                        duplicate_count = 0

                # 更新请求的游标参数
                if 'cursor' in data['data']:
                    current_max = data['data']['cursor']['max']

                    # 检查游标是否重复
                    if current_max in cursor_history:
                        print(f"游标 {current_max} 已存在，停止请求且不保存当前批次数据。")
                        return all_data[:-len(data['data']['list'])]  # 返回前一批的数据，不保存当前数据
                    else:
                        cursor_history.add(current_max)  # 记录游标
                        params['max'] = current_max
                        params['view_at'] = data['data']['cursor']['view_at']
                        print(f"请求游标更新：max={params['max']}, view_at={params['view_at']}")
                else:
                    print("未能获取游标信息，停止请求。")
                    break
                # 暂停1秒在请求
                time.sleep(1)
            else:
                print("没有更多的数据或数据结构错误。")
                break
        else:
            print(f"请求失败，状态码: {response.status_code}, 原因: {response.text}")
            break

    return all_data


# 主逻辑
cursor_history = load_cursor_history()  # 加载游标历史
local_history = find_latest_local_history()  # 读取本地最新日期的历史记录
new_history = fetch_and_compare_history(headers, params, local_history, cursor_history)  # 获取新历史记录

if new_history:
    save_history(new_history)  # 将数据按日期切分并保存
    save_cursor_history(cursor_history)  # 保存游标历史
else:
    print("没有新记录可更新。")
