import torch
arg_1 = -1029
arg_2 = 128
arg_3 = 0
arg_4 = False
arg_class = torch.nn.GRU(input_size=arg_1,hidden_size=arg_2,num_layers=arg_3,batch_first=arg_4,)
arg_5_0_tensor = torch.randint(-16384,32768,[100, 1, 1], dtype=torch.int16)
arg_5_0 = arg_5_0_tensor.clone()
arg_5_1_tensor = torch.randint(-256,16,[0, 100, 128], dtype=torch.int32)
arg_5_1 = arg_5_1_tensor.clone()
arg_5 = [arg_5_0,arg_5_1,]
res = arg_class(*arg_5)
