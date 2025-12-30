results = dict()
import torch
arg_1_tensor = torch.rand([1], dtype=torch.float32)
arg_1 = arg_1_tensor.clone()
arg_2 = torch.preserve_format
try:
  results["res_cpu"] = torch.ones_like(arg_1,memory_format=arg_2,)
except Exception as e:
  results["err_cpu"] = "ERROR:"+str(e)
arg_1 = arg_1_tensor.clone().cuda()
try:
  results["res_gpu"] = torch.ones_like(arg_1,memory_format=arg_2,)
except Exception as e:
  results["err_gpu"] = "ERROR:"+str(e)

print(results)
