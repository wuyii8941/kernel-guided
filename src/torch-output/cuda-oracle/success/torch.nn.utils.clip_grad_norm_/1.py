results = dict()
import torch
arg_1_tensor = torch.rand([2, 2], dtype=torch.float32)
arg_1 = arg_1_tensor.clone()
arg_2 = 1e+20
arg_3 = 2.0
try:
  results["res_cpu"] = torch.nn.utils.clip_grad_norm_(parameters=arg_1,max_norm=arg_2,norm_type=arg_3,)
except Exception as e:
  results["err_cpu"] = "ERROR:"+str(e)
arg_1 = arg_1_tensor.clone().cuda()
try:
  results["res_gpu"] = torch.nn.utils.clip_grad_norm_(parameters=arg_1,max_norm=arg_2,norm_type=arg_3,)
except Exception as e:
  results["err_gpu"] = "ERROR:"+str(e)

print(results)
