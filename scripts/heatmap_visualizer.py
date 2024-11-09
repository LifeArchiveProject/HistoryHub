import calendar
import json
import os
import re
from datetime import datetime, timedelta

from jinja2 import Environment, FileSystemLoader
from pyecharts import options as opts
from pyecharts.charts import Calendar
from pyecharts.commons.utils import JsCode

from scripts.utils import load_config, get_output_path, get_config_path

# 设置周的起始日为星期一
calendar.setfirstweekday(calendar.MONDAY)

config = load_config()

class HeatmapVisualizer:
    def __init__(self):
        # 从配置文件加载配置
        self.config = load_config()
        self.heatmap_config = self.config.get('heatmap', {})
        
        # 使用配置文件中的路径
        self.template_file = get_config_path(self.heatmap_config.get('template_file', 'template.html'))
        self.output_dir = get_output_path(self.heatmap_config.get('output_dir', 'heatmap'))
        self.base_folder = get_output_path('')
        
        # 从配置中获取图表尺寸
        self.chart_width = self.heatmap_config.get('chart', {}).get('width', '1000px')
        self.chart_height = self.heatmap_config.get('chart', {}).get('height', '200px')
        
        # 从配置中获取颜色配置
        self.color_pieces = self.heatmap_config.get('colors', {}).get('pieces', [
            {"min": 1, "max": 10, "color": "#FFECF1"},
            {"min": 11, "max": 50, "color": "#FFB3CA"},
            {"min": 51, "max": 100, "color": "#FF8CB0"},
            {"min": 101, "max": 200, "color": "#FF6699"},
            {"min": 201, "max": 9999, "color": "#E84B85"},
        ])
        
        self.charts = []
        self.data = {}
        
        # 打印路径信息
        print("\n=== 热力图路径信息 ===")
        print(f"模板文件路径: {self.template_file}")
        print(f"输出目录: {self.output_dir}")
        print(f"基础文件夹: {self.base_folder}")
        print(f"模板文件存在: {os.path.exists(self.template_file)}")
        if os.path.exists(os.path.dirname(self.template_file)):
            print(f"模板目录内容: {os.listdir(os.path.dirname(self.template_file))}")
        print("=====================\n")
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.years = self.detect_years()

    def detect_years(self):
        """
        扫描 base_folder 文件夹，检测所有符合 daily_count_XXXX.json 格式的文件，并提取年份。
        """
        pattern = re.compile(r'daily_count_(\d{4})\.json$')
        years = []
        if not os.path.exists(self.base_folder):
            print(f"文件夹 {self.base_folder} 不存在。")
            return years

        for filename in os.listdir(self.base_folder):
            match = pattern.match(filename)
            if match:
                year = int(match.group(1))
                years.append(year)

        years = sorted(years)  # 按年份排序
        if not years:
            print(f"在文件夹 {self.base_folder} 中未找到符合格式的 JSON 文件。")
        else:
            print(f"检测到年份: {years}")
        return years

    def load_data(self, year):
        """加载指定年份的 JSON 数据"""
        data_file = os.path.join(self.base_folder, f'daily_count_{year}.json')
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                daily_count = json.load(f)
            return daily_count
        except FileNotFoundError:
            print(f"文件 {data_file} 不存在，请检查文件路径。")
            return {}

    def plot_calendar_heatmaps(self):
        """生成热力图"""
        for year in self.years:
            daily_count = self.load_data(year)
            if not daily_count:
                print(f"跳过年份 {year}，因为没有找到相关数据或数据为空。")
                continue
            self.data[year] = daily_count
            try:
                chart_html = self.create_calendar_chart(year, daily_count)
                if chart_html:
                    self.charts.append({
                        'year': year,
                        'chart_html': chart_html
                    })
            except ValueError as e:
                print(f"处理年份 {year} 时出错: {e}")
                continue

        if not self.charts:
            print("没有可生成的热力图。")
            return {"status": "error", "message": "没有可生成的热力图。"}

        env = Environment(loader=FileSystemLoader(os.path.dirname(self.template_file)))
        try:
            template = env.get_template(os.path.basename(self.template_file))
        except Exception as e:
            error_message = f"加载模板文件 {self.template_file} 时出错: {str(e)}"
            print(error_message)
            return {"status": "error", "message": error_message}

        rendered_html = template.render(
            title=self.heatmap_config.get('title', "Bilibili 每年每日视频观看热力图"),
            charts=self.charts
        )

        output_file = os.path.join(self.output_dir, "heatmap_comparison.html")
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(rendered_html)
            success_message = f"热力图已保存为 {output_file}"
            return {"status": "success", "message": success_message}
        except Exception as e:
            error_message = f"保存 HTML 文件时出错: {e}"
            print(error_message)
            return {"status": "error", "message": error_message}

    def create_calendar_chart(self, year, daily_count):
        """创建日历热力图"""
        date_range = self.generate_date_range(daily_count)
        if not date_range:
            print(f"年份 {year} 的日期范围生成失败。")
            return ""

        data = self.prepare_data_for_calendar(date_range, daily_count)

        calendar_range = [f"{year}-01-01", f"{year}-12-31"]

        calendar_chart = (
            Calendar(init_opts=opts.InitOpts(width=self.chart_width, height=self.chart_height))
            .add(
                series_name="观看数量",
                yaxis_data=data,
                calendar_opts=opts.CalendarOpts(
                    range_=calendar_range,
                    daylabel_opts=opts.CalendarDayLabelOpts(name_map="cn"),
                    monthlabel_opts=opts.CalendarMonthLabelOpts(name_map="cn"),
                    cell_size=[15, 15],
                    itemstyle_opts=opts.ItemStyleOpts(
                        border_width=0.5,
                        border_color="#ccc",
                        color="#ffffff",
                    ),
                    splitline_opts=opts.SplitLineOpts(is_show=False)
                ),
            )
            .set_global_opts(
                visualmap_opts=opts.VisualMapOpts(
                    max_=100,
                    min_=1,
                    orient="horizontal",
                    is_piecewise=True,
                    pieces=self.color_pieces,
                    pos_top="top",
                    textstyle_opts=opts.TextStyleOpts(color="#FF6699"),
                ),
                tooltip_opts=opts.TooltipOpts(
                    is_show=True,
                    formatter=JsCode(
                        """
                        function(params) { 
                            var date = params.value[0];
                            var count = params.value[1];
                            return date + ' : ' + count + '个视频';
                        }
                        """
                    )
                )
            )
        )

        return calendar_chart.render_embed()

    def generate_date_range(self, daily_count):
        """生成日期范围"""
        if not daily_count:
            return []

        try:
            all_dates = [datetime.strptime(date, '%Y-%m-%d') for date in daily_count.keys()]
        except ValueError as e:
            print(f"日期格式错误: {e}")
            return []

        min_date, max_date = min(all_dates), max(all_dates)

        if min_date.year != max_date.year:
            raise ValueError("数据中包含多个年份，请确保数据只包含一个年份。")

        year = min_date.year
        num_days = (datetime(year, 12, 31) - datetime(year, 1, 1)).days + 1
        return [datetime(year, 1, 1) + timedelta(days=i) for i in range(num_days)]

    def prepare_data_for_calendar(self, date_range, daily_count):
        """准备日历数据"""
        return [
            [date.strftime('%Y-%m-%d'), daily_count.get(date.strftime('%Y-%m-%d'), 0)]
            for date in date_range
        ]

def generate_heatmap():
    visualizer = HeatmapVisualizer()
    return visualizer.plot_calendar_heatmaps()

if __name__ == "__main__":
    result = generate_heatmap()
    print(result["message"])
