import sys
sys.path.insert(0,'.')
import torch
from torch.autograd import Variable #用于 PyTorch 的张量操作和自动微分
from torchvision.models import resnet
import pytorch_to_caffe

if __name__=='__main__':
    name='/home/hispark/resnet18'
    resnet18=resnet.resnet18(num_classes=13)
    checkpoint = torch.load("/ai/pytorch_to_caffe_master/epoch_100.pth", map_location = 'cpu')
    new_sd = {}
    for k,v in checkpoint['state_dict'].items():
        if not k.endswith('num_batches_tracked'):
            if k.startswith('backbone'):
                k_new = k.split('backbone.')[1]
            if k.startswith('head'):
                k_new = k.split('head.')[1]
            new_sd[k_new] = v

    resnet18.load_state_dict(new_sd)
    resnet18.eval()
    input=torch.ones([1,3,224,224])
     #input=torch.ones([1,3,224,224])
    pytorch_to_caffe.trans_net(resnet18,input,name)
    pytorch_to_caffe.save_prototxt('{}.prototxt'.format(name))
    pytorch_to_caffe.save_caffemodel('{}.caffemodel'.format(name))
