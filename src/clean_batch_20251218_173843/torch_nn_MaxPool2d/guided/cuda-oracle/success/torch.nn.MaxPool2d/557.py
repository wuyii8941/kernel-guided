results = dict()
import torch
arg_1 = 3
arg_2 = 2
arg_3 = 63
arg_class = torch.nn.MaxPool2d(kernel_size=arg_1,stride=arg_2,padding=arg_3,)
arg_4_0_tensor = torch.rand([16, 64, 30, 30], dtype=torch.float32)
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
