import torch
arg_1 = 1e+20
arg_2 = 256
arg_3 = True
arg_4 = -64.80940978102572
arg_class = torch.nn.LSTM(arg_1,arg_2,bidirectional=arg_3,batch_first=arg_4,)
arg_5_0_tensor = torch.randint(0,128,[1, 31, 256], dtype=torch.uint8)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
