results = dict()
import torch
arg_1_tensor = torch.rand([128, 1344, 8, 8], dtype=torch.float32)
arg_1 = arg_1_tensor.clone()
arg_2 = True
try:
  results["res_cpu"] = torch.nn.functional.relu(arg_1,inplace=arg_2,)
except Exception as e:
  results["err_cpu"] = "ERROR:"+str(e)
arg_1 = arg_1_tensor.clone().cuda()
try:
  results["res_gpu"] = torch.nn.functional.relu(arg_1,inplace=arg_2,)
except Exception as e:
  results["err_gpu"] = "ERROR:"+str(e)

print(results)
