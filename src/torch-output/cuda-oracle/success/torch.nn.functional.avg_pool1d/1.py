results = dict()
import torch
arg_1_tensor = torch.rand([0, 16], dtype=torch.float16)
arg_1 = arg_1_tensor.clone()
arg_2 = 3
arg_3 = 2
arg_4 = 0
arg_5 = False
try:
  results["res_cpu"] = torch.nn.functional.avg_pool1d(arg_1,arg_2,arg_3,arg_4,arg_5,)
except Exception as e:
  results["err_cpu"] = "ERROR:"+str(e)
arg_1 = arg_1_tensor.clone().cuda()
try:
  results["res_gpu"] = torch.nn.functional.avg_pool1d(arg_1,arg_2,arg_3,arg_4,arg_5,)
except Exception as e:
  results["err_gpu"] = "ERROR:"+str(e)

print(results)
