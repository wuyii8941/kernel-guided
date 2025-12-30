results = dict()
import torch
arg_1 = 2
arg_2 = 2
arg_class = torch.nn.MaxPool2d(kernel_size=arg_1,stride=arg_2,)
arg_3_0_tensor = torch.randint(-2048,2048,[0, 256, 0, 8], dtype=torch.int64)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
try:
  results["res_cpu"] = arg_class(*arg_3)
except Exception as e:
  results["err_cpu"] = "ERROR:"+str(e)
arg_class = arg_class.cuda()
arg_3_0 = arg_3_0_tensor.clone().cuda()
arg_3 = [arg_3_0,]
try:
  results["res_gpu"] = arg_class(*arg_3)
except Exception as e:
  results["err_gpu"] = "ERROR:"+str(e)

print(results)
