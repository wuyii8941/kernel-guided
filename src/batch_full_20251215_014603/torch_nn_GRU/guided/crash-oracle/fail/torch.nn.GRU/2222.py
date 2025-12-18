import torch
arg_1 = False
arg_2 = -1e+20
arg_3 = False
arg_class = torch.nn.GRU(arg_1,arg_2,arg_3,)
arg_4_0_tensor = torch.rand([0, 4, np.int64(16)], dtype=torch.float16)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.rand([2, np.int64(16), 25], dtype=torch.bfloat16)
arg_4_1 = arg_4_1_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,]
res = arg_class(*arg_4)
