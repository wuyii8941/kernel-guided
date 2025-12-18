import torch
arg_1 = False
arg_2 = 8
arg_class = torch.nn.TransformerDecoderLayer(d_model=arg_1,nhead=arg_2,)
arg_3_0_tensor = torch.randint(-2,2,[57, 43, np.int64(1)], dtype=torch.int32)
arg_3_0 = arg_3_0_tensor.clone()
arg_3_1_tensor = torch.randint(-4,16,[0, 0, 564], dtype=torch.int8)
arg_3_1 = arg_3_1_tensor.clone()
arg_3 = [arg_3_0,arg_3_1,]
res = arg_class(*arg_3)
