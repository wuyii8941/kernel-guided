import torch
arg_1 = -1.0
arg_2 = 245
arg_3 = True
arg_4 = 0.2732128942607659
arg_class = torch.nn.LSTM(arg_1,arg_2,bidirectional=arg_3,batch_first=arg_4,)
arg_5_0_tensor = torch.randint(-256,1,[1, np.int64(1024), 254], dtype=torch.int16)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
