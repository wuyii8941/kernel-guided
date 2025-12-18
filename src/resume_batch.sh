#!/bin/bash

# Batch Resume Script - Single Concurrent (Safe Mode)
# ===================================================
# 修改：MAX_CONCURRENT=1，避免资源竞争导致崩溃

# =============================================================================
# 配置参数
# =============================================================================

MAX_CONCURRENT=2        # 🔧 同时只运行 1 个实验（安全模式）
CHECK_INTERVAL=30       # 每 30 秒检查一次
STAGGER_DELAY=3         # 启动间隔 3 秒

# =============================================================================
# Auto-nohup
# =============================================================================
if [ -z "$NOHUP_MODE" ]; then
    echo "=================================================="
    echo "🔥 Auto-launching with nohup (Safe Mode)..."
    echo "=================================================="
    echo ""
    
    SCRIPT_PATH="$0"
    LOG_FILE="resume_launcher_$(date +%Y%m%d_%H%M%S).log"
    
    echo "Script will run in background"
    echo "Log file: $LOG_FILE"
    echo ""
    echo "Max Concurrent: 1 (Safe Mode)"
    echo ""
    echo "Commands:"
    echo "  Watch log:    tail -f $LOG_FILE"
    echo "  Monitor:      cd batch_full_* && ./monitor.sh"
    echo "  Pause:        kill \$(cat batch_full_*/controller.pid)"
    echo ""
    
    NOHUP_MODE=1 nohup bash "$SCRIPT_PATH" > "$LOG_FILE" 2>&1 &
    
    PID=$!
    echo "✅ Launched in background (PID: $PID)"
    echo ""
    
    exit 0
fi

# 如果到这里，说明已经在 nohup 下运行了
# =============================================================================

echo "=================================================="
echo "🔄 Batch Resume - Safe Mode (Concurrent=1)"
echo "=================================================="
echo ""
echo "[Running under nohup - safe to close SSH]"
echo ""
echo "Max Concurrent: $MAX_CONCURRENT"
echo "Check Interval: ${CHECK_INTERVAL}s"
echo ""

# =============================================================================
# 查找批量测试目录
# =============================================================================

BATCH_DIR=$(ls -dt batch_full_* 2>/dev/null | head -1)

if [ -z "$BATCH_DIR" ]; then
    echo "❌ No batch directory found (batch_full_*)"
    echo "   Please run the original batch_launcher.sh first"
    exit 1
fi

echo "Found batch directory: $BATCH_DIR"
cd "$BATCH_DIR"

# 保存控制器 PID
echo $$ > controller.pid
echo "Controller PID: $$"
echo ""

# =============================================================================
# 配置文件检查
# =============================================================================

CONFIG_FILE="/data1/tzh/FreeFuzz-baseline/FreeFuzz/src/config/demo_torch.conf"

if [ ! -f "$CONFIG_FILE" ]; then
    # 尝试其他路径
    for path in \
        "../config/demo_torch.conf" \
        "../../config/demo_torch.conf" \
        "./demo_torch.conf"; do
        if [ -f "$path" ]; then
            CONFIG_FILE="$path"
            break
        fi
    done
fi

if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ Config file not found!"
    echo "   Tried: /data1/tzh/FreeFuzz-baseline/FreeFuzz/src/config/demo_torch.conf"
    echo "   Please check config file location"
    exit 1
fi

echo "Config file: $CONFIG_FILE"
echo ""

# =============================================================================
# API 列表（按优先级排序）
# =============================================================================

declare -a APIS=(
    # 重点 API（优先运行）
    "torch.nn.LSTM:15000"
    "torch.nn.GRU:15000"
    "torch.nn.RNN:12000"
    
    # Transformer
    "torch.nn.MultiheadAttention:15000"
    "torch.nn.TransformerEncoderLayer:20000"
    "torch.nn.TransformerDecoderLayer:20000"
    
    # Normalization
    "torch.nn.BatchNorm2d:8000"
    "torch.nn.LayerNorm:8000"
    "torch.nn.GroupNorm:8000"
    
    # Convolution
    "torch.nn.Conv2d:5000"
    "torch.nn.Conv1d:5000"
    "torch.nn.Conv3d:5000"
    
    # Others
    "torch.nn.Linear:8000"
    "torch.nn.ReLU:3000"
    "torch.nn.GELU:3000"
    "torch.nn.Sigmoid:3000"
)

# =============================================================================
# 辅助函数
# =============================================================================

get_running_count() {
    # 统计当前运行的 benchmark 进程数
    local count=$(ps aux | grep "[b]enchmark_full_oracle.py" | wc -l)
    echo "$count"
}

is_completed() {
    local log_file="$1"
    
    if [ ! -f "$log_file" ]; then
        return 1  # 日志不存在 = 未完成
    fi
    
    # 检查是否已完成或饱和
    if grep -q "Fuzzing completed" "$log_file" 2>/dev/null; then
        return 0  # 已完成
    fi
    
    if grep -q "Saturation reached" "$log_file" 2>/dev/null; then
        return 0  # 已饱和（视为完成）
    fi
    
    return 1  # 未完成
}

has_checkpoint() {
    local output_dir="$1"
    
    # 检查是否存在 checkpoint 文件
    if [ -d "$output_dir" ]; then
        if ls "$output_dir"/*checkpoint*.pkl >/dev/null 2>&1; then
            return 0  # 有 checkpoint
        fi
    fi
    
    return 1  # 无 checkpoint
}

get_checkpoint_iteration() {
    local output_dir="$1"
    
    # 从 checkpoint metadata 中读取迭代次数
    local meta_file=$(ls "$output_dir"/*metadata.json 2>/dev/null | head -1)
    
    if [ -f "$meta_file" ]; then
        local iter=$(grep -oP '"iteration":\s*\K\d+' "$meta_file" 2>/dev/null)
        echo "${iter:-0}"
    else
        echo "0"
    fi
}

check_segfault() {
    local log_file="$1"
    
    # 检查是否有段错误
    if [ -f "$log_file" ]; then
        if grep -q "Segmentation fault\|core dumped" "$log_file" 2>/dev/null; then
            return 0  # 有段错误
        fi
    fi
    
    return 1  # 无段错误
}

# =============================================================================
# 主循环：智能启动实验
# =============================================================================

echo "=================================================="
echo "Starting Intelligent Resume (Safe Mode)"
echo "=================================================="
echo ""

TOTAL=${#APIS[@]}
STARTED=0
SKIPPED=0
RESUMED=0
FAILED=0

for api_entry in "${APIS[@]}"; do
    IFS=':' read -r API_NAME MAX_ITER <<< "$api_entry"
    API_CLEAN=$(echo "$API_NAME" | tr '.' '_')
    
    OUTPUT_DIR="${API_CLEAN}"
    LOG_FILE="${API_CLEAN}.log"
    PID_FILE="${API_CLEAN}.pid"
    
    echo ""
    echo "---------------------------------------------------"
    
    # =========================================================================
    # 检查是否已完成
    # =========================================================================
    if is_completed "$LOG_FILE"; then
        echo "✅ [SKIP] $API_NAME - Already completed"
        SKIPPED=$((SKIPPED + 1))
        continue
    fi
    
    # =========================================================================
    # 检查是否已在运行
    # =========================================================================
    if [ -f "$PID_FILE" ]; then
        OLD_PID=$(cat "$PID_FILE")
        if ps -p "$OLD_PID" > /dev/null 2>&1; then
            echo "🟢 [RUNNING] $API_NAME - PID: $OLD_PID"
            STARTED=$((STARTED + 1))
            continue
        fi
    fi
    
    # =========================================================================
    # 检查之前是否崩溃
    # =========================================================================
    if check_segfault "$LOG_FILE"; then
        echo "⚠️  [WARNING] $API_NAME - Previous segfault detected"
        echo "   Last 10 lines of log:"
        tail -10 "$LOG_FILE" | sed 's/^/   /'
        echo ""
        echo "   Will retry..."
        # 备份崩溃日志
        cp "$LOG_FILE" "${LOG_FILE}.crash_backup_$(date +%s)"
    fi
    
    # =========================================================================
    # 等待直到并发数低于限制
    # =========================================================================
    while true; do
        RUNNING=$(get_running_count)
        
        if [ "$RUNNING" -lt "$MAX_CONCURRENT" ]; then
            break
        fi
        
        echo "⏳ [WAIT] Waiting for slot to free up... (Running: $RUNNING/$MAX_CONCURRENT)"
        sleep $CHECK_INTERVAL
    done
    
    # =========================================================================
    # 启动/恢复实验
    # =========================================================================
    
    # 检查是否有 checkpoint
    RESUME_MSG=""
    if has_checkpoint "$OUTPUT_DIR"; then
        CHECKPOINT_ITER=$(get_checkpoint_iteration "$OUTPUT_DIR")
        RESUME_MSG=" (resuming from iteration $CHECKPOINT_ITER)"
        RESUMED=$((RESUMED + 1))
    fi
    
    STARTED=$((STARTED + 1))
    echo ""
    echo "[$STARTED/$TOTAL] 🚀 Starting: $API_NAME${RESUME_MSG}"
    echo "   Output: $OUTPUT_DIR"
    echo "   Log: $LOG_FILE"
    
    # 启动实验
    nohup python3 ../benchmark_full_oracle.py \
        --api "$API_NAME" \
        --max-iterations "$MAX_ITER" \
        --output "$OUTPUT_DIR" \
        --conf "$CONFIG_FILE" \
        >> "$LOG_FILE" 2>&1 &
    
    NEW_PID=$!
    echo "$NEW_PID" > "$PID_FILE"
    echo "   ✅ PID: $NEW_PID"
    
    # 等待几秒，检查是否立即崩溃
    sleep 5
    
    if ps -p "$NEW_PID" > /dev/null 2>&1; then
        echo "   ✓ Process still running (healthy)"
    else
        echo "   ❌ Process died immediately!"
        FAILED=$((FAILED + 1))
        
        # 显示崩溃原因
        echo "   Last 20 lines of log:"
        tail -20 "$LOG_FILE" | sed 's/^/   /'
        
        continue
    fi
    
    # 错开启动
    echo ""
    echo "   Waiting ${STAGGER_DELAY}s before next start..."
    sleep $STAGGER_DELAY
done

# =============================================================================
# 持续监控
# =============================================================================

echo ""
echo "=================================================="
echo "Initial Launch Complete"
echo "=================================================="
echo ""
echo "Started:  $STARTED"
echo "Resumed:  $RESUMED"
echo "Skipped:  $SKIPPED"
echo "Failed:   $FAILED"
echo "Total:    $TOTAL"
echo ""
echo "Now entering monitoring mode..."
echo "Single experiment will run at a time (safe mode)"
echo ""

# 持续监控，当实验完成时自动启动下一个
QUEUE_INDEX=0
CHECK_COUNT=0

while true; do
    sleep $CHECK_INTERVAL
    
    RUNNING=$(get_running_count)
    
    if [ "$RUNNING" -eq 0 ]; then
        # 检查是否还有未完成的实验
        PENDING=0
        for api_entry in "${APIS[@]}"; do
            IFS=':' read -r API_NAME MAX_ITER <<< "$api_entry"
            API_CLEAN=$(echo "$API_NAME" | tr '.' '_')
            LOG_FILE="${API_CLEAN}.log"
            
            if ! is_completed "$LOG_FILE"; then
                PENDING=$((PENDING + 1))
            fi
        done
        
        if [ "$PENDING" -eq 0 ]; then
            echo ""
            echo "=================================================="
            echo "✅ All Experiments Finished"
            echo "=================================================="
            
            # 生成最终报告
            if [ -f "./monitor.sh" ]; then
                ./monitor.sh > final_report.txt 2>&1
                echo "Final report saved to: final_report.txt"
            fi
            
            echo ""
            
            # 清理控制器 PID
            rm -f controller.pid
            
            exit 0
        else
            echo ""
            echo "⚠️  All running experiments finished, but $PENDING still pending"
            echo "   This might indicate all experiments are failing"
            echo "   Check logs for errors"
            echo ""
            
            # 等待一段时间再检查
            sleep 60
        fi
    fi
    
    # 定期输出状态（每 5 次检查）
    CHECK_COUNT=$((CHECK_COUNT + 1))
    if [ $((CHECK_COUNT % 5)) -eq 0 ]; then
        echo "[$(date +%H:%M:%S)] Status: $RUNNING running"
        
        # 显示当前运行的实验
        if [ "$RUNNING" -gt 0 ]; then
            for pid_file in *.pid; do
                [ -e "$pid_file" ] || continue
                
                API=$(basename "$pid_file" .pid)
                PID=$(cat "$pid_file")
                
                if ps -p "$PID" > /dev/null 2>&1; then
                    # 尝试提取进度
                    LOG="${API}.log"
                    if [ -f "$LOG" ]; then
                        LAST_CHECKPOINT=$(grep "Checkpoint:" "$LOG" | tail -1)
                        if [ -n "$LAST_CHECKPOINT" ]; then
                            echo "   → $API: $LAST_CHECKPOINT"
                        else
                            echo "   → $API: Running..."
                        fi
                    fi
                fi
            done
        fi
        
        echo ""
    fi
done