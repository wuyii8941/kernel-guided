import torch
arg_1 = -16
arg_2 = 16
arg_3 = True
arg_4 = -104.0
arg_class = torch.nn.LSTM(arg_1,arg_2,bidirectional=arg_3,batch_first=arg_4,)
arg_5_0_tensor = torch.rand([np.int64(1024), 15, 256, 1], dtype=torch.bfloat16)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
