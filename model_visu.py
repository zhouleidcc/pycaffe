# -*- coding: utf-8 -*-

import numpy as np
import os,sys,caffe
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig

caffe_root='./'
os.chdir(caffe_root)
sys.path.insert(0,caffe_root+'python')

plt.rcParams['figure.figsize'] = (8, 8)
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'

net = caffe.Net(caffe_root + 'cifar10_quick.prototxt',
                caffe_root + 'cifar10_quick_iter_5000.caffemodel',
                caffe.TEST)
[(k, v[0].data.shape) for k, v in net.params.items()]


# 编写一个函数，用于显示各层的参数
def show_feature(data, padsize=1, padval=0):
    data -= data.min()
    data /= data.max()

    # force the number of filters to be square
    n = int(np.ceil(np.sqrt(data.shape[0])))
    padding = ((0, n ** 2 - data.shape[0]), (0, padsize), (0, padsize)) + ((0, 0),) * (data.ndim - 3)
    data = np.pad(data, padding, mode='constant', constant_values=(padval, padval))

    # tile the filters into an image
    data = data.reshape((n, n) + data.shape[1:]).transpose((0, 2, 1, 3) + tuple(range(4, data.ndim + 1)))
    data = data.reshape((n * data.shape[1], n * data.shape[3]) + data.shape[4:])
    plt.imshow(data) # 设断点
    plt.axis('off')


# 第一个卷积层，参数规模为(32,3,5,5)，即32个5*5的3通道filter
weight = net.params["conv1"][0].data
# 参数有两种类型：权值参数和偏置项,分别用params["conv1"][0] 和params["conv1"][1] 表示
print weight.shape
show_feature(weight.transpose(0, 2, 3, 1))


# 第二个卷积层的权值参数，共有32*32个filter,每个filter大小为5*5
weight = net.params["conv2"][0].data
print weight.shape
show_feature(weight.reshape(32*32, 5, 5))

# 第三个卷积层的权值，共有64*32个filter,每个filter大小为5*5，取其前1024个进行可视化
weight = net.params["conv3"][0].data
print weight.shape
show_feature(weight.reshape(64*32,5,5))



