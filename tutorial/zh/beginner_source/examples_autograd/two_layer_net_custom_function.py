# -*- coding: utf-8 -*-
"""
PyTorch: Defining new autograd functions
----------------------------------------

A fully-connected ReLU network with one hidden layer and no biases, trained to
predict y from x by minimizing squared Euclidean distance.

This implementation computes the forward pass using operations on PyTorch
Variables, and uses PyTorch autograd to compute gradients.

In this implementation we implement our own custom autograd function to perform
the ReLU function.
"""
import torch
from torch.autograd import Variable


class MyReLU(torch.autograd.Function):
    """
    我们可以通过子类实现我们自己定制的autograd函数
    torch.autograd.Function和执行在Tensors上运行的向前和向后通行证.
    """

    @staticmethod
    def forward(ctx, input):
        """
        在正向传递中,我们收到一个包含输入和返回张量的张量,其中包含输出.
        ctx是一个上下文对象,可用于存储反向计算的信息.
        您可以使用ctx.save_for_backward方法缓存任意对象以用于后向传递.
        """
        ctx.save_for_backward(input)
        return input.clamp(min=0)

    @staticmethod
    def backward(ctx, grad_output):
        """
        在后向传递中,我们收到一个张量,其中包含相对于输出的损失梯度,
        我们需要计算相对于输入的损失梯度.
        """
        input, = ctx.saved_tensors
        grad_input = grad_output.clone()
        grad_input[input < 0] = 0
        return grad_input


dtype = torch.FloatTensor
# dtype = torch.cuda.FloatTensor # 取消注释以在GPU上运行

# N 是一个batch的样本数量; D_in是输入维度;
# H 是隐藏层向量的维度; D_out是输出维度.
N, D_in, H, D_out = 64, 1000, 100, 10

# 创建随机张量来保存输入和输出,并将它们包装在变量中.
x = Variable(torch.randn(N, D_in).type(dtype), requires_grad=False)
y = Variable(torch.randn(N, D_out).type(dtype), requires_grad=False)

# 为权重创建随机张量,并将其包装在变量中.
w1 = Variable(torch.randn(D_in, H).type(dtype), requires_grad=True)
w2 = Variable(torch.randn(H, D_out).type(dtype), requires_grad=True)

learning_rate = 1e-6
for t in range(500):
    # 为了应用我们的函数,我们使用Function.apply方法.我们把它称为'relu'.
    relu = MyReLU.apply

    # 正向传递:使用变量上的运算来计算预测的y; 
    # 我们使用我们的自定义autograd操作来计算ReLU.
    y_pred = relu(x.mm(w1)).mm(w2)

    # 计算和打印损失
    loss = (y_pred - y).pow(2).sum()
    print(t, loss.data[0])

    # 使用autograd来计算反向传递.
    loss.backward()

    # 使用渐变下降更新权重
    w1.data -= learning_rate * w1.grad.data
    w2.data -= learning_rate * w2.grad.data

    # 更新权重后手动将梯度归零
    w1.grad.data.zero_()
    w2.grad.data.zero_()
