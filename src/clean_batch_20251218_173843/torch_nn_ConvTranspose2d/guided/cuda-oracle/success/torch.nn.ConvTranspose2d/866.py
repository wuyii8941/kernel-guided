results = dict()
import torch
arg_1 = 111
arg_2 = 1
arg_3 = 4
arg_4 = -1024
arg_5 = 1
arg_class = torch.nn.ConvTranspose2d(arg_1,arg_2,arg_3,arg_4,arg_5,)
arg_6_0_tensor = torch.rand([64, 66, 14, 70], dtype=torch.float32)
arg_6_0 = arg_6_0_tensor.clone()
arg_6 = [arg_6_0,]
try:
  results["res_cpu"] = arg_class(*arg_6)
except Exception as e:
  results["err_cpu"] = "ERROR:"+str(e)
arg_class = arg_class.cuda()
arg_6_0 = arg_6_0_tensor.clone().cuda()
arg_6 = [arg_6_0,]
try:
  results["res_gpu"] = arg_class(*arg_6)
except Exception as e:
  results["err_gpu"] = "ERROR:"+str(e)

print(results)
