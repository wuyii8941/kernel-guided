results = dict()
import torch
arg_1 = True
arg_2 = 128
arg_3 = 2
arg_4 = False
arg_class = torch.nn.GRU(input_size=arg_1,hidden_size=arg_2,num_layers=arg_3,batch_first=arg_4,)
arg_5_0_tensor = torch.randint(-1,32,[100, 21], dtype=torch.int8)
arg_5_0 = arg_5_0_tensor.clone()
arg_5_1_tensor = torch.randint(-32,32,[0, 110, 115, 0], dtype=torch.int8)
arg_5_1 = arg_5_1_tensor.clone()
arg_5 = [arg_5_0,arg_5_1,]
try:
  results["res_cpu"] = arg_class(*arg_5)
except Exception as e:
  results["err_cpu"] = "ERROR:"+str(e)
arg_class = arg_class.cuda()
arg_5_0 = arg_5_0_tensor.clone().cuda()
arg_5_1 = arg_5_1_tensor.clone().cuda()
arg_5 = [arg_5_0,arg_5_1,]
try:
  results["res_gpu"] = arg_class(*arg_5)
except Exception as e:
  results["err_gpu"] = "ERROR:"+str(e)

print(results)
