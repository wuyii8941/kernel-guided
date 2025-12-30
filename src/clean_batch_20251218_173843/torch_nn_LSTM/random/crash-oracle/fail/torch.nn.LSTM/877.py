import torch
arg_1 = 256
arg_2 = 256
arg_3 = True
arg_4 = 8.0
arg_class = torch.nn.LSTM(arg_1,arg_2,bidirectional=arg_3,batch_first=arg_4,)
arg_5_0_tensor = torch.rand([1, 63, 260, 1], dtype=torch.float16)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
