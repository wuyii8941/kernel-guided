results = dict()
import torch
arg_1 = 512
arg_2 = 1
arg_class = torch.nn.TransformerEncoderLayer(d_model=arg_1,nhead=arg_2,)
arg_3_0_tensor = torch.randint(0,64,[0, 32, 512], dtype=torch.uint8)
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
