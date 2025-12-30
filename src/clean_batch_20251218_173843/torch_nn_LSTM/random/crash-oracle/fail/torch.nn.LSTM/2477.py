import torch
arg_1 = 256
arg_2 = "mean"
arg_3 = -26
arg_4 = "replicate"
arg_class = torch.nn.LSTM(arg_1,arg_2,bidirectional=arg_3,batch_first=arg_4,)
arg_5_0_tensor = torch.rand([16, 63, 256], dtype=torch.complex128)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
