results = dict()
import torch
arg_1_tensor = torch.randint(-128,512,[2, 2], dtype=torch.int64)
arg_1 = arg_1_tensor.clone()
arg_2_0 = -56
arg_2 = [arg_2_0,]
try:
  results["res_cpu"] = torch.reshape(arg_1,arg_2,)
except Exception as e:
  results["err_cpu"] = "ERROR:"+str(e)
arg_1 = arg_1_tensor.clone().cuda()
arg_2 = [arg_2_0,]
try:
  results["res_gpu"] = torch.reshape(arg_1,arg_2,)
except Exception as e:
  results["err_gpu"] = "ERROR:"+str(e)

print(results)
