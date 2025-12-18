results = dict()
import torch
arg_1 = -1e+20
arg_2 = 68.0
arg_3 = True
arg_4 = 1
arg_5 = 1
arg_6 = False
arg_class = torch.nn.Conv2d(in_channels=arg_1,out_channels=arg_2,kernel_size=arg_3,stride=arg_4,padding=arg_5,bias=arg_6,)
arg_7_0_tensor = torch.rand([26, 128, 144, 144], dtype=torch.float32)
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
