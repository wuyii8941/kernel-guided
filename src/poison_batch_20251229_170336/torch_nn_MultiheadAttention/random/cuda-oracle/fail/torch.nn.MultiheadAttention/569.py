results = dict()
import torch
arg_1 = 512
arg_2 = 11
arg_3 = 2.915300784950253
arg_class = torch.nn.MultiheadAttention(arg_1,arg_2,dropout=arg_3,)
arg_4_0_tensor = torch.rand([20, 32, 518], dtype=torch.float32)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.rand([20, 32], dtype=torch.float32)
arg_4_1 = arg_4_1_tensor.clone()
arg_4_2_tensor = torch.rand([20, 32, 510], dtype=torch.bfloat16)
arg_4_2 = arg_4_2_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
try:
  results["res_cpu"] = arg_class(*arg_4)
except Exception as e:
  results["err_cpu"] = "ERROR:"+str(e)
arg_class = arg_class.cuda()
arg_4_0 = arg_4_0_tensor.clone().cuda()
arg_4_1 = arg_4_1_tensor.clone().cuda()
arg_4_2 = arg_4_2_tensor.clone().cuda()
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
try:
  results["res_gpu"] = arg_class(*arg_4)
except Exception as e:
  results["err_gpu"] = "ERROR:"+str(e)

print(results)
