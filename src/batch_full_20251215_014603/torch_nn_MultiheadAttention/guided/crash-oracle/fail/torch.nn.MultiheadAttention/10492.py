import torch
arg_1 = 512
arg_2 = 8
arg_3 = -17.9
arg_class = torch.nn.MultiheadAttention(arg_1,arg_2,dropout=arg_3,)
arg_4_0_tensor = torch.randint(0,1,[20, 54, 543], dtype=torch.uint8)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.rand([20, np.int64(1), 512, 1], dtype=torch.float32)
arg_4_1 = arg_4_1_tensor.clone()
arg_4_2_tensor = torch.rand([11, 32, 551, 0], dtype=torch.float32)
arg_4_2 = arg_4_2_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
res = arg_class(*arg_4)
