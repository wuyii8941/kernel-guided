import torch
arg_1 = 10
arg_2 = 20
arg_3 = "zeros"
arg_class = torch.nn.RNN(arg_1,arg_2,arg_3,)
arg_4_0_tensor = torch.randint(-16,128,[5, 35, 10], dtype=torch.int32)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.randint(-16,16,[24, 3], dtype=torch.int8)
arg_4_1 = arg_4_1_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,]
res = arg_class(*arg_4)
