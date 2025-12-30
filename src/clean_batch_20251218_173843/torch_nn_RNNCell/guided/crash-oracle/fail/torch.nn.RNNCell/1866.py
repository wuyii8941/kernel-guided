import torch
arg_1 = 10
arg_2 = 20
arg_class = torch.nn.RNNCell(arg_1,arg_2,)
arg_3_0_tensor = torch.randint(-256,4096,[3], dtype=torch.int32)
arg_3_0 = arg_3_0_tensor.clone()
arg_3_1_tensor = torch.randint(-16384,4096,[3, 20, 2], dtype=torch.int16)
arg_3_1 = arg_3_1_tensor.clone()
arg_3 = [arg_3_0,arg_3_1,]
res = arg_class(*arg_3)
