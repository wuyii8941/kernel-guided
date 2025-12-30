#!/bin/bash

# =============================================================================
# 🔬 HKG-Fuzz Batch Test (Hybrid Kernel-Guided Fuzzer)
# =============================================================================
# 策略: Warm-up (Random) → Evolution (Kernel-Guided ε-greedy)
# 度量: Dispatcher State Coverage + Kernel Coverage
# =============================================================================

export TMPDIR=/data1/tzh/tmp

# =============================================================================
# 配置
# =============================================================================
MAX_CONCURRENT=1
CHECK_INTERVAL=30

# ✅ 指向 HKG-Fuzz Engine
BENCHMARK_SCRIPT="hkg_fuzz_engine.py"

# ✅ HKG-Fuzz 特有参数
WARMUP_RATIO=0.1        # 10% 热启动
EPSILON=0.1             # 10% 探索率
EXPANSION_EPSILON=0.3   # 停滞时 30% 探索率

# =============================================================================
# Auto-nohup
# =============================================================================
if [ -z "$NOHUP_MODE" ]; then
    echo "=================================================="
    echo "🔬 HKG-Fuzz Batch Test"
    echo "=================================================="
    echo ""
    
    SCRIPT_PATH="$0"
    LOG_FILE="hkg_batch_$(date +%Y%m%d_%H%M%S).log"
    
    echo "Script will run in background"
    echo "Log file: $LOG_FILE"
    echo "Mode: Serial (one at a time)"
    echo ""
    echo "Strategy:"
    echo "  Phase 1 (Warm-up): ${WARMUP_RATIO}× iterations → Random"
    echo "  Phase 2 (Evolution): ε-greedy (${EPSILON} explore)"
    echo ""
    echo "Commands:"
    echo "  Watch log: tail -f $LOG_FILE"
    echo "  Monitor:   cd hkg_batch_* && ./monitor.sh"
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
BATCH_DIR="hkg_batch_${TIMESTAMP}"
mkdir -p "$BATCH_DIR"

echo "=================================================="
echo "🔬 HKG-Fuzz Batch Test"
echo "=================================================="
echo ""
echo "[Running under nohup]"
echo "Strategy: Warm-up (Random) → Evolution (Kernel-Guided)"
echo "Coverage: Dispatcher State Coverage + Kernel Coverage"
echo ""

# =============================================================================
# 🧪 API 列表 (完整版 - 49 APIs)
# =============================================================================
# 迭代次数策略:
# 1. Transformer/RNN/Attention (最复杂): 10,000 - 15,000
# 2. Conv/BatchNorm (路径多): 8,000
# 3. Norm/Embedding (中等): 5,000 - 6,000
# 4. Activation/Loss (简单): 3,000 - 4,000
# =============================================================================

declare -a APIS=(
    # =========================================================================
    # 🔴 Tier 1: 核心数学运算
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
    "torch.nn.Sigmoid:3000"
    "torch.nn.Tanh:3000"
    "torch.nn.Softplus:3000"
    "torch.nn.SELU:3000"

    # =========================================================================
    # 🟠 Tier 2: 归一化层
    # =========================================================================
    "torch.nn.BatchNorm2d:8000"
    "torch.nn.BatchNorm1d:6000"
    "torch.nn.LayerNorm:6000"
    "torch.nn.GroupNorm:6000"
    "torch.nn.InstanceNorm2d:6000"
    "torch.nn.LocalResponseNorm:5000"

    # =========================================================================
    # 🟡 Tier 3: RNN/Transformer (最复杂)
    # =========================================================================
    "torch.nn.Transformer:12000"
    "torch.nn.MultiheadAttention:10000"
    "torch.nn.TransformerEncoderLayer:10000"
    "torch.nn.TransformerDecoderLayer:10000"
    "torch.nn.LSTM:10000"
    "torch.nn.GRU:10000"
    "torch.nn.RNN:8000"
    "torch.nn.LSTMCell:6000"
    "torch.nn.GRUCell:6000"
    "torch.nn.RNNCell:6000"

    # =========================================================================
    # 🟢 Tier 4: 卷积/线性
    # =========================================================================
    "torch.nn.Conv2d:8000"
    "torch.nn.ConvTranspose2d:8000"
    "torch.nn.Conv1d:6000"
    "torch.nn.ConvTranspose1d:6000"
    "torch.nn.Linear:4000"
    "torch.nn.Bilinear:4000"

    # =========================================================================
    # 🔵 Tier 5: 池化/Embedding/其他
    # =========================================================================
    "torch.nn.Embedding:6000"
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
echo "Test Plan Summary (HKG-Fuzz)"
echo "=================================================="
echo "Total APIs: $TOTAL"
echo "Total iterations: $TOTAL_ITERS"
echo "Warm-up ratio: ${WARMUP_RATIO} ($(echo "$TOTAL_ITERS * $WARMUP_RATIO" | bc | cut -d. -f1) iters)"
echo "Output directory: $BATCH_DIR"
echo ""
echo "Starting in 5 seconds..."
sleep 5

# =============================================================================
# 检查依赖脚本
# =============================================================================
if [ ! -f "$BENCHMARK_SCRIPT" ]; then
    echo "❌ ERROR: $BENCHMARK_SCRIPT not found!"
    echo "Required files: hkg_fuzz_engine.py, dispatcher_space.py, csv_logger.py"
    exit 1
fi

for dep in "dispatcher_space.py" "csv_logger.py"; do
    if [ ! -f "$dep" ]; then
        echo "❌ ERROR: Dependency $dep not found!"
        exit 1
    fi
done

echo "✅ Found HKG-Fuzz Engine and dependencies"

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
        *Softmax*|*Loss*|*Sigmoid*|*Tanh*|*GELU*|*SELU*|*Mish*|*Softplus*) TIER="🔴 T1" ;;
        *Norm*) TIER="🟠 T2" ;;
        *LSTM*|*GRU*|*RNN*|*Transformer*|*Attention*) TIER="🟡 T3" ;;
        *Conv*|*Linear*|*Bilinear*) TIER="🟢 T4" ;;
        *) TIER="🔵 T5" ;;
    esac
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "[$COUNT/$TOTAL] $TIER $API_NAME"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Iterations: $MAX_ITER (Warm-up: $(echo "$MAX_ITER * $WARMUP_RATIO" | bc | cut -d. -f1))"
    echo "Output: $OUTPUT_DIR"
    
    # 检查是否已完成
    if [ -f "$LOG_FILE" ]; then
        if grep -q "HKG-FUZZ COMPLETED" "$LOG_FILE" 2>/dev/null; then
            echo "✅ Already completed - skipping"
            SKIPPED=$((SKIPPED + 1))
            continue
        fi
    fi
    
    TEST_START=$(date +%s)
    echo "Started: $(date '+%Y-%m-%d %H:%M:%S')"
    
    # ==========================================================
    # 🔬 运行 HKG-Fuzz Engine
    # ==========================================================
    python3 "$BENCHMARK_SCRIPT" \
        --api "$API_NAME" \
        --max-iterations $MAX_ITER \
        --warmup-ratio $WARMUP_RATIO \
        --epsilon $EPSILON \
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
        
    elif [ $EXIT_CODE -eq 139 ]; then
        echo "🔥 SEGFAULT DETECTED (Exit 139)!"
        
        # 记录 Segfault 为 Bug
        BUG_DIR="${OUTPUT_DIR}/crash-oracle/potential-bug/${API_CLEAN}"
        mkdir -p "$BUG_DIR"
        
        TIMESTAMP_BUG=$(date +%s)
        cat > "${BUG_DIR}/segfault_${TIMESTAMP_BUG}.py" <<EOF
# ---------------------------------------------------------
# ⚠️ CRASH REPORT (Generated by Shell Watchdog)
# ---------------------------------------------------------
# API: $API_NAME
# Error: Segmentation Fault (Signal 11)
# Exit Code: 139
# Description: Python process crashed.
# ---------------------------------------------------------
print("Segfault detected by shell watchdog")
EOF
        echo "   -> Logged as bug in: $BUG_DIR"
        FAILED=$((FAILED + 1))
        
    else
        echo "❌ Failed with exit code $EXIT_CODE"
        FAILED=$((FAILED + 1))
    fi
    
    # 提取统计信息 (适配 HKG-Fuzz 输出格式)
    KERNELS=$(grep -oP "Total Kernels: \K\d+" "$LOG_FILE" 2>/dev/null | tail -1)
    DISP_COV=$(grep -oP "Coverage: \d+/\d+ = \K[\d.]+" "$LOG_FILE" 2>/dev/null | tail -1)
    WARMUP_DONE=$(grep -oP "warmup_count.*: \K\d+" "$LOG_FILE" 2>/dev/null | tail -1)
    
    echo "Results: Kernels=${KERNELS:-0}, Dispatcher=${DISP_COV:-0}%, Warmup=${WARMUP_DONE:-0}"
    
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
echo "🎉 HKG-Fuzz Batch Tests Finished"
echo "=================================================="
echo "Total time: ${TOTAL_H}h ${TOTAL_M}m"
echo "APIs tested: $TOTAL"
echo "  ✅ Completed: $COMPLETED"
echo "  ❌ Failed/Crashed: $FAILED"
echo "  ⏭️  Skipped: $SKIPPED"
echo ""

TOTAL_BUGS=$(find "$BATCH_DIR" -path "*/potential-bug/*.py" 2>/dev/null | wc -l)
echo "Total Bugs Found: $TOTAL_BUGS"
echo ""

rm -f "${BATCH_DIR}/controller.pid"

# =============================================================================
# 生成 Monitor 脚本
# =============================================================================

cat > "${BATCH_DIR}/monitor.sh" << 'MONITOR_EOF'
#!/bin/bash
cd "$(dirname "$0")"
clear
echo "=================================================="
echo "🔬 HKG-Fuzz Batch Monitor"
echo "=================================================="
echo ""
printf "%-35s %-12s %-8s %-10s %-8s\n" "API" "Status" "Kernels" "DispCov" "Bugs"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

COMPLETED=0; FAILED=0; RUNNING=0; PENDING=0; TOTAL=0

for log_file in *.log; do
    [ -e "$log_file" ] || continue
    TOTAL=$((TOTAL + 1))
    API=$(basename "$log_file" .log)
    
    # 解析状态
    if grep -q "HKG-FUZZ COMPLETED" "$log_file" 2>/dev/null; then
        STATUS="✅ Done"
        COMPLETED=$((COMPLETED + 1))
    elif grep -q "Segmentation fault" "$log_file" 2>/dev/null; then
        STATUS="🔥 Crash"
        FAILED=$((FAILED + 1))
    elif [ -f "${API}.pid" ] && kill -0 $(cat "${API}.pid") 2>/dev/null; then
        STATUS="🏃 Running"
        RUNNING=$((RUNNING + 1))
    else
        STATUS="⏸️ Pending"
        PENDING=$((PENDING + 1))
    fi
    
    # 提取 Metrics
    KERNELS=$(grep -oP "Total Kernels: \K\d+" "$log_file" 2>/dev/null | tail -1)
    DISP_COV=$(grep -oP "Coverage: \d+/\d+ = \K[\d.]+%" "$log_file" 2>/dev/null | tail -1)
    
    # Bug 计数
    BUGS=$(find "${API}" -path "*/potential-bug/*.py" 2>/dev/null | wc -l)
    
    printf "%-35s %-12s %-8s %-10s %-8s\n" \
        "$API" "$STATUS" "${KERNELS:-0}" "${DISP_COV:-0%}" "$BUGS"
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
printf "Total: %d | 🏃 Running: %d | ✅ Done: %d | 🔥 Crashed: %d | ⏸️ Pending: %d\n" \
    $TOTAL $RUNNING $COMPLETED $FAILED $PENDING

# 汇总 Dispatcher Coverage
echo ""
echo "📊 Dispatcher Coverage Summary:"
for log_file in *.log; do
    [ -e "$log_file" ] || continue
    API=$(basename "$log_file" .log)
    COV=$(grep -oP "Coverage: (\d+)/(\d+) = ([\d.]+)%" "$log_file" 2>/dev/null | tail -1)
    if [ -n "$COV" ]; then
        echo "   $API: $COV"
    fi
done
MONITOR_EOF
chmod +x "${BATCH_DIR}/monitor.sh"

# =============================================================================
# 生成 Pause 脚本
# =============================================================================

cat > "${BATCH_DIR}/pause.sh" << 'PAUSE_EOF'
#!/bin/bash
cd "$(dirname "$0")"
echo "Stopping HKG-Fuzz Tests..."
[ -f "controller.pid" ] && kill -9 $(cat controller.pid) 2>/dev/null
pkill -9 -f "hkg_fuzz_engine"
echo "Stopped"
PAUSE_EOF
chmod +x "${BATCH_DIR}/pause.sh"

# =============================================================================
# 生成汇总报告脚本
# =============================================================================

cat > "${BATCH_DIR}/report.sh" << 'REPORT_EOF'
#!/bin/bash
cd "$(dirname "$0")"
echo "=================================================="
echo "📊 HKG-Fuzz Final Report"
echo "=================================================="
echo ""

# 收集所有 dispatcher.json
echo "Dispatcher Coverage by API:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
for dir in */; do
    API=$(basename "$dir")
    JSON=$(find "$dir" -name "*_dispatcher.json" 2>/dev/null | head -1)
    if [ -f "$JSON" ]; then
        # 解析 JSON 获取覆盖率
        HITS=$(grep -oP '"total_hits": \K\d+' "$JSON")
        DUPS=$(grep -oP '"duplicate_hits": \K\d+' "$JSON")
        printf "%-40s Hits: %-6s Dups: %-6s\n" "$API" "${HITS:-0}" "${DUPS:-0}"
    fi
done

echo ""
echo "Bug Summary:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
CRASH_BUGS=$(find . -path "*/crash-oracle/potential-bug/*.py" 2>/dev/null | wc -l)
CUDA_BUGS=$(find . -path "*/cuda-oracle/potential-bug/*.py" 2>/dev/null | wc -l)
PREC_BUGS=$(find . -path "*/precision-oracle/potential-bug/*.py" 2>/dev/null | wc -l)
echo "  CRASH Bugs:     $CRASH_BUGS"
echo "  CUDA Bugs:      $CUDA_BUGS"
echo "  PRECISION Bugs: $PREC_BUGS"
echo "  ─────────────────"
echo "  Total:          $((CRASH_BUGS + CUDA_BUGS + PREC_BUGS))"
REPORT_EOF
chmod +x "${BATCH_DIR}/report.sh"

echo ""
echo "=================================================="
echo "✅ Batch setup complete"
echo "=================================================="
echo ""
echo "Helper scripts generated in: $BATCH_DIR/"
echo "  ./monitor.sh  - Real-time status"
echo "  ./pause.sh    - Stop all tests"
echo "  ./report.sh   - Generate final report"
echo ""
echo "Done!"