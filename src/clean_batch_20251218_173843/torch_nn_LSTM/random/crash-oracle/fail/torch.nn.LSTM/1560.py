import torch
arg_1 = 214
arg_2 = 20
arg_3 = True
arg_4 = -39
arg_class = torch.nn.LSTM(arg_1,arg_2,bidirectional=arg_3,batch_first=arg_4,)
arg_5_0_tensor = torch.randint(-2,8192,[1, 15, 0], dtype=torch.int16)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
