import torch
arg_1 = 1022.0
arg_2 = 262
arg_3 = True
arg_4 = 9
arg_class = torch.nn.LSTM(arg_1,arg_2,bidirectional=arg_3,batch_first=arg_4,)
arg_5_0_tensor = torch.rand([1, 7, 256], dtype=torch.float64)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
