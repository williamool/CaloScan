# 打开原始数据文件
input_file_path = 'dishes_list.txt'
output_file_path = 'insert_statements.sql'

# 读取文件内容并转换为插入语句
with open(input_file_path, 'r', encoding='utf-8') as input_file, open(output_file_path, 'w',
                                                                      encoding='utf-8') as output_file:
    for line in input_file:
        # 去除前后的空格、花括号，并按逗号分割
        parts = line.strip().strip('{}').split(',')

        #print(parts)

        # 提取 index 和 name
        if len(parts) == 3:
            # 提取 index
            index_part = parts[0].split(':')
            #print(index_part)
            type_value = index_part[1].strip().strip("' ")
            #print(type_value)
            #else:
                #continue  # 如果格式不对，跳过这行

            # 提取 dish name
            dish_part = parts[1].split(':')
            #print(dish_part)
            dish = dish_part[1].strip().strip("' ")
            dish = dish[:-2]

            # 生成SQL插入语句
            insert_statement = f"INSERT INTO dishname(type, dish) VALUES('{type_value}', '{dish}');"

            # 写入到输出文件
            output_file.write(insert_statement + '\n')

print("SQL插入语句已生成并写入到文件：", output_file_path)
