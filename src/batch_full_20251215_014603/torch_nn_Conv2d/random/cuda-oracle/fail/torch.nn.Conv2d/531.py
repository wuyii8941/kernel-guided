results = dict()
import torch
arg_1 = -17
arg_2 = 16
arg_3_0 = 1
arg_3_1 = 3
arg_3 = [arg_3_0,arg_3_1,]
arg_4 = 1
arg_5_0 = 0
arg_5_1 = 1
arg_5 = [arg_5_0,arg_5_1,]
arg_6 = False
arg_7_0 = 1
arg_7 = [arg_7_0,]
arg_class = torch.nn.Conv2d(arg_1,arg_2,arg_3,stride=arg_4,padding=arg_5,bias=arg_6,dilation=arg_7,)
arg_8_0_tensor = torch.rand([8, 16, 128, 256], dtype=torch.float32)
arg_8_0 = arg_8_0_tensor.clone()
arg_8 = [arg_8_0,]
try:
  results["res_cpu"] = arg_class(*arg_8)
except Exception as e:
  results["err_cpu"] = "ERROR:"+str(e)
arg_class = arg_class.cuda()
arg_8_0 = arg_8_0_tensor.clone().cuda()
arg_8 = [arg_8_0,]
try:
  results["res_gpu"] = arg_class(*arg_8)
except Exception as e:
  results["err_gpu"] = "ERROR:"+str(e)

print(results)
