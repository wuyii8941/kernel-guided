import torch
arg_1 = 1
arg_2 = -4.0
arg_3 = 6
arg_4 = True
arg_class = torch.nn.GRU(input_size=arg_1,hidden_size=arg_2,num_layers=arg_3,batch_first=arg_4,)
arg_5_0_tensor = torch.randint(-8192,32768,[100, 1, 1, 1], dtype=torch.int16)
arg_5_0 = arg_5_0_tensor.clone()
arg_5_1_tensor = torch.randint(0,8,[1, 100], dtype=torch.uint8)
arg_5_1 = arg_5_1_tensor.clone()
arg_5 = [arg_5_0,arg_5_1,]
res = arg_class(*arg_5)
