import os
import sys
import json

import PIL
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import transforms, datasets
from tqdm import tqdm
from PIL import UnidentifiedImageError
from PIL import Image

from model import resnet50
import torchvision.models.resnet

def main():
    #选择学习设备
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print("using {} device".format(device))

    data_transform = {
        "train": transforms.Compose([transforms.RandomHorizontalFlip(p = 0.5),
                                     transforms.RandomRotation(degrees = 15),
                                     transforms.ColorJitter(brightness=0.126, saturation=0.5),
                                     transforms.Resize((550, 550)),
                                     transforms.RandomCrop(448),
                                     transforms.ToTensor(),
                                     transforms.Normalize([0.5457954, 0.44430383, 0.34424934], [0.23273608, 0.24383051, 0.24237761])]),
        "val": transforms.Compose([transforms.Resize((550, 550)),
                                   transforms.RandomCrop(448),
                                   transforms.ToTensor(),
                                   transforms.Normalize([0.5457954, 0.44430383, 0.34424934],[0.23273608, 0.24383051, 0.24237761])])
    }
    data_root = os.path.abspath(os.getcwd())
    image_path = os.path.join(data_root, "dataset")
    assert os.path.exists(image_path), "{} path does not exist.".format(image_path)

    train_dataset = datasets.ImageFolder(root = os.path.join(image_path, "train"),
                                         transform = data_transform["train"])
    train_num = len(train_dataset)

    food_list = train_dataset.class_to_idx
    cla_dict = dict((val, key) for key, val in food_list.items())

    json_str = json.dumps(cla_dict, indent = 4)
    with open('class_indices.json', 'w') as json_file:
        json_file.write(json_str)

    batch_size = 8
    nw = 8
    print('Using {} dataloader workers every process'.format(nw))

    train_loader = torch.utils.data.DataLoader(train_dataset,
                                               batch_size = batch_size, shuffle = True,
                                               num_workers = nw)

    validate_dataset = datasets.ImageFolder(root = os.path.join(image_path, "val"),
                                            transform = data_transform["val"])

    val_num = len(validate_dataset)
    validate_loader = torch.utils.data.DataLoader(validate_dataset,
                                                  batch_size = batch_size, shuffle = True,
                                                  num_workers = nw)
    print("using {} image for training, {} images for validation".format(train_num, val_num))

    net = resnet50()

    model_weight_path = "./food_resnet50_pre.pth"
    net.cuda()
    net.load_state_dict(torch.load(model_weight_path))
    '''
    assert os.path.exists(model_weight_path), "file {} does not exist.".format(model_weight_path)
    net.load_state_dict(torch.load(model_weight_path, map_location = 'cpu'))  # 加载预训练的ResNet-50模型权重，并应用到net模型中
    '''

    in_channel = net.fc.in_features
    net.fc = nn.Linear(in_channel, 2000)
    net.to(device)

    loss_function = nn.CrossEntropyLoss()

    params = [p for p in net.parameters() if p.requires_grad]
    optimizer = optim.Adam(params, lr = 0.0001)

    train_error = 0
    validate_error = 0
    epochs = 200
    best_acc = 0.0
    save_path = '/food_ResNet50.pth'
    train_steps = len(train_loader)
    for epoch in range(epochs):
        net.train()
        running_loss = 0.0
        train_bar = tqdm(train_loader, file = sys.stdout)
        for step, data in enumerate(train_bar):
            try:
                images, labels = data
                optimizer.zero_grad()
                logits = net(images.to(device))
                loss = loss_function(logits, labels.to(device))
                loss.backward()
                optimizer.step()

                running_loss += loss.item()

                train_bar.desc = "train epoch[{}/{}] loss:{:.3f}".format(epoch + 1,
                                                                        epochs,
                                                                        loss)
            except PIL.UnidentifiedImageError as e:
                continue

        net.eval()
        acc = 0.0
        with torch.no_grad():
            val_bar = tqdm(validate_loader, file = sys.stdout)
            for val_data in val_bar:
                try:
                    val_images, val_labels = val_data
                    outputs = net(val_images.to(device))
                    predict_y = torch.max(outputs, dim = 1)[1]
                    acc += torch.eq(predict_y, val_labels.to(device)).sum().item()

                    val_bar.desc = "valid epoch[{}/{}]".format(epoch + 1,
                                                               epochs)
                except PIL.UnidentifiedImageError as e:
                    print("An ")
                    continue

        val_accurate = acc / val_num
        print('[epoch %d] train_loss: %.3f  val_accuracy: %.3f' %
              (epoch + 1, running_loss / train_steps, val_accurate))

        if val_accurate > best_acc:
            best_acc = val_accurate
            torch.save(net.state_dict(), save_path)

        print("Finished Training")

if __name__ == '__main__':
    main()