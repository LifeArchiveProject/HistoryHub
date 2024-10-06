import calendar
import json
import os
import re
from datetime import datetime, timedelta

from jinja2 import Environment, FileSystemLoader
from pyecharts import options as opts
from pyecharts.charts import Calendar
from pyecharts.commons.utils import JsCode

# 设置周的起始日为星期一
calendar.setfirstweekday(calendar.MONDAY)


class HeatmapVisualizer:
    def __init__(self, template_file='template.html', output_dir='./', base_folder='daily_count'):
        """
        初始化 HeatmapVisualizer。

        :param template_file: Jinja2 模板文件名
        :param output_dir: 输出目录
        :param base_folder: 存放 JSON 数据的基础文件夹
        """
        self.template_file = template_file
        self.output_dir = output_dir
        self.base_folder = base_folder
        self.charts = []  # 存储所有生成的图表 HTML
        self.data = {}  # 存储每个年份的数据

        # 确保输出目录存在
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        # 自动检测可用的年份
        self.years = self.detect_years()

    def detect_years(self):
        """
        扫描 base_folder 文件夹，检测所有符合 daily_count_XXXX.json 格式的文件，并提取年份。

        :return: 排序后的年份列表
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
        """
        加载指定年份的 JSON 数据。

        :param year: 年份
        :return: 数据字典
        """
        data_file = os.path.join(self.base_folder, f'daily_count_{year}.json')
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                daily_count = json.load(f)
            return daily_count
        except FileNotFoundError:
            print(f"文件 {data_file} 不存在，请检查文件路径。")
            return {}

    def generate_date_range(self, daily_count):
        """
        生成指定年份的日期范围。

        :param daily_count: 每日计数数据
        :return: 日期列表
        """
        if not daily_count:
            return []

        # 获取数据中的所有日期
        try:
            all_dates = [datetime.strptime(date, '%Y-%m-%d') for date in daily_count.keys()]
        except ValueError as e:
            print(f"日期格式错误: {e}")
            return []

        min_date, max_date = min(all_dates), max(all_dates)

        # 确保数据只包含一个年份
        if min_date.year != max_date.year:
            raise ValueError("数据中包含多个年份，请确保数据只包含一个年份。")

        year = min_date.year

        # 生成从1月1日到12月31日的日期范围
        num_days = (datetime(year, 12, 31) - datetime(year, 1, 1)).days + 1
        date_range = [datetime(year, 1, 1) + timedelta(days=i) for i in range(num_days)]
        return date_range

    def prepare_data_for_calendar(self, date_range, daily_count):
        """
        准备日历图表的数据。

        :param date_range: 日期范围
        :param daily_count: 每日计数数据
        :return: 数据列表
        """
        data = [
            [date.strftime('%Y-%m-%d'), daily_count.get(date.strftime('%Y-%m-%d'), 0)]
            for date in date_range
        ]
        return data

    def create_calendar_chart(self, year, daily_count):
        """
        创建单个年份的日历热力图。

        :param year: 年份
        :param daily_count: 每日计数数据
        :return: 图表的 HTML 片段
        """
        date_range = self.generate_date_range(daily_count)
        if not date_range:
            print(f"年份 {year} 的日期范围生成失败。")
            return ""

        data = self.prepare_data_for_calendar(date_range, daily_count)

        # 设置日历的范围
        calendar_range = [f"{year}-01-01", f"{year}-12-31"]

        # 定义颜色分段
        pieces = [
            {"min": 1, "max": 10, "color": "#FFECF1"},
            {"min": 11, "max": 50, "color": "#FFB3CA"},
            {"min": 51, "max": 100, "color": "#FF8CB0"},
            {"min": 101, "max": 200, "color": "#FF6699"},
            {"min": 201, "max": 9999, "color": "#E84B85"},
        ]

        # 创建日历热力图
        calendar_chart = (
            Calendar(init_opts=opts.InitOpts(width="1000px", height="200px"))
            .add(
                series_name="观看数量",
                yaxis_data=data,
                calendar_opts=opts.CalendarOpts(
                    range_=calendar_range,
                    daylabel_opts=opts.CalendarDayLabelOpts(
                        name_map="cn",  # 显示中文的星期名称
                    ),
                    monthlabel_opts=opts.CalendarMonthLabelOpts(
                        name_map="cn",  # 显示中文的月份名称
                    ),
                    cell_size=[15, 15],  # 设置每个格子的大小
                    itemstyle_opts=opts.ItemStyleOpts(
                        border_width=0.5,
                        border_color="#ccc",  # 边框颜色
                        color="#ffffff",  # 方格背景颜色
                    ),
                    splitline_opts=opts.SplitLineOpts(is_show=False)  # 隐藏月份之间的分割线
                ),
            )
            .set_global_opts(
                visualmap_opts=opts.VisualMapOpts(
                    max_=100,
                    min_=1,
                    orient="horizontal",
                    is_piecewise=True,
                    pieces=pieces,
                    pos_top="top",
                    textstyle_opts=opts.TextStyleOpts(  # 修改标签颜色
                        color="#FF6699",  # 标签文字颜色
                    ),
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

        # 渲染图表为 HTML 片段
        chart_html = calendar_chart.render_embed()
        return chart_html

    def plot_calendar_heatmaps(self):
        """
        为所有检测到的年份生成日历热力图，并将其整合到一个 HTML 文件中。
        """
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
            return

        # 使用 Jinja2 渲染完整的 HTML 文件
        env = Environment(loader=FileSystemLoader('.'))
        try:
            template = env.get_template(self.template_file)
        except Exception as e:
            print(f"加载模板文件 {self.template_file} 时出错: {e}")
            return

        rendered_html = template.render(
            title="Bilibili 每年每日视频观看热力图",
            charts=self.charts
        )

        # 将生成的 HTML 保存到指定的输出目录
        output_file = os.path.join(self.output_dir, "heatmap_comparison.html")
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(rendered_html)
            print(f"热力图已保存为 {output_file}")
        except Exception as e:
            print(f"保存 HTML 文件时出错: {e}")


if __name__ == "__main__":
    visualizer = HeatmapVisualizer()  # 自动检测年份
    visualizer.plot_calendar_heatmaps()
