from pymysql import Connection

'''获取到连接MySQL的对象'''
conn = Connection(
    host = "localhost",  #主机名（IP）
    port = 3306,         #端口
    user = 'root',       #账户
    password = '114514', #密码
    autocommit = True
)

print(conn.get_server_info())   #输出为服务器的版本

'''获取游标对象'''
cursor = conn.cursor()
conn.select_db("test")  #选择数据库

'''使用游标对象执行MySQL语句'''
# cursor.execute("CREATE TABLE test_pymysql(id int, info varchar(255));")
cursor.execute("select * from student")     #查询表
cursor.execute("insert into student values(1002, '梅峻豪', 18)")
# 插入操作要有提交这一步

'''获取查询结果'''
results: tuple = cursor.fetchall()
for i in results:
    print(i)


conn.close()    #关闭数据库连接