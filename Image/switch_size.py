from PIL import Image

# 打开原始图片
img = Image.open("web1.png")

# 缩放到指定大小
resized_img = img.resize((1512, 860))

# 保存结果
resized_img.save("web1.png")
