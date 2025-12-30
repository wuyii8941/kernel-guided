#!/bin/bash

# =============================================================================
# 🧪 Poison Injection Full Batch Test
# =============================================================================
# 策略: 投毒 (Inf/NaN/Extreme) + Segfault 捕获
# 目的: 诱发底层 Crash 和 Precision 错误，并将进程崩溃记录为有效 Bug
# =============================================================================

export TMPDIR=/data1/tzh/tmp

# =============================================================================
# 配置
# =============================================================================
MAX_CONCURRENT=1
CHECK_INTERVAL=30
# ✅ 指向投毒版脚本
BENCHMARK_SCRIPT="benchmark_full_oracle.py" 

# =============================================================================
# Auto-nohup
# =============================================================================
if [ -z "$NOHUP_MODE" ]; then
    echo "=================================================="
    echo "🧪 Poison Batch Test (Fault Injection)"
    echo "=================================================="
    echo ""
    
    SCRIPT_PATH="$0"
    LOG_FILE="poison_batch_$(date +%Y%m%d_%H%M%S).log"
    
    echo "Script will run in background"
    echo "Log file: $LOG_FILE"
    echo "Mode: Serial (one at a time)"
    echo "Strategy: Poison Injection + Segfault Capture"
    echo ""
    echo "Commands:"
    echo "  Watch log: tail -f $LOG_FILE"
    echo "  Monitor:   cd poison_batch_* && ./monitor.sh"
    echo ""
    
    NOHUP_MODE=1 nohup bash "$SCRIPT_PATH" > "$LOG_FILE" 2>&1 &
    
    PID=$!
    echo "✅ Launched in background (PID: $PID)"
    echo ""
    
    exit 0
fi

# =============================================================================
# 主程序开始
# =============================================================================

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BATCH_DIR="poison_batch_${TIMESTAMP}"
mkdir -p "$BATCH_DIR"

echo "=================================================="
echo "🧪 Poison Batch Test"
echo "=================================================="
echo ""
echo "[Running under nohup]"
echo "Strategy: Value Poisoning (NaN/Inf/Extreme)"
echo "Safety: Segfaults (139) will be caught and logged"
echo ""

# =============================================================================
# 🧪 API 列表
# =============================================================================

# =============================================================================
# 🧪 API 列表 (完整版 - 49 APIs)
# =============================================================================
# 策略调整:
# 1. Transformer/RNN/Attention (最复杂): 10,000 - 15,000
# 2. Conv/BatchNorm (路径多): 8,000
# 3. Norm/Embedding (中等): 5,000 - 6,000
# 4. Activation/Loss (简单): 3,000 - 4,000
# =============================================================================

declare -a APIS=(
        # =========================================================================
    # 🔴 Tier 1: 核心数学运算 (主要是为了测数值投毒，4000次足够触发 Inf 传播)
    # =========================================================================
    "torch.nn.CrossEntropyLoss:5000"
    "torch.nn.Softmax:4000"
    "torch.nn.LogSoftmax:4000"
    "torch.nn.NLLLoss:4000"
    "torch.nn.BCELoss:4000"
    "torch.nn.BCEWithLogitsLoss:4000"
    "torch.nn.KLDivLoss:4000"
    "torch.nn.PoissonNLLLoss:4000"
    "torch.nn.GELU:4000"
    "torch.nn.Mish:4000"
    # 极其简单的激活函数，3000 次就能饱和
    "torch.nn.Sigmoid:3000"
    "torch.nn.Tanh:3000"
    "torch.nn.Softplus:3000"
    "torch.nn.SELU:3000"
        # =========================================================================
    # 🟠 Tier 2: 归一化层 (BatchNorm 状态复杂，其他 Norm 对 shape 敏感)
    # =========================================================================
    "torch.nn.BatchNorm2d:8000"
    "torch.nn.BatchNorm1d:6000"
    "torch.nn.LayerNorm:6000"
    "torch.nn.GroupNorm:6000"
    "torch.nn.InstanceNorm2d:6000"
    "torch.nn.LocalResponseNorm:5000"

    # =========================================================================
    # 🟡 Tier 3: RNN/Transformer (逻辑最深，给足时间触发 Expansion Mode)
    # =========================================================================
    "torch.nn.Transformer:12000"
    "torch.nn.MultiheadAttention:10000"
    "torch.nn.TransformerEncoderLayer:10000"
    "torch.nn.TransformerDecoderLayer:10000"
    "torch.nn.LSTM:10000"
    "torch.nn.GRU:10000"
    "torch.nn.RNN:8000"
    # Cell 类虽然也是 RNN，但逻辑比完整 Layer 简单一点，6000 够了
    "torch.nn.LSTMCell:6000"
    "torch.nn.GRUCell:6000"
    "torch.nn.RNNCell:6000"

    # =========================================================================
    # 🟢 Tier 4: 卷积/线性 (CUDNN 路径极多，需要多跑覆盖 stride/padding 组合)
    # =========================================================================
    "torch.nn.Conv2d:8000"
    "torch.nn.ConvTranspose2d:8000"
    "torch.nn.Conv1d:6000"
    "torch.nn.ConvTranspose1d:6000"
    "torch.nn.Linear:4000"
    "torch.nn.Bilinear:4000"




    # =========================================================================
    # 🔵 Tier 5: 池化/Embedding/其他 (相对稳定)
    # =========================================================================
    "torch.nn.Embedding:6000"      # Embedding 容易出现索引越界，多跑点
    "torch.nn.EmbeddingBag:6000"
    "torch.nn.MaxPool2d:3000"
    "torch.nn.AvgPool2d:3000"
    "torch.nn.AdaptiveAvgPool2d:3000"
    "torch.nn.Dropout:3000"
    "torch.nn.Dropout2d:3000"
    "torch.nn.ReLU:3000"
    "torch.nn.LeakyReLU:3000"
    "torch.nn.PReLU:3000"
    "torch.nn.ELU:3000"
    "torch.nn.MSELoss:3000"
    "torch.nn.L1Loss:3000"
)
TOTAL=${#APIS[@]}

# 计算总迭代数
TOTAL_ITERS=0
for api_entry in "${APIS[@]}"; do
    IFS=':' read -r API_NAME MAX_ITER <<< "$api_entry"
    TOTAL_ITERS=$((TOTAL_ITERS + MAX_ITER))
done

echo "=================================================="
echo "Test Plan Summary (Poison Version)"
echo "=================================================="
echo "Total APIs: $TOTAL"
echo "Total iterations: $TOTAL_ITERS"
echo "Output directory: $BATCH_DIR"
echo ""
echo "Starting in 5 seconds..."
sleep 5

# =============================================================================
# 检查 benchmark 脚本
# =============================================================================
if [ ! -f "$BENCHMARK_SCRIPT" ]; then
    echo "❌ ERROR: $BENCHMARK_SCRIPT not found!"
    echo "Please ensure benchmark_poison.py is in the current directory."
    exit 1
fi
echo "✅ Found Poison Script: $BENCHMARK_SCRIPT"

# =============================================================================
# 保存控制器 PID
# =============================================================================
echo $$ > "${BATCH_DIR}/controller.pid"

# =============================================================================
# 串行执行所有测试
# =============================================================================

echo ""
echo "=================================================="
echo "Starting Tests"
echo "=================================================="
echo ""

COUNT=0
COMPLETED=0
FAILED=0
SKIPPED=0
START_TIME=$(date +%s)

for api_entry in "${APIS[@]}"; do
    IFS=':' read -r API_NAME MAX_ITER <<< "$api_entry"
    API_CLEAN=$(echo "$API_NAME" | tr '.' '_')
    
    OUTPUT_DIR="${BATCH_DIR}/${API_CLEAN}"
    LOG_FILE="${BATCH_DIR}/${API_CLEAN}.log"
    PID_FILE="${BATCH_DIR}/${API_CLEAN}.pid"
    
    COUNT=$((COUNT + 1))
    
    # 确定 Tier
    case "$API_NAME" in
        *Softmax*|*Loss*|*Sigmoid*|*Tanh*|*GELU*|*SELU*|*Mish*|*Softplus*) TIER="🔴 Tier1" ;;
        *Norm*) TIER="🟠 Tier2" ;;
        *LSTM*|*GRU*|*RNN*|*Transformer*|*Attention*) TIER="🟡 Tier3" ;;
        *Conv*|*Linear*|*Bilinear*) TIER="🟢 Tier4" ;;
        *) TIER="🔵 Tier5" ;;
    esac
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "[$COUNT/$TOTAL] $TIER $API_NAME"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Iterations: $MAX_ITER"
    echo "Output: $OUTPUT_DIR"
    
    if [ -f "$LOG_FILE" ]; then
        if grep -q "Fuzzing completed" "$LOG_FILE" 2>/dev/null; then
            echo "✅ Already completed - skipping"
            SKIPPED=$((SKIPPED + 1))
            continue
        fi
    fi
    
    TEST_START=$(date +%s)
    echo "Started: $(date '+%Y-%m-%d %H:%M:%S')"
    
    # ==========================================================
    # 运行投毒版脚本 (指向容器内配置路径)
    # ==========================================================
    python3 "$BENCHMARK_SCRIPT" \
        --api "$API_NAME" \
        --max-iterations $MAX_ITER \
        --output "$OUTPUT_DIR" \
        > "$LOG_FILE" 2>&1 &
    
    PID=$!
    echo "$PID" > "$PID_FILE"
    echo "PID: $PID"
    
    wait $PID
    EXIT_CODE=$?
    
    TEST_END=$(date +%s)
    TEST_DURATION=$((TEST_END - TEST_START))
    
    echo "Finished: $(date '+%Y-%m-%d %H:%M:%S') (${TEST_DURATION}s)"
    
    if [ $EXIT_CODE -eq 0 ]; then
        echo "✅ Completed successfully"
        COMPLETED=$((COMPLETED + 1))
        
    # ==========================================================
    # 🔥🔥🔥 核心修改：Segfault 捕获逻辑 🔥🔥🔥
    # ==========================================================
    elif [ $EXIT_CODE -eq 139 ]; then
        echo "🔥 SEGFAULT DETECTED (Exit 139)!"
        
        # 1. 强制在 guided 目录下生成 bug 文件夹 (无论当前策略如何，记录下来最重要)
        # 注意：这里假设 benchmark 脚本会生成 random/guided 目录
        # 如果 benchmark_poison.py 同时跑两个，我们默认把 Segfault 归类到 guided 下
        BUG_DIR="${OUTPUT_DIR}/guided/crash-oracle/potential-bug"
        mkdir -p "$BUG_DIR"
        
        # 2. 创建一个伪造的 Bug 文件，以便统计脚本识别
        TIMESTAMP_BUG=$(date +%s)
        cat > "${BUG_DIR}/segfault_${TIMESTAMP_BUG}.py" <<EOF
# ---------------------------------------------------------
# ⚠️ CRASH REPORT (Generated by Shell Watchdog)
# ---------------------------------------------------------
# API: $API_NAME
# Error: Segmentation Fault (Signal 11)
# Exit Code: 139
# Description: Python process crashed immediately. 
# Likely caused by Poisoned Input (Inf/NaN/Extreme).
# ---------------------------------------------------------
print("Segfault detected by shell watchdog")
EOF
        echo "   -> Logged as bug in: $BUG_DIR"
        FAILED=$((FAILED + 1))
        
    else
        echo "❌ Failed with exit code $EXIT_CODE"
        FAILED=$((FAILED + 1))
    fi
    
    # 简易统计
    RANDOM_K=$(grep -oP "Random.*Total kernels: \K\d+" "$LOG_FILE" 2>/dev/null | tail -1)
    GUIDED_K=$(grep -oP "Guided.*Total kernels: \K\d+" "$LOG_FILE" 2>/dev/null | tail -1)
    echo "Kernels Found: Random=${RANDOM_K:-0}, Guided=${GUIDED_K:-0}"
    
    sleep 2
done

# =============================================================================
# 完成与清理
# =============================================================================

END_TIME=$(date +%s)
TOTAL_TIME=$((END_TIME - START_TIME))
TOTAL_H=$((TOTAL_TIME / 3600))
TOTAL_M=$(((TOTAL_TIME % 3600) / 60))

echo ""
echo "=================================================="
echo "🎉 Poison Batch Tests Finished"
echo "=================================================="
echo "Total time: ${TOTAL_H}h ${TOTAL_M}m"
echo "APIs tested: $TOTAL"
echo "  ✅ Completed: $COMPLETED"
echo "  ❌ Failed/Crashed: $FAILED"
echo ""

TOTAL_BUGS=$(find "$BATCH_DIR" -path "*/potential-bug/*.py" 2>/dev/null | wc -l)
echo "Total Bugs Found (Including Segfaults): $TOTAL_BUGS"
echo ""

rm -f "${BATCH_DIR}/controller.pid"

# =============================================================================
# 生成辅助脚本
# =============================================================================

cat > "${BATCH_DIR}/monitor.sh" << 'MONITOR_EOF'
#!/bin/bash
cd "$(dirname "$0")"
clear
echo "=================================================="
echo "🧪 Poison Batch Monitor"
echo "=================================================="
echo ""
COMPLETED=0; FAILED=0; RUNNING=0; PENDING=0; TOTAL=0
for log_file in *.log; do
    [ -e "$log_file" ] || continue
    TOTAL=$((TOTAL + 1))
    API=$(basename "$log_file" .log)
    
    if grep -q "Fuzzing completed" "$log_file" 2>/dev/null; then
        STATUS="✅"; COMPLETED=$((COMPLETED + 1)); PROGRESS="Done"
    elif grep -q "Segmentation fault" "$log_file" 2>/dev/null; then
        # 如果脚本成功捕获并创建了bug文件，这里也显示 Crash
        STATUS="🔥"; FAILED=$((FAILED + 1)); PROGRESS="CRASHED (Captured)"
    elif [ -f "${API}.pid" ] && kill -0 $(cat "${API}.pid") 2>/dev/null; then
        STATUS="🏃"; RUNNING=$((RUNNING + 1))
        ITER=$(grep -oP "Iter \K\d+" "$log_file" 2>/dev/null | tail -1)
        PROGRESS="Running (${ITER:-0})"
    else
        STATUS="⏸️"; PENDING=$((PENDING + 1)); PROGRESS="Pending"
    fi
    R_K=$(grep -oP "Random.*Total kernels: \K\d+" "$log_file" 2>/dev/null | tail -1)
    G_K=$(grep -oP "Guided.*Total kernels: \K\d+" "$log_file" 2>/dev/null | tail -1)
    
    # Bug counts
    R_B=$(find "${API}/random" -path "*/potential-bug/*.py" 2>/dev/null | wc -l)
    G_B=$(find "${API}/guided" -path "*/potential-bug/*.py" 2>/dev/null | wc -l)

    printf "%s %-35s %-15s R_Ker:%-4s G_Ker:%-4s Bugs:%d/%d\n" \
        "$STATUS" "$API" "$PROGRESS" "${R_K:-0}" "${G_K:-0}" "$R_B" "$G_B"
done
echo ""
printf "Total: %d | 🏃%d | ✅%d | 🔥%d | ⏸️%d\n" $TOTAL $RUNNING $COMPLETED $FAILED $PENDING
MONITOR_EOF
chmod +x "${BATCH_DIR}/monitor.sh"

cat > "${BATCH_DIR}/pause.sh" << 'PAUSE_EOF'
#!/bin/bash
cd "$(dirname "$0")"
echo "Stopping Poison Tests..."
[ -f "controller.pid" ] && kill -9 $(cat controller.pid) 2>/dev/null
# 注意这里杀的是 benchmark_poison
pkill -9 -f "benchmark_poison"
echo "Stopped"
PAUSE_EOF
chmod +x "${BATCH_DIR}/pause.sh"

echo "Done! Run: ./run_batch_poison.sh"