import torch
arg_class = torch.nn.NLLLoss()
arg_1_0_tensor = torch.randint(-8,32768,[5, 4, 27, 8, 44], dtype=torch.int16)
arg_1_0 = arg_1_0_tensor.clone()
arg_1_1_tensor = torch.randint(-128,64,[5, 8, np.int64(1024)], dtype=torch.int64)
arg_1_1 = arg_1_1_tensor.clone()
arg_1 = [arg_1_0,arg_1_1,]
res = arg_class(*arg_1)
