results = dict()
import torch
arg_1 = 32
arg_2 = 3
arg_3 = 5
arg_4 = 1
arg_5 = 2
arg_6 = True
arg_class = torch.nn.Conv2d(arg_1,arg_2,arg_3,arg_4,arg_5,bias=arg_6,)
arg_7_0_tensor = torch.rand([26, 0, 144], dtype=torch.float32)
arg_7_0 = arg_7_0_tensor.clone()
arg_7 = [arg_7_0,]
try:
  results["res_cpu"] = arg_class(*arg_7)
except Exception as e:
  results["err_cpu"] = "ERROR:"+str(e)
arg_class = arg_class.cuda()
arg_7_0 = arg_7_0_tensor.clone().cuda()
arg_7 = [arg_7_0,]
try:
  results["res_gpu"] = arg_class(*arg_7)
except Exception as e:
  results["err_gpu"] = "ERROR:"+str(e)

print(results)
