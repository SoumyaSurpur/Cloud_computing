#!/usr/bin/env bash
# ==============================================================================
# Sysbench CPU Benchmark Automation Script
# Cloud Computing Laboratory - Experiment 1: Hypervisor Performance Analysis
# Author: Soumya Surpur
# ==============================================================================

set -euo pipefail

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
HOSTNAME_VAL=$(hostname)
OUTPUT_FILE="sysbench_result_${HOSTNAME_VAL}_${TIMESTAMP}.log"

echo "========================================================================" | tee "${OUTPUT_FILE}"
echo "    CLOUD COMPUTING LAB - HYPERVISOR CPU BENCHMARK RUNNER               " | tee -a "${OUTPUT_FILE}"
echo "========================================================================" | tee -a "${OUTPUT_FILE}"
echo "Execution Timestamp : $(date)" | tee -a "${OUTPUT_FILE}"
echo "Host Machine / VM   : ${HOSTNAME_VAL}" | tee -a "${OUTPUT_FILE}"
echo "Operating System    : $(uname -s) $(uname -r) $(uname -m)" | tee -a "${OUTPUT_FILE}"
echo "------------------------------------------------------------------------" | tee -a "${OUTPUT_FILE}"

echo -e "\n[1/3] Inspecting Virtual Hardware Configuration..." | tee -a "${OUTPUT_FILE}"
echo "--- CPU Architecture ---" | tee -a "${OUTPUT_FILE}"
lscpu | grep -E "Model name|CPU\(s\)|Thread\(s\) per core|Core\(s\) per socket|Socket\(s\)|Virtualization" || true | tee -a "${OUTPUT_FILE}"

echo -e "\n--- Memory Allocation ---" | tee -a "${OUTPUT_FILE}"
free -h | tee -a "${OUTPUT_FILE}"

echo -e "\n--- Storage Filesystem ---" | tee -a "${OUTPUT_FILE}"
df -h / | tee -a "${OUTPUT_FILE}"

echo -e "\n[2/3] Checking and Installing Sysbench..." | tee -a "${OUTPUT_FILE}"
if ! command -v sysbench &> /dev/null; then
    echo "Sysbench not found. Updating package repositories and installing..." | tee -a "${OUTPUT_FILE}"
    sudo apt-get update -y && sudo apt-get install -y sysbench
fi

echo "Sysbench binary verified:" | tee -a "${OUTPUT_FILE}"
sysbench --version | tee -a "${OUTPUT_FILE}"

echo -e "\n[3/3] Running CPU Benchmark (Prime Search up to 20,000)..." | tee -a "${OUTPUT_FILE}"
echo "Command: sysbench cpu --cpu-max-prime=20000 run" | tee -a "${OUTPUT_FILE}"
echo "------------------------------------------------------------------------" | tee -a "${OUTPUT_FILE}"
sysbench cpu --cpu-max-prime=20000 run | tee -a "${OUTPUT_FILE}"

echo -e "\n========================================================================" | tee -a "${OUTPUT_FILE}"
echo "Benchmark completed successfully." | tee -a "${OUTPUT_FILE}"
echo "Log file saved to: ${OUTPUT_FILE}" | tee -a "${OUTPUT_FILE}"
echo "========================================================================" | tee -a "${OUTPUT_FILE}"
