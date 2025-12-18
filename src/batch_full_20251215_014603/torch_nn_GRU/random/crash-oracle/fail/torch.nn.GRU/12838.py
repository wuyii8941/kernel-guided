import torch
arg_1 = 1
arg_2 = 128
arg_3 = 1
arg_4 = False
arg_class = torch.nn.GRU(input_size=arg_1,hidden_size=arg_2,num_layers=arg_3,batch_first=arg_4,)
arg_5_0_tensor = torch.randint(-4,128,[42, 0, 1, 43], dtype=torch.int64)
arg_5_0 = arg_5_0_tensor.clone()
arg_5_1_tensor = torch.rand([1, 100, 55], dtype=torch.float64)
arg_5_1 = arg_5_1_tensor.clone()
arg_5 = [arg_5_0,arg_5_1,]
res = arg_class(*arg_5)
