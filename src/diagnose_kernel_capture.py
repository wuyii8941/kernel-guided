#!/usr/bin/env python3
"""
Benchmark 流程诊断 - 模拟 benchmark_full_oracle.py 的完整执行流程
"""

import sys
import os
import configparser
from pathlib import Path

# 添加 src 到路径
sys.path.insert(0, str(Path(__file__).parent))

print("="*70)
print("BENCHMARK FLOW DIAGNOSTICS")
print("="*70)

# 1. 导入所有必需模块
print("\n[1] Importing modules...")
try:
    from classes.database import TorchDatabase
    from classes.torch_api import TorchAPI
    from classes.torch_library import TorchLibrary
    from classes.argument import Argument, ArgType
    from constants.enum import OracleType
    print("  ✅ All modules imported")
except ImportError as e:
    print(f"  ❌ Import failed: {e}")
    sys.exit(1)

# 2. 配置数据库
print("\n[2] Configuring database...")
config_paths = [
    "config/demo_torch.conf",
    "../config/demo_torch.conf",
]

config = None
for path in config_paths:
    if os.path.exists(path):
        config = configparser.ConfigParser()
        config.read(path)
        print(f"  ✅ Using config: {path}")
        break

if not config:
    print("  ❌ Config file not found")
    sys.exit(1)

TorchDatabase.database_config(
    config["mongodb"]["host"],
    int(config["mongodb"]["port"]),
    config["mongodb"]["torch_database"]
)
print("  ✅ Database configured")

# 3. 创建测试 API
print("\n[3] Creating test API...")
test_api_name = "torch.nn.functional.relu"
try:
    api = TorchAPI(test_api_name)
    print(f"  ✅ Created API: {test_api_name}")
    print(f"  Arguments: {list(api.args.keys())}")
except Exception as e:
    print(f"  ❌ Failed to create API: {e}")
    sys.exit(1)

# 4. 创建 TorchLibrary
print("\n[4] Creating TorchLibrary...")
try:
    library = TorchLibrary("test_output", diff_bound=1e-5)
    print(f"  ✅ TorchLibrary created")
except Exception as e:
    print(f"  ❌ Failed: {e}")
    sys.exit(1)

# 5. 测试每个 Oracle - 这是关键！
print("\n[5] Testing each Oracle (simulating benchmark flow)...")
print("-"*70)

oracles = [OracleType.CRASH, OracleType.CUDA, OracleType.PRECISION]
total_kernels_captured = {}

for oracle in oracles:
    print(f"\n  Testing {oracle.name} Oracle:")
    print(f"  {'-'*60}")
    
    try:
        # 🔥 这里模拟 benchmark 的核心调用
        captured_kernels = library.test_with_oracle(api, oracle)
        
        print(f"  ✅ Oracle executed successfully")
        print(f"  Kernels captured: {len(captured_kernels)}")
        
        if len(captured_kernels) > 0:
            print(f"  Sample kernels: {list(captured_kernels)[:3]}")
        else:
            print(f"  ⚠️  WARNING: NO KERNELS CAPTURED!")
            print(f"  → This is the problem you're seeing in benchmark")
        
        total_kernels_captured[oracle.name] = len(captured_kernels)
        
    except Exception as e:
        print(f"  ❌ Oracle failed: {e}")
        import traceback
        traceback.print_exc()
        total_kernels_captured[oracle.name] = 0

# 6. 分析结果
print("\n" + "="*70)
print("ANALYSIS")
print("="*70)

print("\nKernels captured by oracle:")
for oracle_name, count in total_kernels_captured.items():
    status = "✅" if count > 0 else "❌"
    print(f"  {status} {oracle_name}: {count} kernels")

total = sum(total_kernels_captured.values())
print(f"\nTotal kernels across all oracles: {total}")

if total == 0:
    print("\n❌ PROBLEM CONFIRMED: No kernels being captured in oracle flow!")
    print("\nPossible causes:")
    print("1. test_with_oracle() not passing is_cuda=True to generate_code()")
    print("2. Generated code running on CPU despite is_cuda=True")
    print("3. Exception being silently caught")
    
    # 深度调试：直接检查生成的代码
    print("\n" + "="*70)
    print("DEEP DIVE: Checking generated code")
    print("="*70)
    
    for oracle in oracles:
        print(f"\n{oracle.name} Oracle generated code:")
        print("-"*60)
        code = library.generate_code(api, oracle)
        
        # 检查是否包含 CUDA 调用
        has_cuda = ".cuda()" in code or ".to(" in code
        print(f"Has .cuda() calls: {has_cuda}")
        
        if not has_cuda:
            print("❌ FOUND THE PROBLEM: Code doesn't contain CUDA calls!")
            print("\nGenerated code preview:")
            print(code[:500])
        else:
            print("✅ Code contains CUDA calls")
            print("\nCode preview (first 300 chars):")
            print(code[:300])
        print("-"*60)
else:
    print("\n✅ Kernels are being captured correctly!")
    print("→ The problem might be in the benchmark loop or logging")

print("\n" + "="*70)
print("RECOMMENDATION")
print("="*70)

if total == 0:
    print("""
The issue is that test_with_oracle() is not generating CUDA code.

Fix: Modify classes/torch_library.py, method generate_code():

    @staticmethod
    def generate_code(api: TorchAPI, oracle: OracleType) -> str:
        if oracle == OracleType.CRASH:
            return api.to_code(is_cuda=True)  # ← ADD is_cuda=True
        elif oracle == OracleType.CUDA:
            code = api.to_code(res="cpu_res", use_try=True)
            code += api.to_diff_code(oracle, res="cuda_res", use_try=True)
            return code
        elif oracle == OracleType.PRECISION:
            code = api.to_code(res="low_res", low_precision=True, is_cuda=True)  # ← ADD
            code += api.to_diff_code(oracle, res="high_res")
            return code

Then re-run your benchmark.
""")
else:
    print("""
test_with_oracle() is working correctly. The problem is elsewhere.

Check:
1. Is benchmark logging kernels correctly?
2. Are kernels being added to coverage tracker?
3. Print statements - are they being executed?

Add debug prints in benchmark_full_oracle.py:
    captured_kernels = self.library.test_with_oracle(api, oracle)
    print(f"DEBUG: Captured {len(captured_kernels)} kernels")  # ← ADD THIS
""")

print("="*70)