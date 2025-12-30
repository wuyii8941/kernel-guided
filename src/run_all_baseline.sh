#!/bin/bash

# =============================================================================
# 🧪 Original Strategy Full Batch Test (Clean Baseline)
# =============================================================================
# 策略: 80% DB Sampling + 20% Random Mutation (无投毒)
# 修正: 移除了不受支持的 --diff-bound 参数
# =============================================================================

export TMPDIR=/data1/tzh/tmp

# =============================================================================
# 配置
# =============================================================================
MAX_CONCURRENT=1
CHECK_INTERVAL=30
BENCHMARK_SCRIPT="benchmark_full_oracle_tc.py" 
# DIFF_BOUND 参数已移除，因为 Baseline 脚本使用默认值

# =============================================================================
# Auto-nohup
# =============================================================================
if [ -z "$NOHUP_MODE" ]; then
    echo "=================================================="
    echo "🧪 Clean Batch Test (Original Strategy)"
    echo "=================================================="
    echo ""
    
    SCRIPT_PATH="$0"
    LOG_FILE="clean_batch_$(date +%Y%m%d_%H%M%S).log"
    
    echo "Script will run in background"
    echo "Log file: $LOG_FILE"
    echo "Mode: Serial (one at a time)"
    echo "Strategy: Original FreeFuzz (No Poison, 80% DB Sampling)"
    echo ""
    echo "Commands:"
    echo "  Watch log: tail -f $LOG_FILE"
    echo "  Monitor:   cd clean_batch_* && ./monitor.sh"
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
BATCH_DIR="clean_batch_${TIMESTAMP}"
mkdir -p "$BATCH_DIR"

echo "=================================================="
echo "🧪 Clean Batch Test (Baseline)"
echo "=================================================="
echo ""
echo "[Running under nohup]"
echo "Strategy: Standard Mutation (No Poison)"
echo "Database Sampling: 80%"
echo ""

# =============================================================================
# 🧪 API 列表
# =============================================================================

declare -a APIS=(
    # 🔴 Tier 1: 核心数学运算
    "torch.nn.Softmax:3500"
    "torch.nn.LogSoftmax:3500"
    "torch.nn.CrossEntropyLoss:3500"
    "torch.nn.NLLLoss:3000"
    "torch.nn.BCELoss:3500"
    "torch.nn.BCEWithLogitsLoss:3500"
    "torch.nn.KLDivLoss:3000"
    "torch.nn.PoissonNLLLoss:3000"
    "torch.nn.Sigmoid:2500"
    "torch.nn.Tanh:2500"
    "torch.nn.Softplus:2500"
    "torch.nn.GELU:3000"
    "torch.nn.SELU:2500"
    "torch.nn.Mish:2500"
    
    # 🟠 Tier 2: 归一化层
    "torch.nn.LayerNorm:3500"
    "torch.nn.BatchNorm1d:3000"
    "torch.nn.BatchNorm2d:3500"
    "torch.nn.GroupNorm:3000"
    "torch.nn.InstanceNorm2d:3000"
    "torch.nn.LocalResponseNorm:2500"
    
    # 🟡 Tier 3: RNN/Transformer
    "torch.nn.LSTM:4500"
    "torch.nn.GRU:4500"
    "torch.nn.RNN:3500"
    "torch.nn.LSTMCell:3000"
    "torch.nn.GRUCell:3000"
    "torch.nn.RNNCell:2500"
    "torch.nn.MultiheadAttention:4500"
    "torch.nn.TransformerEncoderLayer:6000"
    "torch.nn.TransformerDecoderLayer:6000"
    "torch.nn.Transformer:7000"
    
    # 🟢 Tier 4: 基础卷积/线性
    "torch.nn.Linear:3000"
    "torch.nn.Bilinear:2500"
    "torch.nn.Conv1d:2500"
    "torch.nn.Conv2d:3000"
    "torch.nn.ConvTranspose1d:2500"
    "torch.nn.ConvTranspose2d:2500"
    
    # 🔵 Tier 5: 池化/Dropout/其他
    "torch.nn.MaxPool2d:1500"
    "torch.nn.AvgPool2d:1500"
    "torch.nn.AdaptiveAvgPool2d:1500"
    "torch.nn.Dropout:1500"
    "torch.nn.Dropout2d:1500"
    "torch.nn.ReLU:1500"
    "torch.nn.LeakyReLU:1500"
    "torch.nn.PReLU:1500"
    "torch.nn.ELU:1500"
    "torch.nn.Embedding:2500"
    "torch.nn.EmbeddingBag:2500"
    "torch.nn.MSELoss:1500"
    "torch.nn.L1Loss:1500"
)

TOTAL=${#APIS[@]}

# 计算总迭代数
TOTAL_ITERS=0
for api_entry in "${APIS[@]}"; do
    IFS=':' read -r API_NAME MAX_ITER <<< "$api_entry"
    TOTAL_ITERS=$((TOTAL_ITERS + MAX_ITER))
done

echo "=================================================="
echo "Test Plan Summary (Clean Baseline)"
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
    exit 1
fi
echo "✅ Found Benchmark Script: $BENCHMARK_SCRIPT"

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
    
    # 检查是否已完成
    if [ -f "$LOG_FILE" ]; then
        if grep -q "Fuzzing completed" "$LOG_FILE" 2>/dev/null; then
            echo "✅ Already completed - skipping"
            SKIPPED=$((SKIPPED + 1))
            continue
        fi
    fi
    
    # 启动测试
    TEST_START=$(date +%s)
    echo "Started: $(date '+%Y-%m-%d %H:%M:%S')"
    
    # ==========================================================
    # 核心修改：去掉了 --diff-bound 参数
    # ==========================================================
    python3 "$BENCHMARK_SCRIPT" \
        --api "$API_NAME" \
        --max-iterations $MAX_ITER \
        --output "$OUTPUT_DIR" \
        --conf /workspace/FreeFuzz/src/config/demo_torch.conf \
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
    elif [ $EXIT_CODE -eq 139 ]; then
        echo "❌ Segmentation fault (exit code 139)"
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
echo "🎉 Clean Baseline Tests Finished"
echo "=================================================="
echo "Total time: ${TOTAL_H}h ${TOTAL_M}m"
echo "APIs tested: $TOTAL"
echo "  ✅ Completed: $COMPLETED"
echo "  ❌ Failed: $FAILED"
echo ""

TOTAL_BUGS=$(find "$BATCH_DIR" -path "*/potential-bug/*.py" 2>/dev/null | wc -l)
echo "Total Bugs Found (Clean Run): $TOTAL_BUGS"
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
echo "🧪 Clean Batch Monitor"
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
        STATUS="❌"; FAILED=$((FAILED + 1)); PROGRESS="Segfault"
    elif [ -f "${API}.pid" ] && kill -0 $(cat "${API}.pid") 2>/dev/null; then
        STATUS="🏃"; RUNNING=$((RUNNING + 1))
        ITER=$(grep -oP "Iter \K\d+" "$log_file" 2>/dev/null | tail -1)
        PROGRESS="Running (${ITER:-0})"
    else
        STATUS="⏸️"; PENDING=$((PENDING + 1)); PROGRESS="Pending"
    fi
    R_K=$(grep -oP "Random.*Total kernels: \K\d+" "$log_file" 2>/dev/null | tail -1)
    G_K=$(grep -oP "Guided.*Total kernels: \K\d+" "$log_file" 2>/dev/null | tail -1)
    printf "%s %-35s %-15s R_Ker:%-4s G_Ker:%-4s\n" "$STATUS" "$API" "$PROGRESS" "${R_K:-0}" "${G_K:-0}"
done
echo ""
printf "Total: %d | 🏃%d | ✅%d | ❌%d | ⏸️%d\n" $TOTAL $RUNNING $COMPLETED $FAILED $PENDING
MONITOR_EOF
chmod +x "${BATCH_DIR}/monitor.sh"

cat > "${BATCH_DIR}/pause.sh" << 'PAUSE_EOF'
#!/bin/bash
cd "$(dirname "$0")"
echo "Stopping..."
[ -f "controller.pid" ] && kill -9 $(cat controller.pid) 2>/dev/null
pkill -9 -f "benchmark_full_oracle_tc"
echo "Stopped"
PAUSE_EOF
chmod +x "${BATCH_DIR}/pause.sh"

echo "Done!"