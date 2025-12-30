import torch
arg_1 = 300
arg_2 = 261
arg_3 = True
arg_4 = False
arg_class = torch.nn.LSTM(arg_1,arg_2,bidirectional=arg_3,batch_first=arg_4,)
arg_5_0_tensor = torch.randint(-8,32,[41, 15, 294], dtype=torch.int8)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
