import torch
arg_1 = 256
arg_2 = 258
arg_3 = False
arg_4 = 0.6505658904357841
arg_class = torch.nn.LSTM(arg_1,arg_2,bidirectional=arg_3,batch_first=arg_4,)
arg_5_0_tensor = torch.randint(-256,512,[2, 31, 256], dtype=torch.int64)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
