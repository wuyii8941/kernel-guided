results = dict()
import torch
arg_1 = 155
arg_2 = 0
arg_3 = "max"
arg_4_0 = 25
arg_4_1 = -46
arg_4_2 = -6
arg_4_3 = -56
arg_4_4 = -6
arg_4_5 = -34
arg_4 = [arg_4_0,arg_4_1,arg_4_2,arg_4_3,arg_4_4,arg_4_5,]
arg_5 = False
arg_class = torch.nn.Conv2d(arg_1,arg_2,kernel_size=arg_3,padding=arg_4,bias=arg_5,)
arg_6_0_tensor = torch.rand([128, 128, 32, 32], dtype=torch.float32)
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
