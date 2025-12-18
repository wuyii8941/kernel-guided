results = dict()
import torch
arg_1 = 32
arg_2 = -13
arg_3 = 9
arg_4 = 1
arg_class = torch.nn.Conv2d(arg_1,arg_2,arg_3,arg_4,)
arg_5_0_tensor = torch.randint(-16,16,[0, 0, 1088, 1088], dtype=torch.int8)
arg_5_0 = arg_5_0_tensor.clone()
arg_5 = [arg_5_0,]
try:
  results["res_cpu"] = arg_class(*arg_5)
except Exception as e:
  results["err_cpu"] = "ERROR:"+str(e)
arg_class = arg_class.cuda()
arg_5_0 = arg_5_0_tensor.clone().cuda()
arg_5 = [arg_5_0,]
try:
  results["res_gpu"] = arg_class(*arg_5)
except Exception as e:
  results["err_gpu"] = "ERROR:"+str(e)

print(results)
