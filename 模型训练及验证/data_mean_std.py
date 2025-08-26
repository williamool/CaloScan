import torch
from torchvision.datasets import ImageFolder
def getStart(train_data):
    print("Compute mean and variance for training data")
    print(len(train_data))
    train_loader = torch.utils.data.DataLoader(
        train_data, batch_size = 1, shuffle = False, num_workers = 0, pin_memory = True)
    #每个批次样本数，不打乱数据顺序，不使用额外进程，储存在CUDA固定内存中
    mean = torch.zeros(3) #RGB 一维张量
    std = torch.zeros(3)
    for X, _ in train_loader:
        for d in range(3):
            mean[d] += X[:, d, :, :].mean() #选择所有通道为d的数据并计算均值
            #批次中样本数，通道数，高宽
            std[d] += X[:, d, :, :].std()
    mean.div_(len(train_data))
    std.div_(len(train_data))
    return list(mean.numpy()), list(std.numpy())

if __name__ == '__main__':
    train_dataset = ImageFolder(root = 'dataset', transform = None)
    print(getStart(train_dataset))
