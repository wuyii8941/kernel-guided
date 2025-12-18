import torch
arg_1 = False
arg_2 = 128
arg_3 = 8
arg_4 = False
arg_class = torch.nn.GRU(input_size=arg_1,hidden_size=arg_2,num_layers=arg_3,batch_first=arg_4,)
arg_5_0_tensor = torch.rand([99, 0], dtype=torch.bfloat16)
arg_5_0 = arg_5_0_tensor.clone()
arg_5_1_tensor = torch.randint(0,2,[1, 92, 129, 6], dtype=torch.bool)
arg_5_1 = arg_5_1_tensor.clone()
arg_5 = [arg_5_0,arg_5_1,]
res = arg_class(*arg_5)
