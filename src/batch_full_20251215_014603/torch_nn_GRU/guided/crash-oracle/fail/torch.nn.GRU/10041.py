import torch
arg_1 = 60
arg_2 = 1024
arg_3 = 62
arg_4 = True
arg_class = torch.nn.GRU(input_size=arg_1,hidden_size=arg_2,num_layers=arg_3,batch_first=arg_4,)
arg_5_0_tensor = torch.rand([127, 31, 1, 0], dtype=torch.bfloat16)
arg_5_0 = arg_5_0_tensor.clone()
arg_5_1_tensor = torch.rand([1, 56, 128], dtype=torch.complex128)
arg_5_1 = arg_5_1_tensor.clone()
arg_5 = [arg_5_0,arg_5_1,]
res = arg_class(*arg_5)
