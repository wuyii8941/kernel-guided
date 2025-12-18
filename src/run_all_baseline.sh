#!/bin/bash

# =============================================================================
# 🧪 Poison Injection Full Batch Test (24h Edition)
# =============================================================================
# 优化原则:
# 1. 投毒敏感 API 优先 (Inf/NaN/Extreme 容易触发问题的)
# 2. 迭代次数按饱和速度调整 (快饱和的少跑，慢饱和的多跑)
# 3. 串行运行避免资源竞争
# =============================================================================

export TMPDIR=/data1/tzh/tmp

# =============================================================================
# 配置
# =============================================================================
MAX_CONCURRENT=1
CHECK_INTERVAL=30
BENCHMARK_SCRIPT="benchmark_full_oracle.py"
DIFF_BOUND="1e-6"

# =============================================================================
# Auto-nohup
# =============================================================================
if [ -z "$NOHUP_MODE" ]; then
    echo "=================================================="
    echo "🧪 Poison Injection Batch Test (24h Edition)"
    echo "=================================================="
    echo ""
    
    SCRIPT_PATH="$0"
    LOG_FILE="poison_batch_$(date +%Y%m%d_%H%M%S).log"
    
    echo "Script will run in background"
    echo "Log file: $LOG_FILE"
    echo "Mode: Serial (one at a time)"
    echo "Strategy: Poison Injection (5% Inf + 5% NaN + 10% Extreme)"
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
echo "🧪 Poison Injection Batch Test"
echo "=================================================="
echo ""
echo "[Running under nohup - safe to close SSH]"
echo "Poison Strategy: 5% Inf + 5% NaN + 10% Extreme + 30% Dict + 50% Mild"
echo "Precision Bound: $DIFF_BOUND (stricter than default 1e-5)"
echo ""

# =============================================================================
# 🧪 API 列表 - 按投毒敏感度排序
# =============================================================================
# 
# 投毒触发机制:
# - Inf:  exp(large) 溢出, 除法溢出, 累积溢出
# - NaN:  0/0, inf-inf, sqrt(neg), log(neg)
# - Extreme (1e20): 数值不稳定, 精度丢失
#
# 敏感度分级:
# 🔴 Tier 1: 数学运算密集 (exp/log/div/sqrt) - 最容易被投毒
# 🟠 Tier 2: 归一化层 (有除法 x/std) - 很容易被投毒  
# 🟡 Tier 3: RNN系列 (多层门控累积) - 容易累积毒性
# 🟢 Tier 4: 卷积/池化 (相对稳定) - 不太敏感
# =============================================================================

declare -a APIS=(
    # =========================================================================
    # 🔴 Tier 1: 数学运算密集型 - 投毒最敏感
    # =========================================================================
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
    
    # =========================================================================
    # 🟠 Tier 2: 归一化层
    # =========================================================================
    "torch.nn.LayerNorm:3500"
    "torch.nn.BatchNorm1d:3000"
    "torch.nn.BatchNorm2d:3500"
    "torch.nn.GroupNorm:3000"
    "torch.nn.InstanceNorm2d:3000"
    "torch.nn.LocalResponseNorm:2500"
    
    # =========================================================================
    # 🟡 Tier 3: RNN/Transformer
    # =========================================================================
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
    
    # =========================================================================
    # 🟢 Tier 4: 线性/卷积
    # =========================================================================
    "torch.nn.Linear:3000"
    "torch.nn.Bilinear:2500"
    "torch.nn.Conv1d:2500"
    "torch.nn.Conv2d:3000"
    "torch.nn.ConvTranspose1d:2500"
    "torch.nn.ConvTranspose2d:2500"
    
    # =========================================================================
    # 🔵 Tier 5: 池化/Dropout/其他
    # =========================================================================
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

# 计算总迭代数和预估时间
TOTAL_ITERS=0
for api_entry in "${APIS[@]}"; do
    IFS=':' read -r API_NAME MAX_ITER <<< "$api_entry"
    TOTAL_ITERS=$((TOTAL_ITERS + MAX_ITER))
done

echo "=================================================="
echo "Test Plan Summary"
echo "=================================================="
echo ""
echo "Total APIs: $TOTAL"
echo "Total iterations: $TOTAL_ITERS"
echo "Estimated time: ~$((TOTAL_ITERS / 3000)) hours (assuming ~3000 iter/hour)"
echo ""
echo "Priority Order:"
echo "  🔴 Tier 1: Math-heavy (Softmax, Loss, Sigmoid...) - 14 APIs"
echo "  🟠 Tier 2: Normalization (LayerNorm, BatchNorm...) - 9 APIs"
echo "  🟡 Tier 3: RNN/Transformer - 10 APIs"
echo "  🟢 Tier 4: Linear/Conv - 8 APIs"
echo "  🔵 Tier 5: Pool/Dropout/Other - remaining"
echo ""
echo "Output directory: $BATCH_DIR"
echo ""
echo "Starting in 5 seconds..."
sleep 5

# =============================================================================
# 检查 benchmark 脚本
# =============================================================================
if [ ! -f "$BENCHMARK_SCRIPT" ]; then
    echo "❌ ERROR: $BENCHMARK_SCRIPT not found!"
    echo "Please copy it to current directory."
    exit 1
fi
echo "✅ Found: $BENCHMARK_SCRIPT"

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
        *Softmax*|*Loss*|*Sigmoid*|*Tanh*|*GELU*|*SELU*|*Mish*|*Softplus*)
            TIER="🔴 Tier1"
            ;;
        *Norm*)
            TIER="🟠 Tier2"
            ;;
        *LSTM*|*GRU*|*RNN*|*Transformer*|*Attention*)
            TIER="🟡 Tier3"
            ;;
        *Conv*|*Linear*|*Bilinear*)
            TIER="🟢 Tier4"
            ;;
        *)
            TIER="🔵 Tier5"
            ;;
    esac
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "[$COUNT/$TOTAL] $TIER $API_NAME"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Iterations: $MAX_ITER"
    echo "Output: $OUTPUT_DIR"
    echo ""
    
    # 检查是否已完成
    if [ -f "$LOG_FILE" ]; then
        if grep -q "Fuzzing completed\|Saturation reached" "$LOG_FILE" 2>/dev/null; then
            echo "✅ Already completed - skipping"
            SKIPPED=$((SKIPPED + 1))
            continue
        fi
    fi
    
    # 启动测试
    TEST_START=$(date +%s)
    echo "Started: $(date '+%Y-%m-%d %H:%M:%S')"
    
    python3 "$BENCHMARK_SCRIPT" \
        --api "$API_NAME" \
        --max-iterations $MAX_ITER \
        --output "$OUTPUT_DIR" \
        --conf /data1/tzh/FreeFuzz-baseline/FreeFuzz/src/config/demo_torch.conf \
        --diff-bound $DIFF_BOUND \
        > "$LOG_FILE" 2>&1 &
    
    PID=$!
    echo "$PID" > "$PID_FILE"
    echo "PID: $PID"
    
    # 等待进程完成
    wait $PID
    EXIT_CODE=$?
    
    TEST_END=$(date +%s)
    TEST_DURATION=$((TEST_END - TEST_START))
    
    echo ""
    echo "Finished: $(date '+%Y-%m-%d %H:%M:%S') (${TEST_DURATION}s)"
    echo "Exit code: $EXIT_CODE"
    
    # 检查结果
    if [ $EXIT_CODE -eq 0 ]; then
        echo "✅ Completed successfully"
        COMPLETED=$((COMPLETED + 1))
    elif [ $EXIT_CODE -eq 139 ]; then
        echo "❌ Segmentation fault (exit code 139)"
        FAILED=$((FAILED + 1))
        echo "Last 10 lines:"
        tail -10 "$LOG_FILE" | sed 's/^/  /'
    else
        echo "❌ Failed with exit code $EXIT_CODE"
        FAILED=$((FAILED + 1))
    fi
    
    # 提取统计
    RANDOM_K=$(grep -oP "Random.*Total kernels: \K\d+" "$LOG_FILE" 2>/dev/null | tail -1)
    GUIDED_K=$(grep -oP "Guided.*Total kernels: \K\d+" "$LOG_FILE" 2>/dev/null | tail -1)
    RANDOM_B=$(find "$OUTPUT_DIR/random" -path "*/potential-bug/*.py" 2>/dev/null | wc -l)
    GUIDED_B=$(find "$OUTPUT_DIR/guided" -path "*/potential-bug/*.py" 2>/dev/null | wc -l)
    
    echo ""
    echo "Results:"
    echo "  Random: K=${RANDOM_K:-0}, Bugs=${RANDOM_B}"
    echo "  Guided: K=${GUIDED_K:-0}, Bugs=${GUIDED_B}"
    
    # 总体进度
    ELAPSED=$((TEST_END - START_TIME))
    ELAPSED_H=$((ELAPSED / 3600))
    ELAPSED_M=$(((ELAPSED % 3600) / 60))
    
    echo ""
    echo "Progress: $COUNT/$TOTAL | ✅$COMPLETED ❌$FAILED ⏭️$SKIPPED | Time: ${ELAPSED_H}h${ELAPSED_M}m"
    
    # 休息
    sleep 2
done

# =============================================================================
# 完成
# =============================================================================

END_TIME=$(date +%s)
TOTAL_TIME=$((END_TIME - START_TIME))
TOTAL_H=$((TOTAL_TIME / 3600))
TOTAL_M=$(((TOTAL_TIME % 3600) / 60))

echo ""
echo "=================================================="
echo "🎉 All Tests Finished"
echo "=================================================="
echo ""
echo "Total time: ${TOTAL_H}h ${TOTAL_M}m"
echo "APIs tested: $TOTAL"
echo "  ✅ Completed: $COMPLETED"
echo "  ❌ Failed: $FAILED"
echo "  ⏭️ Skipped: $SKIPPED"
echo ""

# Bug 统计
TOTAL_BUGS=$(find "$BATCH_DIR" -path "*/potential-bug/*.py" 2>/dev/null | wc -l)
CRASH_BUGS=$(find "$BATCH_DIR" -path "*/crash-oracle/potential-bug/*.py" 2>/dev/null | wc -l)
CUDA_BUGS=$(find "$BATCH_DIR" -path "*/cuda-oracle/potential-bug/*.py" 2>/dev/null | wc -l)
PRECISION_BUGS=$(find "$BATCH_DIR" -path "*/precision-oracle/potential-bug/*.py" 2>/dev/null | wc -l)

echo "Bug Summary:"
echo "  Total:     $TOTAL_BUGS"
echo "  CRASH:     $CRASH_BUGS"
echo "  CUDA:      $CUDA_BUGS"
echo "  PRECISION: $PRECISION_BUGS"
echo ""

# 清理
rm -f "${BATCH_DIR}/controller.pid"

# =============================================================================
# 生成监控脚本
# =============================================================================

cat > "${BATCH_DIR}/monitor.sh" << 'MONITOR_EOF'
#!/bin/bash
cd "$(dirname "$0")"

clear
echo "=================================================="
echo "🧪 Poison Injection Batch Monitor"
echo "=================================================="
echo ""

COMPLETED=0
FAILED=0
RUNNING=0
PENDING=0
TOTAL=0

for log_file in *.log; do
    [ -e "$log_file" ] || continue
    
    TOTAL=$((TOTAL + 1))
    API=$(basename "$log_file" .log)
    
    # 确定 Tier
    case "$API" in
        *Softmax*|*Loss*|*Sigmoid*|*Tanh*|*GELU*|*SELU*|*Mish*|*Softplus*)
            TIER="🔴"
            ;;
        *Norm*)
            TIER="🟠"
            ;;
        *LSTM*|*GRU*|*RNN*|*Transformer*|*Attention*)
            TIER="🟡"
            ;;
        *Conv*|*Linear*|*Bilinear*)
            TIER="🟢"
            ;;
        *)
            TIER="🔵"
            ;;
    esac
    
    if grep -q "Fuzzing completed\|Saturation reached" "$log_file" 2>/dev/null; then
        STATUS="✅"
        COMPLETED=$((COMPLETED + 1))
        PROGRESS="Done"
    elif grep -q "Segmentation fault" "$log_file" 2>/dev/null; then
        STATUS="❌"
        FAILED=$((FAILED + 1))
        PROGRESS="Segfault"
    elif [ -f "${API}.pid" ] && kill -0 $(cat "${API}.pid") 2>/dev/null; then
        STATUS="🏃"
        RUNNING=$((RUNNING + 1))
        ITER=$(grep -oP "Iter \K\d+" "$log_file" 2>/dev/null | tail -1)
        PROGRESS="Running (${ITER:-0})"
    else
        STATUS="⏸️"
        PENDING=$((PENDING + 1))
        PROGRESS="Pending"
    fi
    
    # Bug counts
    R_BUGS=$(find "${API}/random" -path "*/potential-bug/*.py" 2>/dev/null | wc -l)
    G_BUGS=$(find "${API}/guided" -path "*/potential-bug/*.py" 2>/dev/null | wc -l)
    
    printf "%s %s %-35s %-15s R:%-3d G:%-3d\n" \
        "$TIER" "$STATUS" "$API" "$PROGRESS" "$R_BUGS" "$G_BUGS"
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
printf "Total: %d | 🏃%d | ✅%d | ❌%d | ⏸️%d\n" \
    $TOTAL $RUNNING $COMPLETED $FAILED $PENDING
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Bug summary
echo ""
echo "Bug Totals:"
TOTAL_R=$(find . -path "*/random/*/potential-bug/*.py" 2>/dev/null | wc -l)
TOTAL_G=$(find . -path "*/guided/*/potential-bug/*.py" 2>/dev/null | wc -l)
echo "  Random: $TOTAL_R"
echo "  Guided: $TOTAL_G"
echo ""
echo "By Oracle:"
echo "  CRASH:     R=$(find . -path "*/random/crash-oracle/potential-bug/*.py" 2>/dev/null | wc -l) G=$(find . -path "*/guided/crash-oracle/potential-bug/*.py" 2>/dev/null | wc -l)"
echo "  CUDA:      R=$(find . -path "*/random/cuda-oracle/potential-bug/*.py" 2>/dev/null | wc -l) G=$(find . -path "*/guided/cuda-oracle/potential-bug/*.py" 2>/dev/null | wc -l)"
echo "  PRECISION: R=$(find . -path "*/random/precision-oracle/potential-bug/*.py" 2>/dev/null | wc -l) G=$(find . -path "*/guided/precision-oracle/potential-bug/*.py" 2>/dev/null | wc -l)"

echo ""
echo "Commands: ./monitor.sh | ./pause.sh | tail -f *.log"
MONITOR_EOF

chmod +x "${BATCH_DIR}/monitor.sh"

# =============================================================================
# 生成暂停脚本
# =============================================================================

cat > "${BATCH_DIR}/pause.sh" << 'PAUSE_EOF'
#!/bin/bash
cd "$(dirname "$0")"

echo "⏸️  Stopping tests..."

if [ -f "controller.pid" ]; then
    kill -9 $(cat controller.pid) 2>/dev/null
    rm -f controller.pid
fi

pkill -9 -f "benchmark_full_oracle_poison"

echo "✅ Stopped"
PAUSE_EOF

chmod +x "${BATCH_DIR}/pause.sh"

# =============================================================================
# 生成汇总脚本
# =============================================================================

cat > "${BATCH_DIR}/summary.sh" << 'SUMMARY_EOF'
#!/bin/bash
cd "$(dirname "$0")"

echo "=================================================="
echo "📊 Final Summary"
echo "=================================================="
echo ""

echo "| API | Random K | Guided K | Random Bugs | Guided Bugs |"
echo "|-----|----------|----------|-------------|-------------|"

for dir in */; do
    [ -d "$dir/random" ] || continue
    API=$(basename "$dir")
    
    R_K=$(grep -oP "Random.*Total kernels: \K\d+" "${API}.log" 2>/dev/null | tail -1)
    G_K=$(grep -oP "Guided.*Total kernels: \K\d+" "${API}.log" 2>/dev/null | tail -1)
    R_B=$(find "$dir/random" -path "*/potential-bug/*.py" 2>/dev/null | wc -l)
    G_B=$(find "$dir/guided" -path "*/potential-bug/*.py" 2>/dev/null | wc -l)
    
    printf "| %-30s | %8s | %8s | %11d | %11d |\n" \
        "$API" "${R_K:-0}" "${G_K:-0}" "$R_B" "$G_B"
done

echo ""
SUMMARY_EOF

chmod +x "${BATCH_DIR}/summary.sh"

echo ""
echo "Scripts created:"
echo "  ${BATCH_DIR}/monitor.sh  - Real-time status"
echo "  ${BATCH_DIR}/pause.sh    - Stop all tests"
echo "  ${BATCH_DIR}/summary.sh  - Final summary table"
echo ""
echo "Done!"