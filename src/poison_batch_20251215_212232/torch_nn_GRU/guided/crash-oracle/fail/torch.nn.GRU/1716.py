import torch
arg_1 = -16
arg_2 = 1024
arg_3 = 0.16769739712700726
arg_4 = False
arg_class = torch.nn.GRU(input_size=arg_1,hidden_size=arg_2,num_layers=arg_3,batch_first=arg_4,)
arg_5_0_tensor = torch.randint(0,4,[94, 1, 1], dtype=torch.uint8)
arg_5_0 = arg_5_0_tensor.clone()
arg_5_1_tensor = torch.rand([1, np.int64(16), 0], dtype=torch.float32)
arg_5_1 = arg_5_1_tensor.clone()
arg_5 = [arg_5_0,arg_5_1,]
res = arg_class(*arg_5)
