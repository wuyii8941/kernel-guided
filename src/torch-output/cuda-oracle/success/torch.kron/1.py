results = dict()
import torch
arg_1_tensor = torch.rand([3, 6, 3072], dtype=torch.float32)
arg_1 = arg_1_tensor.clone()
arg_2_tensor = torch.rand([10, 20], dtype=torch.float64)
arg_2 = arg_2_tensor.clone()
try:
  results["res_cpu"] = torch.kron(arg_1,arg_2,)
except Exception as e:
  results["err_cpu"] = "ERROR:"+str(e)
arg_1 = arg_1_tensor.clone().cuda()
arg_2 = arg_2_tensor.clone().cuda()
try:
  results["res_gpu"] = torch.kron(arg_1,arg_2,)
except Exception as e:
  results["err_gpu"] = "ERROR:"+str(e)

print(results)
