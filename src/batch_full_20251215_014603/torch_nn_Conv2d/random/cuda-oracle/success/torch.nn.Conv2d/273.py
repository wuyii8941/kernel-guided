results = dict()
import torch
arg_1 = 832
arg_2 = 0
arg_3 = True
arg_class = torch.nn.Conv2d(arg_1,arg_2,kernel_size=arg_3,)
arg_4_0_tensor = torch.rand([16, 832, 4, 4], dtype=torch.float32)
arg_4_0 = arg_4_0_tensor.clone()
arg_4 = [arg_4_0,]
try:
  results["res_cpu"] = arg_class(*arg_4)
except Exception as e:
  results["err_cpu"] = "ERROR:"+str(e)
arg_class = arg_class.cuda()
arg_4_0 = arg_4_0_tensor.clone().cuda()
arg_4 = [arg_4_0,]
try:
  results["res_gpu"] = arg_class(*arg_4)
except Exception as e:
  results["err_gpu"] = "ERROR:"+str(e)

print(results)
