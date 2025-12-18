import torch
arg_1 = False
arg_2 = 12.046662632211198
arg_3 = False
arg_4 = -3
arg_class = torch.nn.LSTM(arg_1,arg_2,bidirectional=arg_3,batch_first=arg_4,)
arg_5_0_tensor = torch.rand([1, 63, 0], dtype=torch.complex128)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
