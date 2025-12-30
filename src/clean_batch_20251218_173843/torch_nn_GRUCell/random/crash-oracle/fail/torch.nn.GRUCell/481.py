import torch
arg_1 = 10
arg_2 = 14
arg_class = torch.nn.GRUCell(arg_1,arg_2,)
arg_3_0_tensor = torch.randint(0,4,[0, 33, 0, 1], dtype=torch.uint8)
arg_3_0 = arg_3_0_tensor.clone()
arg_3_1_tensor = torch.randint(-16,4096,[3, 0], dtype=torch.int32)
arg_3_1 = arg_3_1_tensor.clone()
arg_3 = [arg_3_0,arg_3_1,]
res = arg_class(*arg_3)
