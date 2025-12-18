results = dict()
import torch
arg_1 = "mean"
arg_2 = 512
arg_3_0 = 2
arg_3_1 = 2
arg_3 = [arg_3_0,arg_3_1,]
arg_4_0 = 3
arg_4_1 = 3
arg_4_2 = 6
arg_4_3 = 6
arg_4_4 = 0
arg_4_5 = 1
arg_4 = [arg_4_0,arg_4_1,arg_4_2,arg_4_3,arg_4_4,arg_4_5,]
arg_class = torch.nn.Conv2d(arg_1,arg_2,kernel_size=arg_3,padding=arg_4,)
arg_5_0_tensor = torch.rand([16, 512, 2, 2], dtype=torch.float32)
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
