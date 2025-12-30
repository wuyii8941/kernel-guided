results = dict()
import torch
arg_1_0 = "reflect"
arg_1_1 = "max"
arg_1_2 = -39.0
arg_1 = [arg_1_0,arg_1_1,arg_1_2,]
arg_2 = 24
arg_3 = -17
arg_class = torch.nn.MaxPool2d(arg_1,stride=arg_2,padding=arg_3,)
arg_4_0_tensor = torch.rand([128, 1069, 8, 41, 56], dtype=torch.float32)
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
