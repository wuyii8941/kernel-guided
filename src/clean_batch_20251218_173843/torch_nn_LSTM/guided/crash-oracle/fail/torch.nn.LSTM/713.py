import torch
arg_1 = 255
arg_2 = 256
arg_3 = -32
arg_4 = -64
arg_class = torch.nn.LSTM(arg_1,arg_2,bidirectional=arg_3,batch_first=arg_4,)
arg_5_0_tensor = torch.rand([9, 31, 298], dtype=torch.complex64)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
