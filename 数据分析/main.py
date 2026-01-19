from operator import is_
from file_define import FileReader, JsonFileReader, TextFileReader
from data_define import Record
from pyecharts.charts import Bar
from pyecharts.options import *
from pyecharts.globals import ThemeType


text_file_reader = TextFileReader("C:\data\code\suishou\数据分析\Text.txt")
json_file_reader = JsonFileReader("C:\data\code\suishou\数据分析\Json.txt")

jan_data: list[Record] = text_file_reader.read_data()
feb_data: list[Record] = json_file_reader.read_data()

all_data: list[Record] = jan_data + feb_data

#数据计算
data_dict = {}
for record in all_data:
    if record.date in data_dict.keys():
        data_dict[record.date] += record.money
    else:
        data_dict[record.date] = record.money

#可视化开发
bar = Bar(init_opts=InitOpts(theme=ThemeType.LIGHT))

bar.add_xaxis(list(data_dict.keys()))
bar.add_yaxis("销售额", list(data_dict.values()), label_opts=LabelOpts(is_show = False))
bar.set_global_opts(
    title_opts = TitleOpts(title="每日销售额")
)

bar.render("每日销售额柱状图.html")