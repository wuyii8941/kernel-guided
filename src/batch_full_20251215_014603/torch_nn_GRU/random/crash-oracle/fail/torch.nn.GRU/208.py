import torch
arg_1 = "max"
arg_2 = 1024
arg_3 = 9
arg_4 = True
arg_class = torch.nn.GRU(input_size=arg_1,hidden_size=arg_2,num_layers=arg_3,batch_first=arg_4,)
arg_5_0_tensor = torch.rand([100, 0], dtype=torch.complex128)
arg_5_0 = arg_5_0_tensor.clone()
arg_5_1_tensor = torch.randint(0,64,[np.int64(1), 100, 128], dtype=torch.uint8)
arg_5_1 = arg_5_1_tensor.clone()
arg_5 = [arg_5_0,arg_5_1,]
res = arg_class(*arg_5)
