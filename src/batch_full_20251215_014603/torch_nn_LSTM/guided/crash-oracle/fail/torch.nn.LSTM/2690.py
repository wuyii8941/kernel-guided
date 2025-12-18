import torch
arg_1 = 256
arg_2 = -1024.0
arg_3 = True
arg_4 = "max"
arg_class = torch.nn.LSTM(arg_1,arg_2,bidirectional=arg_3,batch_first=arg_4,)
arg_5_0_tensor = torch.randint(-1,16384,[0, 95, 282, 1], dtype=torch.int64)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
