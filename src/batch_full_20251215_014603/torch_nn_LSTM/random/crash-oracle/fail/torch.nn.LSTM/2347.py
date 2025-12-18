import torch
arg_1 = 211
arg_2 = 256
arg_3 = True
arg_4 = -66.0
arg_class = torch.nn.LSTM(arg_1,arg_2,bidirectional=arg_3,batch_first=arg_4,)
arg_5_0_tensor = torch.randint(-1,2048,[1, 76, 256], dtype=torch.int32)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
