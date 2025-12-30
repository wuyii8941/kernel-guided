import torch
arg_1 = 0
arg_2 = 256
arg_3 = 32.0
arg_4 = -1029
arg_class = torch.nn.LSTM(arg_1,arg_2,bidirectional=arg_3,batch_first=arg_4,)
arg_5_0_tensor = torch.randint(0,2,[0, 61, 256], dtype=torch.bool)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
