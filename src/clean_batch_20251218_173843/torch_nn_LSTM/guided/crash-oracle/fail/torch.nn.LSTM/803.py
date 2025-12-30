import torch
arg_1 = False
arg_2 = "max"
arg_3 = False
arg_4 = -95.0
arg_class = torch.nn.LSTM(arg_1,arg_2,bidirectional=arg_3,batch_first=arg_4,)
arg_5_0_tensor = torch.randint(-64,1,[1, 31, 256, 19], dtype=torch.int64)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
