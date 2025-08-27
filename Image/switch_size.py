from PIL import Image

# 打开原始图片
img = Image.open("program6.png")

# 缩放到指定大小
resized_img = img.resize((871, 1888))

# 保存结果
resized_img.save("program6.png")
