results = dict()
import torch
arg_1_tensor = torch.rand([2], dtype=torch.float32)
arg_1 = arg_1_tensor.clone()
arg_2 = 1.0
arg_3 = False
try:
  results["res_cpu"] = torch.nn.functional.celu(arg_1,arg_2,arg_3,)
except Exception as e:
  results["err_cpu"] = "ERROR:"+str(e)
arg_1 = arg_1_tensor.clone().cuda()
try:
  results["res_gpu"] = torch.nn.functional.celu(arg_1,arg_2,arg_3,)
except Exception as e:
  results["err_gpu"] = "ERROR:"+str(e)

print(results)
