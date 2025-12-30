import torch
arg_1 = 58
arg_2 = 16
arg_class = torch.nn.LSTMCell(arg_1,arg_2,)
arg_3_0_tensor = torch.rand([53, 10], dtype=torch.float32)
arg_3_0 = arg_3_0_tensor.clone()
arg_3_1_0_tensor = torch.randint(-32768,1024,[0, 77], dtype=torch.int64)
arg_3_1_0 = arg_3_1_0_tensor.clone()
arg_3_1_1_tensor = torch.randint(0,1,[2], dtype=torch.uint8)
arg_3_1_1 = arg_3_1_1_tensor.clone()
arg_3_1 = [arg_3_1_0,arg_3_1_1,]
arg_3 = [arg_3_0,arg_3_1,]
res = arg_class(*arg_3)
