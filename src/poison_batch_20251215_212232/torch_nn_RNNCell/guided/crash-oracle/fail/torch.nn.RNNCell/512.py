import torch
arg_1 = True
arg_2 = 16
arg_class = torch.nn.RNNCell(arg_1,arg_2,)
arg_3_0_tensor = torch.rand([20, 66, 1], dtype=torch.float32)
arg_3_0 = arg_3_0_tensor.clone()
arg_3_1_tensor = torch.randint(-8192,64,[3, 20], dtype=torch.int32)
arg_3_1 = arg_3_1_tensor.clone()
arg_3 = [arg_3_0,arg_3_1,]
res = arg_class(*arg_3)
