import torch
arg_1 = 10
arg_2 = "max"
arg_3 = 1
arg_4 = 105.0
arg_class = torch.nn.LSTM(arg_1,arg_2,bidirectional=arg_3,batch_first=arg_4,)
arg_5_0_tensor = torch.randint(0,2,[1, 17, 256], dtype=torch.bool)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
