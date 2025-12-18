import torch
arg_1 = 261
arg_2 = 251
arg_3 = 6.264208780088822
arg_4 = -1.0
arg_class = torch.nn.LSTM(arg_1,arg_2,bidirectional=arg_3,batch_first=arg_4,)
arg_5_0_tensor = torch.rand([0, 31, 256], dtype=torch.float64)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
