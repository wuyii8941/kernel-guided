results = dict()
import torch
arg_1 = -46
arg_2 = 39.0
arg_3 = 1
arg_class = torch.nn.MaxPool2d(kernel_size=arg_1,stride=arg_2,padding=arg_3,)
arg_4_0_tensor = torch.rand([80, 1067, 38, 14], dtype=torch.float16)
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
