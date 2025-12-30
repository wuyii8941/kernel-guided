results = dict()
import torch
arg_1 = 3
arg_2 = 9
arg_3_0 = 1
arg_3 = [arg_3_0,]
try:
  results["res_cpu"] = torch.randint(arg_1,arg_2,size=arg_3,)
except Exception as e:
  results["err_cpu"] = "ERROR:"+str(e)
arg_3 = [arg_3_0,]
try:
  results["res_gpu"] = torch.randint(arg_1,arg_2,size=arg_3,)
except Exception as e:
  results["err_gpu"] = "ERROR:"+str(e)

print(results)
