results = dict()
import torch
arg_1 = 0
arg_2 = -7
arg_class = torch.nn.LSTMCell(arg_1,arg_2,)
arg_3_0_tensor = torch.randint(-8,128,[2, 10], dtype=torch.int64)
arg_3_0 = arg_3_0_tensor.clone()
arg_3_1_0_tensor = torch.randint(-256,1,[1, 20], dtype=torch.int64)
arg_3_1_0 = arg_3_1_0_tensor.clone()
arg_3_1_1_tensor = torch.randint(-1,8192,[2, 20], dtype=torch.int16)
arg_3_1_1 = arg_3_1_1_tensor.clone()
arg_3_1 = [arg_3_1_0,arg_3_1_1,]
arg_3 = [arg_3_0,arg_3_1,]
try:
  results["res_cpu"] = arg_class(*arg_3)
except Exception as e:
  results["err_cpu"] = "ERROR:"+str(e)
arg_class = arg_class.cuda()
arg_3_0 = arg_3_0_tensor.clone().cuda()
arg_3_1_0 = arg_3_1_0_tensor.clone().cuda()
arg_3_1_1 = arg_3_1_1_tensor.clone().cuda()
arg_3_1 = [arg_3_1_0,arg_3_1_1,]
arg_3 = [arg_3_0,arg_3_1,]
try:
  results["res_gpu"] = arg_class(*arg_3)
except Exception as e:
  results["err_gpu"] = "ERROR:"+str(e)

print(results)
