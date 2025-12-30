import torch
arg_1 = 314
arg_2 = 184
arg_3 = False
arg_4 = "max"
arg_class = torch.nn.LSTM(arg_1,arg_2,bidirectional=arg_3,batch_first=arg_4,)
arg_5_0_tensor = torch.randint(-32,4,[1, 63, 225, 1], dtype=torch.int8)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
