# 假设文件名为 'Supplementary_tables.zh-CN.docx'
with open('D:\ResNet\get_str\dishes.txt', 'r', encoding='utf-8') as file:
    file_content = file.read()
    # 然后使用上面的脚本处理file_content变量
    # ...
# 假设文件内容已经被读取为一个单一的字符串变量，我们称之为file_content
# 这里我们使用提供的文件内容作为示例
# 使用换行符分割整个文件内容，得到每一行
lines = file_content.strip().split('\n')

# 初始化一个空列表来存储菜品信息
dishes_list = {}
ans = 0
# 遍历每一行
for line in lines:
    parts = line.split()
    for i, part in enumerate(parts):
        if i == 1 or i == 4:
            dishes_list[ans] = part
            ans = ans + 1
# 打印结果
for i in range(0, 2000):
    print(dishes_list[i])

with open('dishes_list.txt', 'w', encoding='utf-8') as f:
    for i in range(0, 2000):
        line = f"{{index: '{i}', name: '{dishes_list[i]}'}}" + ",\n"
        f.write(line)