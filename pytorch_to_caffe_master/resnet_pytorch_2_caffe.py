import sys
sys.path.insert(0,'.')
import torch
from torch.autograd import Variable #用于 PyTorch 的张量操作和自动微分
from torchvision.models import resnet
import pytorch_to_caffe

if __name__=='__main__':
    name='/ResNet/done_train/resnet50' #设置导出的 Caffe 模型的基础文件名
    resnet50=resnet.resnet50(num_classes=2000) #创建一个具有 2000 个类别输出的 ResNet-50 模型实例
    loaded_state_dict = torch.load('../done_train/food_ResNet50.pth')
    '''
    checkpoint = torch.load("/ResNet/food_ResNet50.pth", map_location = 'cpu')
    #加载一个保存的模型检查点文件到 CPU 内存中。
    new_sd = {}
    for k,v in checkpoint['state_dict'].items(): #从加载的检查点文件中提取模型的状态字典，这是一个包含模型所有参数和权重的字典
        if not k.endswith('num_batches_tracked'): #是在 BatchNorm 层中用于跟踪批次数的参数，这对于推理或转换模型来说不是必须的，因此可以忽略
            if k.startswith('backbone'):
                k_new = k.split('backbone.')[1] #如果键名以backbone开头，使用分割方法按backbone.分割，取分割后的第二部分（即去掉 backbone. 前缀的部分）作为新的键名
            if k.startswith('head'):
                k_new = k.split('head.')[1] #处理以 head 开头的键名，head 通常用于表示分类头或其他任务特定的网络层。
            new_sd[k_new] = v #将处理后的键 k_new 和对应的值 v 加入新的状态字典 new_sd 中
    '''
    resnet50.load_state_dict(loaded_state_dict) #将新的状态字典加载到 ResNet-50
    resnet50.eval() #将模型设置为评估模式
    input=torch.ones([1,3,224,224]) #创建一个形状为 [1, 3, 448, 448] 的全为 1 的张量，作为模型的输入。
     #input=torch.ones([1,3,448,448])
    pytorch_to_caffe.trans_net(resnet50,input,name) #使用 pytorch_to_caffe 工具将 ResNet-50 模型和输入张量转换为 Caffe 格式
    pytorch_to_caffe.save_prototxt('{}.prototxt'.format(name)) #保存转换后的 Caffe 模型结构文件（.prototxt）
    pytorch_to_caffe.save_caffemodel('{}.caffemodel'.format(name)) #保存转换后的 Caffe 模型权重文件（.caffemodel）
