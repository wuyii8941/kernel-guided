import torch
arg_1 = "sum"
arg_2 = -1024
arg_3 = True
arg_4 = True
arg_class = torch.nn.LSTM(arg_1,arg_2,bidirectional=arg_3,batch_first=arg_4,)
arg_5_0_tensor = torch.randint(-4096,128,[1, 0, 256, 53], dtype=torch.int32)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
