import json
input_file_path = 'class_indices.json'
output_file_path = 'insert_statements_type.sql'

# 读取class_indices.json文件
with open('class_indices.json', 'r') as json_file:
    class_indices = json.load(json_file)

# 去除每行的末尾换行符并生成SQL插入语句
sql_statements = []
with open(input_file_path, 'r', encoding='utf-8') as input_file, open(output_file_path, 'w',
                                                                      encoding='utf-8') as output_file:
    for i in range(0, 2000):
        original_type = str(i)
        done_type = class_indices.get(original_type, original_type)  # 默认映射为原始类型
        sql_statement = f"INSERT INTO real_type(original_type, done_type) VALUES('{original_type}', '{done_type}');"
        output_file.write(sql_statement + '\n')
        sql_statements.append(sql_statement)

# 将结果打印或写入文件
for statement in sql_statements:
    print(statement)

