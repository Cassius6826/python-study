from operator import is_
from file_define import FileReader, JsonFileReader, TextFileReader
from data_define import Record
from pyecharts.charts import Bar
from pyecharts.options import *
from pyecharts.globals import ThemeType
from pymysql import Connection


text_file_reader = TextFileReader("C:\data\code\suishou\数据分析\Text.txt")
json_file_reader = JsonFileReader("C:\data\code\suishou\数据分析\Json.txt")

jan_data: list[Record] = text_file_reader.read_data()
feb_data: list[Record] = json_file_reader.read_data()

all_data: list[Record] = jan_data + feb_data

# 构建MySQL链接对象
conn = Connection(
     host = "localhost",
     port = 3306,
     user = "root",
     password = "114514",
     autocommit = True
)

#获得游标对象
cursor = conn.cursor()
#选择数据库
conn.select_db("py_sql")
#组织SQL语言
#for record in all_data:
#    sql = f"insert into orders(order_date, order_id, money, province)"\
#           f"values('{record.date}','{record.order_id}','{record.money}','{record.province}')"
cursor.execute("select * from orders")

results: tuple = cursor.fetchall()
for i in results:
    print(i)
    #执行SQL语句
#    cursor.execute(sql)


conn.close()