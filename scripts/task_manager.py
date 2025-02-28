import os
import sqlite3
import sys
import argparse
from datetime import datetime

def get_db_connection():
    """获取数据库连接"""
    # 使用相对路径，假设脚本在项目根目录或scripts目录下运行
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir) if os.path.basename(script_dir) == 'scripts' else script_dir
    
    db_path = os.path.join(project_root, 'output', 'database', 'scheduler.db')
    
    if not os.path.exists(db_path):
        print(f"错误: 数据库文件不存在: {db_path}")
        sys.exit(1)
        
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def list_tasks():
    """列出所有任务及其状态"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT t.task_id, t.name, t.task_type, t.enabled, t.schedule_type, t.schedule_time,
           t.last_run_time, t.next_run_time, t.last_status, 
           (SELECT GROUP_CONCAT(depends_on, ', ') FROM task_dependencies WHERE task_id = t.task_id) as dependencies
    FROM tasks t
    ORDER BY 
        CASE t.task_type WHEN 'main' THEN 0 ELSE 1 END, 
        t.parent_id, 
        t.sequence_number
    """)
    
    tasks = cursor.fetchall()
    
    print("\n=== 任务列表 ===")
    print(f"总计 {len(tasks)} 个任务\n")
    
    # 打印所有主任务和它们的子任务
    main_tasks = [t for t in tasks if t['task_type'] == 'main']
    for main_task in main_tasks:
        print(f"【{main_task['task_id']}】({main_task['name']}) - " + 
              f"{'启用' if main_task['enabled'] else '禁用'}")
        print(f"  类型: 主任务, 调度: {main_task['schedule_type']}")
        
        if main_task['schedule_time']:
            print(f"  执行时间: {main_task['schedule_time']}")
            
        print(f"  上次执行: {main_task['last_run_time'] or '未执行'}")
        print(f"  下次执行: {main_task['next_run_time'] or '未计划'}")
        print(f"  上次状态: {main_task['last_status'] or '未知'}")
        
        # 获取这个主任务的子任务
        sub_tasks = [t for t in tasks if t['task_type'] == 'sub' and t['dependencies'] and main_task['task_id'] in t['dependencies']]
        
        if sub_tasks:
            print("\n  子任务:")
            for idx, sub_task in enumerate(sub_tasks, 1):
                print(f"  {idx}. {sub_task['task_id']} ({sub_task['name']}) - " +
                      f"{'启用' if sub_task['enabled'] else '禁用'}")
                      
        # 添加一个空行分隔不同的主任务
        print()
    
    conn.close()

def enable_task(task_id, enable=True):
    """启用或禁用任务"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 检查任务是否存在
    cursor.execute("SELECT task_id, name, task_type, enabled FROM tasks WHERE task_id = ?", (task_id,))
    task = cursor.fetchone()
    
    if not task:
        print(f"错误: 任务 '{task_id}' 不存在")
        conn.close()
        return False
    
    current_status = bool(task['enabled'])
    if current_status == enable:
        print(f"任务 '{task_id}' 已经{'启用' if enable else '禁用'}，无需更改")
        conn.close()
        return True
    
    # 更新任务状态
    now = datetime.now().isoformat()
    cursor.execute("""
    UPDATE tasks 
    SET enabled = ?, last_modified = ?
    WHERE task_id = ?
    """, (1 if enable else 0, now, task_id))
    
    conn.commit()
    conn.close()
    
    print(f"任务 '{task_id}' ({task['name']}) 已{'启用' if enable else '禁用'}")
    return True

def get_task_details(task_id):
    """获取任务详情"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 查询任务基本信息
    cursor.execute("""
    SELECT * FROM tasks WHERE task_id = ?
    """, (task_id,))
    
    task = cursor.fetchone()
    
    if not task:
        print(f"错误: 任务 '{task_id}' 不存在")
        conn.close()
        return False
    
    print(f"\n=== 任务详情: {task_id} ===")
    print(f"名称: {task['name']}")
    print(f"类型: {'主任务' if task['task_type'] == 'main' else '子任务'}")
    print(f"状态: {'启用' if task['enabled'] else '禁用'}")
    print(f"接口: {task['method']} {task['endpoint']}")
    print(f"调度类型: {task['schedule_type']}")
    
    if task['schedule_time']:
        print(f"调度时间: {task['schedule_time']}")
    
    if task['schedule_delay']:
        print(f"延迟时间: {task['schedule_delay']}秒")
    
    print(f"上次执行: {task['last_run_time'] or '未执行'}")
    print(f"下次执行: {task['next_run_time'] or '未计划'}")
    print(f"执行状态: {task['last_status'] or '未知'}")
    print(f"总执行次数: {task['total_runs']}")
    print(f"成功次数: {task['success_runs']}")
    print(f"失败次数: {task['fail_runs']}")
    
    if task['last_error']:
        print(f"最近错误: {task['last_error']}")
    
    # 查询依赖关系
    cursor.execute("""
    SELECT depends_on FROM task_dependencies WHERE task_id = ?
    """, (task_id,))
    
    dependencies = [row['depends_on'] for row in cursor.fetchall()]
    
    if dependencies:
        print(f"\n依赖任务: {', '.join(dependencies)}")
    
    # 查询被依赖关系
    cursor.execute("""
    SELECT task_id FROM task_dependencies WHERE depends_on = ?
    """, (task_id,))
    
    dependent_tasks = [row['task_id'] for row in cursor.fetchall()]
    
    if dependent_tasks:
        print(f"被依赖任务: {', '.join(dependent_tasks)}")
    
    # 如果是主任务，查询子任务
    if task['task_type'] == 'main':
        cursor.execute("""
        SELECT task_id, name, enabled, sequence_number 
        FROM tasks 
        WHERE parent_id = ? 
        ORDER BY sequence_number
        """, (task_id,))
        
        subtasks = cursor.fetchall()
        
        if subtasks:
            print("\n子任务:")
            for idx, subtask in enumerate(subtasks, 1):
                print(f"  {idx}. {subtask['task_id']} ({subtask['name']}) - " +
                      f"{'启用' if subtask['enabled'] else '禁用'}")
    
    # 获取最近的执行记录
    cursor.execute("""
    SELECT * FROM task_executions 
    WHERE task_id = ? 
    ORDER BY start_time DESC 
    LIMIT 5
    """, (task_id,))
    
    executions = cursor.fetchall()
    
    if executions:
        print("\n最近执行记录:")
        for idx, exec_record in enumerate(executions, 1):
            print(f"  {idx}. 时间: {exec_record['start_time']}")
            print(f"     状态: {exec_record['status']}")
            print(f"     耗时: {exec_record['duration']}秒")
            if exec_record['error_message']:
                print(f"     错误: {exec_record['error_message']}")
    
    conn.close()
    return True

def main():
    parser = argparse.ArgumentParser(description='任务管理工具')
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # 列出所有任务
    list_parser = subparsers.add_parser('list', help='列出所有任务')
    
    # 启用任务
    enable_parser = subparsers.add_parser('enable', help='启用任务')
    enable_parser.add_argument('task_id', help='任务ID')
    
    # 禁用任务
    disable_parser = subparsers.add_parser('disable', help='禁用任务')
    disable_parser.add_argument('task_id', help='任务ID')
    
    # 获取任务详情
    details_parser = subparsers.add_parser('details', help='获取任务详情')
    details_parser.add_argument('task_id', help='任务ID')
    
    args = parser.parse_args()
    
    if args.command == 'list':
        list_tasks()
    elif args.command == 'enable':
        enable_task(args.task_id, True)
    elif args.command == 'disable':
        enable_task(args.task_id, False)
    elif args.command == 'details':
        get_task_details(args.task_id)
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 