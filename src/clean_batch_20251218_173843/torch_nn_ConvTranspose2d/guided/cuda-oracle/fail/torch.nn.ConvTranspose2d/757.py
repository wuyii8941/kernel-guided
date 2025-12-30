results = dict()
import torch
arg_1 = 256
arg_2 = False
arg_3 = -33
arg_4 = 2
arg_5 = 1
arg_6 = 0
arg_7 = True
arg_class = torch.nn.ConvTranspose2d(in_channels=arg_1,out_channels=arg_2,kernel_size=arg_3,stride=arg_4,padding=arg_5,output_padding=arg_6,bias=arg_7,)
arg_8_0_tensor = torch.rand([58, 256, 14], dtype=torch.float32)
arg_8_0 = arg_8_0_tensor.clone()
arg_8 = [arg_8_0,]
try:
  results["res_cpu"] = arg_class(*arg_8)
except Exception as e:
  results["err_cpu"] = "ERROR:"+str(e)
arg_class = arg_class.cuda()
arg_8_0 = arg_8_0_tensor.clone().cuda()
arg_8 = [arg_8_0,]
try:
  results["res_gpu"] = arg_class(*arg_8)
except Exception as e:
  results["err_gpu"] = "ERROR:"+str(e)

print(results)
