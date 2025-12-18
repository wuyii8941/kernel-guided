import torch
arg_1 = 256
arg_2 = 259
arg_3 = False
arg_4 = -2.211026932145229
arg_class = torch.nn.LSTM(arg_1,arg_2,bidirectional=arg_3,batch_first=arg_4,)
arg_5_0_tensor = torch.randint(-4096,8,[1, 20, 256], dtype=torch.int16)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
