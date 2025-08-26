# coding: utf-8
import csv
import json
import os
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdklts.v2.region.lts_region import LtsRegion
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdklts.v2 import *
from datetime import datetime, timedelta
from figure import finalloop
from get_upload import uploadtoday

# 当前日期
current_date = datetime.utcnow().date()

# 当天0点的时间戳
start_of_day = int(datetime(current_date.year, current_date.month, current_date.day-5, 0, 0, 0).timestamp() * 1000)

# 当天23:59的时间戳
end_of_day = int(datetime(current_date.year, current_date.month, current_date.day, 23, 59, 59).timestamp() * 1000)


def deletdate(tian):
    output_file_path = 'data.csv'

    # 创建CSV文件并写入数据
    # 读取CSV文件，删除特定日期格式的行
    if os.path.exists(output_file_path):
        temp_file = output_file_path + '.tmp'
        with open(output_file_path, 'r', newline='', encoding='utf-8') as csvfile, \
                open(temp_file, 'w', newline='', encoding='utf-8') as tempcsvfile:

            csvreader = csv.reader(csvfile)
            csvwriter = csv.writer(tempcsvfile)

            for row in csvreader:
                if len(row) > 0 and not row[0].startswith(tian):  # 检查日期部分是否不是以'20240718'开头
                    csvwriter.writerow(row)

        # 移除旧文件并重命名临时文件为新文件
        os.remove(output_file_path)
        os.rename(temp_file, output_file_path)


if __name__ == "__main__":
    # The AK and SK used for authentication are hard-coded or stored in plaintext, which has great security risks. It is recommended that the AK and SK be stored in ciphertext in configuration files or environment variables and decrypted during use to ensure security.
    # In this example, AK and SK are stored in environment variables for authentication. Before running this example, set environment variables CLOUD_SDK_AK and CLOUD_SDK_SK in the local environment
    ak = os.environ["CLOUD_SDK_AK"]
    sk = os.environ["CLOUD_SDK_SK"]

    credentials = BasicCredentials(ak, sk)

    client = LtsClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(LtsRegion.value_of("cn-north-4")) \
        .build()

    try:
        request = ListLogsRequest()
        request.log_group_id = "af4a3084-d328-4998-9e85-00949fa07c66"
        request.log_stream_id = "d23666c4-41d6-41e4-8f6d-8d3719313868"
        request.body = QueryLtsLogParams(
            limit=5000,
            is_count=True,
            end_time=str(end_of_day),
            start_time=str(start_of_day)
        )
        response = client.list_logs(request)
        response_data = response.to_dict()
        json_data = json.dumps(response_data, indent=4)
        output_file_path = 'log_response.json'

        with open(output_file_path, 'w', encoding='utf-8') as json_file:
            json_file.write(json_data)
        #print(response)
    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)

    # 定义输入和输出文件路径
    input_file_path = 'log_response.json'
    output_file_path = 'extracted_data.csv'

    # 打开输入文件并读取内容
    with open('log_response.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 初始化一个列表来存储提取的信息
    extracted_info = []

    # 遍历logs列表
    for log in data["logs"]:
        #print(log)
        # 解析content字段中的JSON字符串
        content = json.loads(log["content"])
        #print(content)

        if content.get("request", {}) != None:
            requests = content.get("request", {})
            if "services" in requests:
                #print(requests)
                requests = json.loads(requests)
                if "services" in requests[0]:
                    services = requests[0]['services']
                    #print(services[0])
                else:
                    continue
                record_time = services[0]['eventTime']
                properties = services[0]['properties']
                if "ControlModule" in properties and properties['ControlModule']:
                    control_module = properties['ControlModule']
                else:
                    continue

               #print(control_module, record_time)
                extracted_info.append((record_time, control_module))

    # 打印提取的信息

    new_data = []
    seen = set()
    for item in extracted_info:
        if item not in seen and item[1] != 'HelloWorld!' and item[1][:11].isdigit():
            seen.add(item)
            new_data.append(item)
            # 如果new_data中元素数量超过20个，则取最后20个元素
    if len(new_data) > 1:
        new_data = new_data[-5:]

    # 1. 读取已有的CSV文件，提取所有日期
    existing_dates = set()  # 使用集合存储日期，避免重复
    if os.path.exists(output_file_path):
        with open(output_file_path, 'r', newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                if len(row) > 0:
                    existing_dates.add(row[0])  # 假设日期在CSV文件的第一列

    # 2. 确定要删除的日期
    dates_to_delete = set()
    for item in new_data:
        date = item[0][:8]  # 提取日期部分，假设日期在item的第一个元素中
        dates_to_delete.add(date)
    output_file_path = 'data.csv'
    unique_dates = list(set(dates_to_delete))
    print(unique_dates)

    for tianshu in unique_dates:
        deletdate(tianshu)
        # print(dates_to_delete)

    output_file_path = 'data.csv'

    # 追加新数据到已有 CSV 文件末尾
    with open(output_file_path, 'a', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        for item in new_data:
            first_four_reversed = item[1][:4][::-1].lstrip('0')  # 去除开头的零
            last_four = item[1][-4:]
            csvwriter.writerow([str(item[0]), first_four_reversed, last_four])
    print('日志解析完成')
    finalloop()
    print('分析完成')
    for tianshu in unique_dates:
        # 将字符串进行切片操作，形成新的日期格式
        formatted_date = f"{tianshu[:4]}-{tianshu[4:6]}-{tianshu[6:]}"
        uploadtoday(formatted_date)
        # print(dates_to_delete)
    print('上传完成')



   #print('shcnahu:',dates_to_delete)




