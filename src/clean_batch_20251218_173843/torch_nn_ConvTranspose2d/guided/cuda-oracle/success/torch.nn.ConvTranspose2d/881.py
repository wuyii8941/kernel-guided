results = dict()
import torch
arg_1 = 16
arg_2 = 33
arg_3_0 = 3
arg_3_1 = 5
arg_3 = [arg_3_0,arg_3_1,]
arg_4_0 = -4
arg_4_1 = -58
arg_4 = [arg_4_0,arg_4_1,]
arg_5_0 = 4
arg_5_1 = 2
arg_5 = [arg_5_0,arg_5_1,]
arg_class = torch.nn.ConvTranspose2d(arg_1,arg_2,arg_3,stride=arg_4,padding=arg_5,)
arg_6_0_tensor = torch.rand([20, 16, 50, 100], dtype=torch.float32)
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
