import torch
arg_1_tensor = torch.rand([128, 1344, 8, 8], dtype=torch.float32)
arg_1 = arg_1_tensor.clone()
arg_2 = True
res = torch.nn.functional.relu(arg_1,inplace=arg_2,)
