results = dict()
import torch
arg_1 = 56
arg_2 = 32
arg_3 = -46.0
arg_4_0 = -24.0
arg_4_1 = "max"
arg_4_2 = 121.0
arg_4_3 = False
arg_4 = [arg_4_0,arg_4_1,arg_4_2,arg_4_3,]
arg_5 = True
arg_class = torch.nn.Conv2d(arg_1,arg_2,kernel_size=arg_3,padding=arg_4,bias=arg_5,)
arg_6_0_tensor = torch.rand([80, 128, 16, 16], dtype=torch.float32)
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
