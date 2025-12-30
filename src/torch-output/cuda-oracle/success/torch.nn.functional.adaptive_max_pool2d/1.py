results = dict()
import torch
arg_1_tensor = torch.rand([1, 64, 10, 9], dtype=torch.float32)
arg_1 = arg_1_tensor.clone()
arg_2 = 7
arg_3 = True
try:
  results["res_cpu"] = torch.nn.functional.adaptive_max_pool2d(arg_1,arg_2,arg_3,)
except Exception as e:
  results["err_cpu"] = "ERROR:"+str(e)
arg_1 = arg_1_tensor.clone().cuda()
try:
  results["res_gpu"] = torch.nn.functional.adaptive_max_pool2d(arg_1,arg_2,arg_3,)
except Exception as e:
  results["err_gpu"] = "ERROR:"+str(e)

print(results)
