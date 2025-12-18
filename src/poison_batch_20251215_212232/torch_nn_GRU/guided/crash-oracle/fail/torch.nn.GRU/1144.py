import torch
arg_1 = 2
arg_2 = 130
arg_3 = 10
arg_4 = False
arg_class = torch.nn.GRU(input_size=arg_1,hidden_size=arg_2,num_layers=arg_3,batch_first=arg_4,)
arg_5_0_tensor = torch.randint(-64,16,[99, 1], dtype=torch.int8)
arg_5_0 = arg_5_0_tensor.clone()
arg_5_1_tensor = torch.rand([0, 105, 135, 1, 5], dtype=torch.float32)
arg_5_1 = arg_5_1_tensor.clone()
arg_5 = [arg_5_0,arg_5_1,]
res = arg_class(*arg_5)
