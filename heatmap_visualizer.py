import calendar
import json
from datetime import datetime, timedelta

from jinja2 import Environment, FileSystemLoader
from pyecharts import options as opts
from pyecharts.charts import Calendar
from pyecharts.commons.utils import JsCode

# 设置周的起始日为星期一
calendar.setfirstweekday(calendar.MONDAY)


class HeatmapVisualizer:
    def __init__(self, data_file='daily_count.json', template_file='template.html', output_dir='/www/wwwroot/java/buy_customers/dist'):
        self.data_file = data_file
        self.template_file = template_file
        self.output_dir = output_dir  # 添加输出目录
        self.daily_count = self.load_data()
        self.date_range = self.generate_date_range()

    # 加载 JSON 数据
    def load_data(self):
        with open(self.data_file, 'r', encoding='utf-8') as f:
            daily_count = json.load(f)
        return daily_count

    # 生成一个包含所有日期的范围
    def generate_date_range(self):
        # 获取数据中的所有日期
        all_dates = [datetime.strptime(date, '%Y-%m-%d') for date in self.daily_count.keys()]
        min_date, max_date = min(all_dates), max(all_dates)

        # 确保数据只包含一个年份
        if min_date.year != max_date.year:
            raise ValueError("数据中包含多个年份，请确保数据只包含一个年份。")

        year = min_date.year

        # 生成从1月1日到12月31日的日期范围
        num_days = (datetime(year, 12, 31) - datetime(year, 1, 1)).days + 1
        date_range = [datetime(year, 1, 1) + timedelta(days=i) for i in range(num_days)]
        return date_range

    # 准备数据用于 Calendar 图表
    def prepare_data_for_calendar(self):
        # 将数据转换为 [日期字符串, 数值] 的形式
        data = [
            [date, self.daily_count.get(date, 0)]
            for date in [d.strftime('%Y-%m-%d') for d in self.date_range]
        ]
        return data

    # 绘制 Calendar 热力图
    def plot_calendar_heatmap(self):
        data = self.prepare_data_for_calendar()
        year = self.date_range[0].year

        # 设置日历的范围
        calendar_range = [f"{year}-01-01", f"{year}-12-31"]

        # 定义颜色分段
        pieces = [
            {"min": 1, "max": 10, "color": "#c6e48b"},
            {"min": 11, "max": 50, "color": "#7bc96f"},
            {"min": 51, "max": 100, "color": "#239a3b"},
            {"min": 101, "max": 99999, "color": "#196127"}
        ]

        # 创建日历热力图
        calendar = (
            Calendar(init_opts=opts.InitOpts(width="1000px", height="250px"))
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
                        border_color="#ccc"
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
        chart_html = calendar.render_embed()

        # 使用 Jinja2 渲染完整的 HTML 文件
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template(self.template_file)
        rendered_html = template.render(
            title="bilibili每日视频观看热力图",
            chart=chart_html
        )

        # 将生成的 HTML 保存到指定的输出目录
        output_file = f"{self.output_dir}/heatmap.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(rendered_html)

        print(f"热力图已保存为 {output_file}")


if __name__ == "__main__":
    visualizer = HeatmapVisualizer()
    visualizer.plot_calendar_heatmap()
