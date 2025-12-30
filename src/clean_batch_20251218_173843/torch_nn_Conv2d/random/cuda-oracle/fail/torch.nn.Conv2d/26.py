results = dict()
import torch
arg_1 = -1
arg_2 = 256
arg_3 = False
arg_4 = 46
arg_class = torch.nn.Conv2d(arg_1,arg_2,bias=arg_3,kernel_size=arg_4,)
arg_5_0_tensor = torch.rand([128, 1536, 7, 7], dtype=torch.float32)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
try:
  results["res_cpu"] = arg_class(*arg_5)
except Exception as e:
  results["err_cpu"] = "ERROR:"+str(e)
arg_class = arg_class.cuda()
arg_5_0 = arg_5_0_tensor.clone().cuda()
arg_5 = [arg_5_0,]
try:
  results["res_gpu"] = arg_class(*arg_5)
except Exception as e:
  results["err_gpu"] = "ERROR:"+str(e)

print(results)
