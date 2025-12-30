import torch
arg_1 = 16
arg_2 = 128
arg_3 = -47
arg_4 = True
arg_class = torch.nn.GRU(input_size=arg_1,hidden_size=arg_2,num_layers=arg_3,batch_first=arg_4,)
arg_5_0_tensor = torch.randint(0,32,[1, 1, 1024], dtype=torch.uint8)
arg_5_0 = arg_5_0_tensor.clone()
arg_5_1_tensor = torch.rand([29, 88, 128], dtype=torch.float32)
arg_5_1 = arg_5_1_tensor.clone()
arg_5 = [arg_5_0,arg_5_1,]
res = arg_class(*arg_5)
