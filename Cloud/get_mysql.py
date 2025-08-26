import pymysql

connection = pymysql.connect(
    host='116.205.105.233',
    user='root',
    password='Wan13882237039',
    database='database'
)

try:
    with connection.cursor() as cursor:
        # 执行 SQL 查询语句
        cursor.execute("SELECT * FROM `users` WHERE `plan`=%s", ('4',))
        # 获取查询结果集中的所有记录
        results = cursor.fetchall()
        for row in results:
            print(row)  # 打印每一行结果
finally:
    connection.close()  # 关闭连接
