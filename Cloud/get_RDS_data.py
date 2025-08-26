# -*- coding:utf-8 -*-
# 从MySQL数据库的数据表中读取每一行数据放入列表中，最后返回一个完整的列表

import pymysql

def get_mysql_list(database, table_name):
    #  创建连接，指定数据库的ip地址，账号、密码、端口号、要操作的数据库、字符集
    host, user, pwd = '116.205.105.233', 'root', 'Wan13882237039'
    conn = pymysql.connect(
        host='116.205.105.233',
        port=3306,
        user='root',
        passwd='Wan13882237039',
        db='database',
        charset='utf8'
    )  # port必须写int类型,MySQL的默认端口为3306. charset必须写utf8
    # 创建游标
    cursor = conn.cursor()
    # 执行sql语句
    sql = 'select * from %s ;' % table_name
    cursor.execute(sql)

    # 获取到sql执行的全部结果
    results = cursor.fetchall()
    table_list = []
    for r in results:
        table_list.append(list(r))  # 由于fetchall方法返回的一个元组，需要每一行为列表形式的数据，将其转换为list类型。

    cursor.close()  # 关闭游标
    conn.close()  # 关闭连接

    return list(table_list)  # 返回一个完整的列表数据


if __name__ == '__main__':
    x = get_mysql_list('database', 'dishname')
    print(x)
