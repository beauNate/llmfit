#!/usr/bin/env bash
# Demo script for llmfit - simulates typing commands
set -e

LLMFIT="./target/release/llmfit"

# Simulate typing effect
type_cmd() {
    local cmd="$1"
    local delay="${2:-0.04}"
    printf "\n\033[1;32m❯\033[0m "
    for (( i=0; i<${#cmd}; i++ )); do
        printf "%s" "${cmd:$i:1}"
        sleep "$delay"
    done
    echo
    sleep 0.3
}

pause() {
    sleep "${1:-2}"
}

clear
echo ""
echo "  ╔══════════════════════════════════════╗"
echo "  ║         llmfit demo v0.7.3           ║"
echo "  ║  Right-size LLMs to your hardware    ║"
echo "  ╚══════════════════════════════════════╝"
echo ""
pause 2

# 1. System detection
echo ""
echo "  ━━━ 1. Hardware Detection ━━━"
type_cmd "llmfit system"
$LLMFIT system
pause 3

# 2. Fit - find models that run on this hardware
echo ""
echo "  ━━━ 2. Find Models That Fit ━━━"
type_cmd "llmfit fit -n 10"
$LLMFIT fit -n 10
pause 3

# 3. Search for a specific model
echo ""
echo "  ━━━ 3. Search Models ━━━"
type_cmd "llmfit search llama"
$LLMFIT search llama
pause 3

# 4. Detailed model info
echo ""
echo "  ━━━ 4. Model Details ━━━"
type_cmd "llmfit info 'Llama 3.1 8B'"
$LLMFIT info 'Llama 3.1 8B'
pause 3

# 5. Recommend for a use case
echo ""
echo "  ━━━ 5. Recommendations by Use Case ━━━"
type_cmd "llmfit recommend -n 5 --use-case coding"
$LLMFIT recommend -n 5 --use-case coding
pause 3

# 6. Compare models
echo ""
echo "  ━━━ 6. Compare Top Models ━━━"
type_cmd "llmfit diff -n 5"
$LLMFIT diff -n 5
pause 3

# 7. Plan hardware for a model
echo ""
echo "  ━━━ 7. Hardware Planning ━━━"
type_cmd "llmfit plan 'Llama 3.1 70B' --context 4096"
$LLMFIT plan 'Llama 3.1 70B' --context 4096
pause 3

# 8. JSON output for automation
echo ""
echo "  ━━━ 8. JSON Output for Automation ━━━"
type_cmd "llmfit recommend -n 3 --json | head -20"
$LLMFIT recommend -n 3 --json | head -20
pause 2

echo ""
echo ""
echo "  ✨ Learn more: https://github.com/AlexsJones/llmfit"
echo ""
pause 3
