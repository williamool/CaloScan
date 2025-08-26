import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np
from scipy.spatial.distance import cosine
caidenames = [
    "拿破仑蛋糕",
    "烤兔肉",
    "双椒蒸鱼头",
    "绿豆汤",
    "广式腊肠炒饭",
    "蒜蓉烤茄子",
    "草莓圣代",
    "蒜蓉菜心",
    "荷叶蒸鸡",
    "椰子冻",
    "红烧肉饭",
    "猪肝面",
    "青椒炒渣渣",
    "炒腊肉炒笋",
    "烤明虾",
    "无骨鸡爪",
    "炸鸡排",
    "番茄鸡蛋汤",
    "蒜蓉粉丝蒸鲍鱼",
    "盐水鸡",
    "油泼面",
    "酸菜鱼米线",
    "炸羊排",
    "麻婆豆腐",
    "腌鹅翅",
    "素鲍鱼",
    "煎饺",
    "意大利肉酱面",
    "馄饨",
    "大黄鱼",
    "水煮牛肉",
    "板栗",
    "煮鸡蛋",
    "烤鸡翅",
    "红烧肉",
    "萝卜猪骨汤",
    "肉末茄子",
    "红烧排骨",
    "蒙古烤全羊",
    "炒花菜",
    "拍黄瓜",
    "红烧牛肉",
    "芋头鸡",
    "老虎青椒",
    "豌豆炒培根",
    "烤扇贝",
    "韭菜炒蛋",
    "豆腐米线",
    "毛豆煮",
    "冬瓜排骨汤",
    "盐煎杏鲍菇",
    "鱼香茄子饭",
    "小米绿豆粥",
    "鸭肝",
    "蒸排骨糯米饭",
    "红烧牛肉面",
    "芋头蒸排骨",
    "番茄牛肉面",
    "叫花鸡",
    "白肉煮",
    "红烧茄子",
    "鲤鱼",
    "大蒜西兰花",
    "薯条",
    "金枪鱼沙拉",
    "蜜汁鸡翅",
    "猪脚饭",
    "红烧肉",
    "辣黄瓜",
    "炸里脊",
    "清蒸鲈鱼",
    "手撕鸡",
    "炸云吞",
    "蘑菇鸡肉粥",
    "蛋黄龙虾",
    "酸奶",
    "纸上烤鱼",
    "萝卜牛肉",
    "白切咸水鸭",
    "酸菜烤鱼",
    "炸猪排",
    "纯肠",
    "香煎鹅肝",
    "卤兔头",
    "新奥尔良烤整腿",
    "铁板排骨虾",
    "牛肉面",
    "胡萝卜丁",
    "茄子煲",
    "牛尾汤",
    "蒸蛋",
    "爆炒虾仁",
    "蒜苔炒腊肉",
    "炸豆腐",
    "宫保牛蛙",
    "香辣牛肉面",
    "牛角面包",
    "红烧羊肉",
    "咸鸭蛋"
]
reference_vector = np.array([
    2500,   # 热量，单位：千卡
    65,     # 蛋白质（克）
    300,    # 碳水化合物（克）
    25,     # 膳食纤维（总量）（克）
    70,     # 总脂肪（克）
    800,    # 维生素 A，RAE（微克）
    1.2,    # 维生素 B-6（毫克）
    2.4,    # 维生素 B-12（微克）
    100,    # 维生素 C（毫克）
    15,     # 维生素 D（D2 + D3）（微克）
    15,     # 维生素 E（α-生育酚）（毫克）
    120,    # 维生素 K（类胡萝卜素）（微克）
    1000,   # 钙（毫克）
    700,    # 磷（毫克）
    350,    # 镁（毫克）
    15,     # 铁（毫克）
    12,     # 锌（毫克）
    1.5,    # 铜（毫克）
    70,     # 硒（微克）
    3500,   # 钾（毫克）
    2300,   # 钠（毫克）
    2500    # 水，单位：毫升
])
plt.rcParams['font.sans-serif'] = ['SimHei']  # 将'SimHei'替换为你希望使用的中文字体，例如'SimSun'、'Microsoft YaHei'等
plt.rcParams['axes.unicode_minus'] = False  # 解决负号'-'显示为方块的问题


# 显示结果
#print(df['时间'])
import pandas as pd

# 指定CSV文件路径
file_path = 'test.csv'

# 读取CSV文件
df = pd.read_csv(file_path)

# 预期的表头列表
expected_headers = [
    'nunber', 'name', 'calo', 'Protein (g)', 'Carbohydrate(g)',
    "Fiber, total dietary ????(g)", 'Total Fat ??(g)',
    "Vitamin A, RAE (mcg_RAE)?A", "Vitamin B-6 (mg)", "Vitamin B-12 (mcg)",
    "Vitamin C (mg)", "Vitamin D (D2 + D3) (mcg)", "Vitamin E (alpha-tocopherol) (mg)",
    "Vitamin K (phylloquinone) (mcg)", "Calcium (mg)", "Phosphorus (mg)",
    "Magnesium (mg)", "Iron (mg)", "Zinc (mg)", "Copper (mg)", "Selenium (mcg)",
    "Potassium (mg)", "Sodium (mg)", "water"
]

# 检查表头是否符合预期
if df.columns.tolist() != expected_headers:
    print("Headers in CSV do not match expected headers.")
    # 如果表头不匹配，可以选择打印出实际的表头进行核对
    print("Actual headers:", df.columns.tolist())
else:
    # 表头匹配，将数据读取到对应表头名的一维变量中
    number = df['nunber'].values
    name = df['name'].values
    calo = df['calo'].values
    protein_g = df['Protein (g)'].values
    carbohydrate_g = df['Carbohydrate(g)'].values
    fiber_g = df["Fiber, total dietary ????(g)"].values
    total_fat_g = df['Total Fat ??(g)'].values
    vitamin_a_mcgRAE = df["Vitamin A, RAE (mcg_RAE)?A"].values
    vitamin_b6_mg = df["Vitamin B-6 (mg)"].values
    vitamin_b12_mcg = df["Vitamin B-12 (mcg)"].values
    vitamin_c_mg = df["Vitamin C (mg)"].values
    vitamin_d_mcg = df["Vitamin D (D2 + D3) (mcg)"].values
    vitamin_e_mg = df["Vitamin E (alpha-tocopherol) (mg)"].values
    vitamin_k_mcg = df["Vitamin K (phylloquinone) (mcg)"].values
    calcium_mg = df["Calcium (mg)"].values
    phosphorus_mg = df["Phosphorus (mg)"].values
    magnesium_mg = df["Magnesium (mg)"].values
    iron_mg = df["Iron (mg)"].values
    zinc_mg = df["Zinc (mg)"].values
    copper_mg = df["Copper (mg)"].values
    selenium_mcg = df["Selenium (mcg)"].values
    potassium_mg = df["Potassium (mg)"].values
    sodium_mg = df["Sodium (mg)"].values
    water = df['water'].values
    #cname = df['cname'].values

    # 打印变量以检查结果（可选）
    #print("Number of entries:", len(number))
    # 可以继续打印其他变量以验证它们的内容
    #print("Calo:",  number)
import pandas as pd

import pandas as pd

# 指定CSV文件路径
file_path = 'data.csv'


df = pd.read_csv(file_path, usecols=[0, 1, 2])  # 只读取前3列


df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0], format='%Y-%m-%d %H:%M:%S')

# 根据日期分组
grouped = df.groupby(df.iloc[:, 0].dt.date)

# 创建一个空的二维数组来存储结果
result = []

# 遍历分组并将每一天的数据保存为新的二维数组
for date, group in grouped:
    day_data = group.values.tolist()
    result.append(day_data)

#print(result[0])




def calculate_nutrient_values(food_number, weight):
    weight = weight / 100
    indices = [i for i, x in enumerate(number) if x == food_number]  # 假设 food_number_list 是你的食物编号列表
    if not indices:
        indices=1
          # 如果找不到食物编号，返回 None

    nutrient_values = [
        calo[indices[0]] * weight,
        protein_g[indices[0]] * weight,
        carbohydrate_g[indices[0]] * weight,
        fiber_g[indices[0]] * weight,
        total_fat_g[indices[0]] * weight,
        vitamin_a_mcgRAE[indices[0]] * weight,
        vitamin_b6_mg[indices[0]] * weight,
        vitamin_b12_mcg[indices[0]] * weight,
        vitamin_c_mg[indices[0]] * weight,
        vitamin_d_mcg[indices[0]] * weight,
        vitamin_e_mg[indices[0]] * weight,
        vitamin_k_mcg[indices[0]] * weight,
        calcium_mg[indices[0]] * weight,
        phosphorus_mg[indices[0]] * weight,
        magnesium_mg[indices[0]] * weight,
        iron_mg[indices[0]] * weight,
        zinc_mg[indices[0]] * weight,
        copper_mg[indices[0]] * weight,
        selenium_mcg[indices[0]] * weight,
        potassium_mg[indices[0]] * weight,
        sodium_mg[indices[0]] * weight,
        water[indices[0]] * weight
    ]
    return nutrient_values





def calculate_total_nutrients_for_day(i):

    # 初始化总营养素向量，假设有22种营养素
    total_nutrients = [0] * 22

    # 遍历那一天的所有饮食记录
    for meal in result[i]:
        # 计算本次摄入的营养素向量
        nutrient_values = calculate_nutrient_values(meal[1], meal[2])

        # 确保nutrient_values的长度与total_nutrients相同
        if len(nutrient_values) == len(total_nutrients):
            # 累加营养素到总向量
            total_nutrients = [x + y for x, y in zip(total_nutrients, nutrient_values)]
        else:
            raise ValueError("营养素向量长度不匹配")

    return total_nutrients
#print(calculate_total_nutrients_for_day( 1))

total_nutrient=calculate_total_nutrients_for_day( 0)


# 营养素的名称（中文）
nutrients_dic = ['热量', '蛋白质（克）', '碳水化合物（克）', '膳食纤维（总量）（克）', '总脂肪（克）',
             '维生素 A，RAE（微克）', '维生素 B-6（毫克）', '维生素 B-12（微克）', '维生素 C（毫克）',
             '维生素 D（D2 + D3）（微克）', '维生素 E（α-生育酚）（毫克）', '维生素 K（类胡萝卜素）（微克）',
             '钙（毫克）', '磷（毫克）', '镁（毫克）', '铁（毫克）', '锌（毫克）', '铜（毫克）',
             '硒（微克）', '钾（毫克）', '钠（毫克）', '水']


# 营养素的名称（中文）
nutrients_dic = ['热量', '蛋白质（克）', '碳水化合物（克）', '膳食纤维（总量）（克）', '总脂肪（克）',
             '维生素 A，RAE（微克）', '维生素 B-6（毫克）', '维生素 B-12（微克）', '维生素 C（毫克）',
             '维生素 D（D2 + D3）（微克）', '维生素 E（α-生育酚）（毫克）', '维生素 K（类胡萝卜素）（微克）',
             '钙（毫克）', '磷（毫克）', '镁（毫克）', '铁（毫克）', '锌（毫克）', '铜（毫克）',
             '硒（微克）', '钾（毫克）', '钠（毫克）', '水']
def zhuzhuangtuplot():
    # 营养素的值（假设这是你的数据）
    total_nutrient_values = total_nutrient
    # 误差统计
    difference = (total_nutrient_values - reference_vector) / reference_vector

    # 创建柱状图
    plt.figure(figsize=(12, 8))
    plt.barh(nutrients_dic, difference, color='skyblue')
    plt.xlabel('营养素值')
    plt.title('不同营养素的柱状图')
    plt.gca().invert_yaxis()  # 反转 y 轴，使得第一个营养素在顶部
    plt.show()



    # 计算余弦相似度
    cosine_similarity = 1 - cosine(total_nutrient_values, reference_vector)

    print(f"余弦相似度: {cosine_similarity}")
    print(reference_vector)
    print(total_nutrient)
    print(difference)

def radarplot(data_dicts, data_labels, plot_title,day,performance):
    performance=round(100*performance)
    # 假设 result 是一个包含 Timestamp 对象的 DataFrame 或 Series
    datetime_obj = result[day][0][0]

    # 使用 Pandas 的方法将 Timestamp 对象转换为日期字符串
    date_str = datetime_obj.strftime('%Y-%m-%d')
    # 初始化一个雷达图的角度
    labels = np.array(list(data_dicts[0].keys()))
    num_vars = len(labels)

    # 计算角度
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    # 使图形闭合
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    # 画每一组数据
    for data_dict, label in zip(data_dicts, data_labels):
        data = list(data_dict.values())

        # 归一化数据
        data = np.array(data)
        data = np.concatenate((data, [data[0]]))

        ax.fill(angles, data, alpha=0.25, label=label)
        ax.plot(angles, data, linewidth=2, label=label)

    # 添加指标名称
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

    full_title = f'{date_str} {plot_title}'

    # 修改标题


    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.subplots_adjust(right=0.75)  # 根据实际情况调整
    plt.title(full_title)
    # 添加 performance 到图像下方
    plt.figtext(0.5, 0.05, f'{plot_title}得分: {performance}', ha='center', fontsize=10)

    # 创建以日期命名的文件夹
    folder_path = f'./{date_str}/'
    os.makedirs(folder_path, exist_ok=True)  # 如果文件夹不存在，则创建

    # 构造保存路径，并保存图像
    save_path = os.path.join(folder_path, f'{plot_title}_day{date_str}.png')
    plt.savefig(save_path)



def Tripleradarplot(day):
    total_nutrient=calculate_total_nutrients_for_day(day)
    # 数据集的标签
    data_labels = ['实际摄入','实际摄入']

    # 给定的名字列表
    names = ['热量', '蛋白质（克）', '碳水化合物（克）', '膳食纤维（总量）（克）', '总脂肪（克）',
             '维生素 A，RAE（微克）', '维生素 B-6（毫克）', '维生素 B-12（微克）', '维生素 C（毫克）',
             '维生素 D（D2 + D3）（微克）', '维生素 E（α-生育酚）（毫克）', '维生素 K（类胡萝卜素）（微克）',
             '钙（毫克）', '磷（毫克）', '镁（毫克）', '铁（毫克）', '锌（毫克）', '铜（毫克）',
             '硒（微克）', '钾（毫克）', '钠（毫克）', '水']

    # 对应的数值列表

    # 创建字典

    names_slice = names[0:5]
    total_nutrient_main = total_nutrient[0:5]
    reference_vector_main = reference_vector[0:5]
    # 计算余弦相似度
    cosine_similarity= assess(total_nutrient_main, reference_vector_main)

    # 创建 nutrient_dict1 和 nutrient_dict2，只使用前五个元素
    nutrient_dict1 = dict(zip(names_slice, total_nutrient_main/reference_vector_main))
    nutrient_dict2 = dict(zip(names_slice, reference_vector_main/reference_vector_main))

    finaldict = []  # 假设 finaldict 是一个空列表

    # 将 nutrient_dict 添加到 finaldict 中
    finaldict.append(nutrient_dict1)
    finaldict.append(nutrient_dict2)

    radarplot(finaldict, data_labels,'今日基本营养素摄入量',day,cosine_similarity)

    names_slice = names[6:12]
    total_nutrient_main = total_nutrient[6:12]
    reference_vector_main = reference_vector[6:12]
    cosine_similarity= assess(total_nutrient_main, reference_vector_main)

    # 创建 nutrient_dict1 和 nutrient_dict2，只使用前五个元素
    nutrient_dict1 = dict(zip(names_slice, total_nutrient_main / reference_vector_main))
    nutrient_dict2 = dict(zip(names_slice, reference_vector_main / reference_vector_main))

    finaldict = []  # 假设 finaldict 是一个空列表

    # 将 nutrient_dict 添加到 finaldict 中
    finaldict.append(nutrient_dict1)
    finaldict.append(nutrient_dict2)

    radarplot(finaldict, data_labels, '今日基本维生素摄入量',day,cosine_similarity)

    names_slice = names[13:21]
    total_nutrient_main = total_nutrient[13:21]
    reference_vector_main = reference_vector[13:21]
    cosine_similarity= assess(total_nutrient_main, reference_vector_main)

    # 创建 nutrient_dict1 和 nutrient_dict2，只使用前五个元素
    nutrient_dict1 = dict(zip(names_slice, total_nutrient_main / reference_vector_main))
    nutrient_dict2 = dict(zip(names_slice, reference_vector_main / reference_vector_main))

    finaldict = []  # 假设 finaldict 是一个空列表

    # 将 nutrient_dict 添加到 finaldict 中
    finaldict.append(nutrient_dict1)
    finaldict.append(nutrient_dict2)

    radarplot(finaldict, data_labels, '今日基本微量元素摄入量',day,cosine_similarity)




def assess(actual,refernce):
    coss=1 - cosine(actual,refernce)
    # 计算绝对值误差
    abs_error = np.abs(actual - refernce)

    # 计算相对误差，可以考虑使用绝对值的大小
    rel_error = np.mean(abs_error / refernce)

    # 综合考虑余弦相似度和绝对误差
    combined_score = coss * (1 - rel_error*0.3)


    return combined_score

def judge(day):
    total_nutrient = calculate_total_nutrients_for_day(day)


    # 对应的数值列表

    # 创建字典


    total_nutrient_main = total_nutrient[0:5]
    reference_vector_main = reference_vector[0:5]
    # 计算余弦相似度
    cosine_similarity1= assess(total_nutrient_main, reference_vector_main)




    total_nutrient_main = total_nutrient[6:12]
    reference_vector_main = reference_vector[6:12]
    cosine_similarity2 =  assess(total_nutrient_main, reference_vector_main)




    total_nutrient_main = total_nutrient[13:21]
    reference_vector_main = reference_vector[13:21]
    cosine_similarity3 = assess(total_nutrient_main, reference_vector_main)

    judge_result=(cosine_similarity1+cosine_similarity2+cosine_similarity3)/3
    judge_result=round(1000*judge_result)/10

    return judge_result


def searchjudge(nutrient_vector):
    total_nutrient = nutrient_vector

    # 对应的数值列表

    # 创建字典

    total_nutrient_main = total_nutrient[0:5]
    reference_vector_main = reference_vector[0:5]
    # 计算余弦相似度
    cosine_similarity1 = assess(total_nutrient_main, reference_vector_main)

    total_nutrient_main = total_nutrient[6:12]
    reference_vector_main = reference_vector[6:12]
    cosine_similarity2 = assess(total_nutrient_main, reference_vector_main)

    total_nutrient_main = total_nutrient[13:21]
    reference_vector_main = reference_vector[13:21]
    cosine_similarity3 = assess(total_nutrient_main, reference_vector_main)

    judge_result = (cosine_similarity1 + cosine_similarity2 + cosine_similarity3) / 3
    judge_result = round(1000 * judge_result) / 10

    return judge_result










dates = []
judge_results = []
yingyangsu = []

for i in range(len(result)):
    datetime_obj = result[i][0][0]  # 获取日期时间对象
    date_str = datetime_obj.strftime('%Y-%m-%d')  # 格式化日期字符串
    dates.append(date_str)  # 收集日期字符串
    judge_result = judge(i)  # 收集judge函数的结果
    judge_results.append(judge_result)
    yingyangsu.append(calculate_total_nutrients_for_day(i))

    # 绘制 Tripleradarplot 等其他必要的图形
    #Tripleradarplot(i)

    # 打印 judge(i) 的结果
    #print(judge(i))

import matplotlib.pyplot as plt


# 假设dates和judge_results是全局变量或在函数外部定义
# dates和judge_results应该是列表或类似结构，存储了日期和对应的得分

# 调用函数，传入天数参数



def searchfood(mean_yys):
    mean_yys = np.array(mean_yys)
    defens = []  # 用于存储每个 food_number 对应的 defen
    for food_number in number:
        total_yys = mean_yys + calculate_nutrient_values(food_number, 200)
        #print(total_yys)

        defen = searchjudge(total_yys)
        #print(defen)

        defens.append((food_number, defen))  # 存储 food_number 和对应的 defen

    # 按照 defen 的值降序排序
    defens.sort(key=lambda x: x[1], reverse=True)

    # 获取前五个 defen 最高的 food_number
    top_food_numbers = [defen[0] for defen in defens[:5]]

    return top_food_numbers






#index = searchfood(calculate_total_nutrients_for_day(6))

# 打印出caidenames[index]的值
#for i in index:
    #print("caidenames[{}] 的值是: {}".format(i, caidenames[i]))



def historyanalyze(day):

    # 假设 result 是一个包含 Timestamp 对象的 DataFrame 或 Series
    datetime_obj = result[day][0][0]

    # 使用 Pandas 的方法将 Timestamp 对象转换为日期字符串
    date_str = datetime_obj.strftime('%Y-%m-%d')
    # 计算索引范围
    low = max(day - 7, 0)  # 确保low不小于0
    up = day
    sums = [0] * 22  # 创建一个长度为22的列表，初始化所有元素为0
    for nutrient_array in yingyangsu[low:up + 1]:
        for i in range(22):  # 对每个元素求和
            sums[i] += nutrient_array[i]

    # 计算均值
    meanyys = [x / (up - low + 1) for x in sums]
    #print(meanyys)

    # 绘制折线图
    plt.figure(figsize=(10, 5))  # 可以调整图形的大小
    plt.plot(dates[low:up + 1], judge_results[low:up + 1], marker='o')  # 使用切片来选择一个范围内的元素

    # 设置图表标题和标签
    plt.title('近七日历史饮食营养得分')
    plt.xlabel('日期')
    plt.ylabel('得分情况')

    # 添加网格
    plt.grid(True)

    # 在每个点上标注数值
    for (date, y) in zip(dates[low:up + 1], judge_results[low:up + 1]):
        plt.text(date, y, f'{y:.2f}', ha='right')  # 格式化为保留两位小数，并水平对齐文本在点的右侧

    # 旋转日期标签以便阅读
    plt.xticks(rotation=45)

    # 显示图例
    plt.legend(['综合评分'], loc='best')

    # 显示图形
    plt.tight_layout()  # 自动调整子图参数，使之填充整个图像区域
    # 创建以日期命名的文件夹
    folder_path = f'./{date_str}/'
    os.makedirs(folder_path, exist_ok=True)  # 如果文件夹不存在，则创建
    plot_title_temp='七日历史饮食记录'

    # 构造保存路径，并保存图像
    save_path = os.path.join(folder_path, f'{plot_title_temp}_day{date_str}.png')
    plt.savefig(save_path)

    meanyys = [round(item) for item in meanyys]

    # 设置柱状图的宽度
    bar_width = 0.4

    # 生成每组柱状图的位置
    index = np.arange(len(nutrients_dic))

    # 创建柱状图
    plt.figure(figsize=(12, 8))
    # 根据条件设置颜色
    colors = ['red' if meanyys[i] < 0.75 * reference_vector[i] else 'skyblue' for i in range(len(reference_vector))]

    # 绘制参考摄入量的柱状图
    bars1 = plt.barh(index - bar_width / 2, reference_vector/reference_vector, bar_width, color='lightgreen', label='参考摄入量')

    # 绘制平均摄入量的柱状图
    bars2 = plt.barh(index + bar_width / 2, meanyys/reference_vector, bar_width, color=colors, label='平均摄入量')

    # 在柱状图上标注具体值
    for bars in [bars1, bars2]:
        for bar, value in zip(bars, reference_vector if bars is bars1 else meanyys):
            plt.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f'{value}',
                     va='center', ha='left', fontsize=12)

    plt.xlabel('营养素值')
    plt.title('不同营养素的柱状图')
    plt.yticks(index, nutrients_dic)
    plt.gca().invert_yaxis()  # 反转 y 轴，使得第一个营养素在顶部
    plt.legend()
    plt.tight_layout()

    # 创建以日期命名的文件夹
    folder_path = f'./{date_str}/'
    os.makedirs(folder_path, exist_ok=True)  # 如果文件夹不存在，则创建
    plot_title_temp = '七日营养素柱状图'

    # 构造保存路径，并保存图像
    save_path = os.path.join(folder_path, f'{plot_title_temp}_day{date_str}.png')
    plt.savefig(save_path)

    # 计算差异比例
    ratios = meanyys / reference_vector

    # 找出小于0.75或大于2的索引
    low_nutrients_indices = np.where(ratios < 0.25)[0]  # 缺少的营养素索引
    high_nutrients_indices = np.where(ratios > 2)[0]  # 过量摄入的营养素索引



    index = searchfood(calculate_total_nutrients_for_day(day))



    # 创建图表
    fig, ax = plt.subplots(figsize=(10, 6))  # 可以根据需要调整图表大小

    ax.text(0.5, 0.0, "缺少的营养素：\n" + "\n".join(f"- {nutrients_dic[i]}" for i in low_nutrients_indices) +
            "\n\n过量摄入的营养素：\n" + "\n".join(f"- {nutrients_dic[i]}" for i in high_nutrients_indices) +
            "\n\n健康食谱推荐：\n" + "\n".join(f"推荐的食谱是: {caidenames[i]}" for i in index),
            horizontalalignment='center', fontsize=18, transform=ax.transAxes)

    # 隐藏坐标轴
    ax.axis('off')

    # 调整图表布局
    plt.subplots_adjust(left=0.3, right=0.7, top=0.9, bottom=0.1)

    # 保存图表为图片
    #plt.savefig('nutrients_report.png', dpi=300, bbox_inches='tight')

    folder_path = f'./{date_str}/'
    os.makedirs(folder_path, exist_ok=True)  # 如果文件夹不存在，则创建
    plot_title_temp = '当日饮食建议'

    # 构造保存路径，并保存图像
    save_path = os.path.join(folder_path, f'{plot_title_temp}_day{date_str}.png')
    plt.savefig(save_path)



#historyanalyze(4)

#print(reference_vector+nutrient_values)
def finalloop():
    last_index = len(result) - 1
    for i in range(last_index-1, last_index + 1):
        Tripleradarplot(i)
        historyanalyze(i)  # 获取日期时间对象


#Tripleradarplot(0)
#historyanalyze(0)

#print(caidenames[6])
#print(caidenames[28])
#print(caidenames[29])
#print(caidenames[31])

#finalloop()




