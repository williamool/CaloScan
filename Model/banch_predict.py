import os
import json

import torch
from PIL import Image
from torchvision import transforms

from model import resnet50


def main():
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    data_transform = transforms.Compose([transforms.RandomHorizontalFlip(p = 0.5),
                                        transforms.RandomRotation(degrees = 15),
                                        transforms.ColorJitter(brightness=0.126, saturation=0.5),
                                        transforms.Resize((550, 550)),
                                        transforms.RandomCrop(448),
                                        transforms.ToTensor(),
                                        transforms.Normalize([0.5457954, 0.44430383, 0.34424934], [0.23273608, 0.24383051, 0.24237761])])
    # 指向需要遍历预测的图像文件夹
    imgs_root = "../predict/imgs"
    assert os.path.exists(imgs_root), f"file: '{imgs_root}' dose not exist."
    # 读取指定文件夹下所有jpg图像路径 生成列表
    img_path_list = [os.path.join(imgs_root, i) for i in os.listdir(imgs_root) if i.endswith(".jpg")]
    '''
    for i in range(0, len(img_path_list)):
        print(img_path_list[i])
    '''

    # read class_indict
    json_path = './class_indices.json'
    assert os.path.exists(json_path), f"file: '{json_path}' dose not exist."

    json_file = open(json_path, "r")
    class_indict = json.load(json_file)

    # create model
    model = resnet50(num_classes=2000).to(device)

    # load model weights
    weights_path = "../food_resNet50.pth"
    assert os.path.exists(weights_path), f"file: '{weights_path}' dose not exist."
    model.load_state_dict(torch.load(weights_path, map_location=device))

    # prediction
    model.eval()
    batch_size = 2  # 每次预测时将多少张图片打包成一个batch
    with torch.no_grad():
        for ids in range(0, len(img_path_list) // batch_size + 1):
            img_list = []
            for img_path in img_path_list[ids * batch_size: (ids + 1) * batch_size]:
                assert os.path.exists(img_path), f"file: '{img_path}' dose not exist."
                img = Image.open(img_path)
                img = data_transform(img)
                img_list.append(img)

            # batch img
            # 将img_list列表中的所有图像打包成一个batch
            batch_img = torch.stack(img_list, dim=0)
            # predict class
            output = model(batch_img.to(device)).cpu()
            predict = torch.softmax(output, dim=1)
            probs, classes = torch.max(predict, dim=1)

            for idx, (pro, cla) in enumerate(zip(probs, classes)):
                print("image: {}  class: {}  prob: {:.3}".format(img_path_list[ids * batch_size + idx],
                                                                 class_indict[str(cla.numpy())],
                                                                 pro.numpy()))


if __name__ == '__main__':
    main()
