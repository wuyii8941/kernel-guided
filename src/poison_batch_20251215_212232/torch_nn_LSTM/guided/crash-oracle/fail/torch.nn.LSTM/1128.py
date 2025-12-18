import torch
arg_1 = 256
arg_2 = 256
arg_3 = 5.37600804348399
arg_4 = -9
arg_class = torch.nn.LSTM(arg_1,arg_2,bidirectional=arg_3,batch_first=arg_4,)
arg_5_0_tensor = torch.randint(-512,64,[1, np.int64(16)], dtype=torch.int16)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
res = arg_class(*arg_5)
