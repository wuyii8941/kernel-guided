import torch
arg_1 = 0
arg_2 = 255
arg_3 = -1
arg_4 = False
arg_class = torch.nn.LSTM(arg_1,arg_2,bidirectional=arg_3,batch_first=arg_4,)
arg_5_0_tensor = torch.rand([0, 60, 254], dtype=torch.complex64)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
