import torch
arg_1 = 261
arg_2 = 255
arg_3 = False
arg_4 = -2.7065321120960206
arg_class = torch.nn.LSTM(arg_1,arg_2,bidirectional=arg_3,batch_first=arg_4,)
arg_5_0_tensor = torch.randint(0,64,[11, 60, 256], dtype=torch.uint8)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
