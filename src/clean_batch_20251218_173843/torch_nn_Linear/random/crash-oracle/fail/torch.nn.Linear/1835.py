import torch
arg_1 = 128
arg_2 = "max"
arg_class = torch.nn.Linear(in_features=arg_1,out_features=arg_2,)
arg_3_0_tensor = torch.randint(-8,64,[256, 128], dtype=torch.int16)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
