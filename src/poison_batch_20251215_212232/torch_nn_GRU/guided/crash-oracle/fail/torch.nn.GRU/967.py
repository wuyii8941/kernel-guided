import torch
arg_1 = 1
arg_2 = 130
arg_3 = -26
arg_4 = True
arg_class = torch.nn.GRU(input_size=arg_1,hidden_size=arg_2,num_layers=arg_3,batch_first=arg_4,)
arg_5_0_tensor = torch.randint(-16384,1,[99, 0], dtype=torch.int32)
arg_5_0 = arg_5_0_tensor.clone()
arg_5_1_tensor = torch.rand([0, 0, np.int64(1), np.int64(16), 6], dtype=torch.float32)
arg_5_1 = arg_5_1_tensor.clone()
arg_5 = [arg_5_0,arg_5_1,]
res = arg_class(*arg_5)
