results = dict()
import torch
arg_1 = 256
arg_2 = 256
arg_3 = 12
arg_4_0 = 2
arg_4_1 = 2
arg_4_2 = 2
arg_4 = [arg_4_0,arg_4_1,arg_4_2,]
arg_5_0 = 4
arg_5_1 = 2
arg_5_2 = 0
arg_5 = [arg_5_0,arg_5_1,arg_5_2,]
arg_6 = False
arg_7 = True
arg_class = torch.nn.ConvTranspose2d(in_channels=arg_1,out_channels=arg_2,kernel_size=arg_3,stride=arg_4,padding=arg_5,output_padding=arg_6,bias=arg_7,)
arg_8_0_tensor = torch.rand([1, 256, 14, 14], dtype=torch.float32)
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
