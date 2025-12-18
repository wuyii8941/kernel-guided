#!/bin/bash
# =============================================================================
# 🧪 Poison Injection Batch Test
# =============================================================================
# 优先测试对 Inf/NaN/Extreme Values 敏感的 API
# 迭代次数基于饱和度分析，避免浪费

set -e  # Exit on error

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BENCHMARK_SCRIPT="benchmark_full_oracle.py"
OUTPUT_BASE="poison_results_$(date +%Y%m%d_%H%M)"
CONF="demo_torch.conf"

# -----------------------------------------------------------------------------
# Pre-flight Checks
# -----------------------------------------------------------------------------
echo "=============================================="
echo "🧪 POISON INJECTION BATCH TEST"
echo "=============================================="
echo "Script Dir: $SCRIPT_DIR"
echo "Working Dir: $(pwd)"
echo "Started: $(date)"
echo "=============================================="

# Check if benchmark script exists
if [[ -f "$SCRIPT_DIR/$BENCHMARK_SCRIPT" ]]; then
    BENCHMARK_PATH="$SCRIPT_DIR/$BENCHMARK_SCRIPT"
    echo "✅ Found: $BENCHMARK_PATH"
elif [[ -f "./$BENCHMARK_SCRIPT" ]]; then
    BENCHMARK_PATH="./$BENCHMARK_SCRIPT"
    echo "✅ Found: $BENCHMARK_PATH"
elif [[ -f "$BENCHMARK_SCRIPT" ]]; then
    BENCHMARK_PATH="$BENCHMARK_SCRIPT"
    echo "✅ Found: $BENCHMARK_PATH"
else
    echo "❌ ERROR: Cannot find $BENCHMARK_SCRIPT"
    echo ""
    echo "Please either:"
    echo "  1. Copy $BENCHMARK_SCRIPT to current directory, or"
    echo "  2. Run this script from the directory containing $BENCHMARK_SCRIPT"
    echo ""
    echo "Current directory contents:"
    ls -la *.py 2>/dev/null || echo "  (no .py files found)"
    exit 1
fi

# Check config file
if [[ ! -f "config/$CONF" ]] && [[ ! -f "$CONF" ]]; then
    echo "⚠️  WARNING: Config file '$CONF' not found, will search in default paths"
fi

# Create output directory
mkdir -p "$OUTPUT_BASE"
echo "📁 Output Dir: $(pwd)/$OUTPUT_BASE"
echo "=============================================="

# -----------------------------------------------------------------------------
# Test Function
# -----------------------------------------------------------------------------
run_test() {
    local api="$1"
    local iters="$2"
    local desc="$3"
    local output_name="$4"
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🔬 Testing: $api"
    echo "   Iterations: $iters"
    echo "   Reason: $desc"
    echo "   Output: $OUTPUT_BASE/$output_name"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    local start_time=$(date +%s)
    
    python "$BENCHMARK_PATH" \
        --api "$api" \
        --max-iterations "$iters" \
        --output "$OUTPUT_BASE/$output_name" \
        --conf "$CONF" \
        --diff-bound 1e-6
    
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    echo ""
    echo "⏱️  Completed in ${duration}s"
    echo ""
}

# -----------------------------------------------------------------------------
# Priority 1: Softmax (最敏感 - exp溢出 + 除法)
# -----------------------------------------------------------------------------
echo ""
echo "[1/5] 🥇 torch.nn.Softmax"
run_test "torch.nn.Softmax" 2000 "exp(inf)=overflow, sum=0 causes div-by-zero" "softmax"

# -----------------------------------------------------------------------------
# Priority 2: LayerNorm (std=0 除法)
# -----------------------------------------------------------------------------
echo ""
echo "[2/5] 🥈 torch.nn.LayerNorm"
run_test "torch.nn.LayerNorm" 2000 "div by std≈0 when inputs are extreme" "layernorm"

# -----------------------------------------------------------------------------
# Priority 3: BatchNorm2d (running stats 累积)
# -----------------------------------------------------------------------------
echo ""
echo "[3/5] 🥉 torch.nn.BatchNorm2d"
run_test "torch.nn.BatchNorm2d" 2000 "running_mean/var accumulates NaN/Inf" "batchnorm2d"

# -----------------------------------------------------------------------------
# Priority 4: CrossEntropyLoss (log_softmax 组合)
# -----------------------------------------------------------------------------
echo ""
echo "[4/5] torch.nn.CrossEntropyLoss"
run_test "torch.nn.CrossEntropyLoss" 1000 "log(softmax(x)) chain, log(0)=-inf" "crossentropy"

# -----------------------------------------------------------------------------
# Priority 5: LSTM (复杂计算图)
# -----------------------------------------------------------------------------
echo ""
echo "[5/5] torch.nn.LSTM"
run_test "torch.nn.LSTM" 2000 "multi-gate sigmoid/tanh saturation" "lstm"

# -----------------------------------------------------------------------------
# Summary
# -----------------------------------------------------------------------------
echo ""
echo "=============================================="
echo "✅ BATCH TEST COMPLETE"
echo "=============================================="
echo "Finished: $(date)"
echo ""
echo "📊 Results Summary:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Find and display results
for dir in "$OUTPUT_BASE"/*/; do
    if [[ -d "$dir" ]]; then
        api_name=$(basename "$dir")
        echo ""
        echo "📁 $api_name:"
        
        # Look for JSON results
        json_file=$(find "$dir" -name "*_results.json" 2>/dev/null | head -1)
        if [[ -n "$json_file" ]] && [[ -f "$json_file" ]]; then
            echo "   $(grep -o '"total_bugs": [0-9]*' "$json_file" 2>/dev/null | head -1 || echo 'No bug count found')"
        fi
        
        # Count bug files
        bug_count=$(find "$dir" -type d -name "bug_*" 2>/dev/null | wc -l)
        echo "   Bug directories: $bug_count"
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📁 Full results: $(pwd)/$OUTPUT_BASE/"
echo "=============================================="