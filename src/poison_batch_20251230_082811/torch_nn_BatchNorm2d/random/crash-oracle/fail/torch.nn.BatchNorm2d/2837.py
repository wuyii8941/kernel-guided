import torch
arg_1 = 512
arg_2 = 1.3324489512448756
arg_class = torch.nn.BatchNorm2d(arg_1,momentum=arg_2,)
arg_3_0_tensor = torch.rand([1, 1024, 7, 7], dtype=torch.float16)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
