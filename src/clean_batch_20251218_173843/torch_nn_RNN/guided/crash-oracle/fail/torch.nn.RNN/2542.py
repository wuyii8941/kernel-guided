import torch
arg_1 = True
arg_2 = -14
arg_3 = 2
arg_class = torch.nn.RNN(arg_1,arg_2,arg_3,)
arg_4_0_tensor = torch.randint(-16384,4,[5, 3, 10], dtype=torch.int64)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.rand([2, 39, 24], dtype=torch.float32)
arg_4_1 = arg_4_1_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,]
res = arg_class(*arg_4)
