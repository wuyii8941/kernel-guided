import torch
arg_1 = 1
arg_2 = 0
arg_3 = -15
arg_4 = True
arg_class = torch.nn.GRU(input_size=arg_1,hidden_size=arg_2,num_layers=arg_3,batch_first=arg_4,)
arg_5_0_tensor = torch.rand([100, 1, 8], dtype=torch.float32)
arg_5_0 = arg_5_0_tensor.clone()
arg_5_1_tensor = torch.randint(0,2,[0, 100, 128], dtype=torch.bool)
arg_5_1 = arg_5_1_tensor.clone()
arg_5 = [arg_5_0,arg_5_1,]
res = arg_class(*arg_5)
