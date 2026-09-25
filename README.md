# Cloud Computing Laboratory

![Course](https://img.shields.io/badge/Course-Cloud%20Computing-blue)
![Hypervisors](https://img.shields.io/badge/Hypervisors-Proxmox%20VE%20%7C%20VMware%20Workstation-orange)
![Benchmark](https://img.shields.io/badge/Benchmark-Sysbench%20CPU%2020k%20Primes-brightgreen)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)

# Experiment 1: Performance Analysis of Type-1 and Type-2 Hypervisors

## Executive Summary

Experiment 1 presents an empirical performance evaluation comparing a **Type-1 Bare-Metal Hypervisor (Proxmox VE / KVM)** against a **Type-2 Hosted Hypervisor (VMware Workstation Pro on Windows)**.

Both virtual environments were provisioned with standardized compute, memory, and storage constraints (**2 vCPU, 2 GB RAM, 20 GB Disk**) running **Ubuntu Linux 22.04 LTS**. The computational efficiency of both virtualization layers was benchmarked using the standard `sysbench` CPU prime-number calculation stress test (`--cpu-max-prime=20000`).

### Key Empirical Finding

> **Proxmox VE (Type-1 Bare-Metal) achieved a computational throughput of 1,587.47 Events/sec compared to VMware Workstation's 636.80 Events/sec — delivering a 2.49x (+149.29%) performance advantage and reducing average latency by 59.87% (0.63 ms vs 1.57 ms).**

---

## Table of Contents

1. [Architectural Overview](#1-architectural-overview)
2. [Virtual Machine Specifications](#2-virtual-machine-specifications)
3. [Experimental Methodology](#3-experimental-methodology)
4. [Empirical Results & Verified Evidence](#4-empirical-results--verified-evidence)
5. [Performance Comparison Matrix](#5-performance-comparison-matrix)
6. [Analytical Visualizations & Charts](#6-analytical-visualizations--charts)
7. [In-Depth Technical Analysis](#7-in-depth-technical-analysis)
8. [Practical Engineering Takeaways](#8-practical-engineering-takeaways)
9. [Automation Scripts & Reproduction](#9-automation-scripts--reproduction)
10. [Repository Structure](#10-repository-structure)

---

## 1. Architectural Overview

Virtualization fundamentally alters how computing resources are scheduled, mapped, and consumed. The two dominant hypervisor classifications represent distinct trade-offs between architectural isolation, system overhead, and deployment convenience:

```
   ===================================          ===================================
     TYPE-1: BARE-METAL HYPERVISOR                 TYPE-2: HOSTED HYPERVISOR
     (e.g., Proxmox VE / Linux KVM)                (e.g., VMware Workstation)
   ===================================          ===================================

    +-------------------------------+            +-------------------------------+
    |   Guest VM (Ubuntu Linux)     |            |   Guest VM (Ubuntu Linux)     |
    +-------------------------------+            +-------------------------------+
                   |                                            |
                   v                                            v
    +-------------------------------+            +-------------------------------+
    |  Proxmox VE (KVM Hypervisor)  |            |  VMware Workstation (App)     |
    |      Direct Ring-0 Host       |            +-------------------------------+
    +-------------------------------+                           |
                   |                                            v
                   |                             +-------------------------------+
                   |                             |  Host OS (Windows 11 NT)      |
                   |                             +-------------------------------+
                   v                                            v
    +-------------------------------+            +-------------------------------+
    |     Bare-Metal Hardware       |            |     Bare-Metal Hardware       |
    |   (CPU, Memory, Disk, NIC)    |            |   (CPU, Memory, Disk, NIC)    |
    +-------------------------------+            +-------------------------------+
```

### Architectural Distinctions

- **Type-1 Hypervisor (Bare-Metal - Proxmox VE)**: Runs directly on physical hardware. The KVM module converts the host Linux kernel into a bare-metal hypervisor. CPU instructions generated within guest VMs execute directly on hardware virtualization extensions (Intel VT-x / AMD-V) in VMX non-root mode, with hypervisor intervention required only for privileged hardware events.
- **Type-2 Hypervisor (Hosted - VMware Workstation)**: Operates as an application process managed by a general-purpose host OS (Windows 11). Guest CPU calls, interrupts, and I/O requests must pass through VMware's Virtual Machine Monitor (VMM) and subsequently traverse the Windows NT kernel scheduler and driver stack, introducing measurable context-switching latency and scheduling contention.

---

## 2. Virtual Machine Specifications

To guarantee scientific parity, both guest environments were deployed with identical virtual resource allocations:

| Specification Parameter | Proxmox VE (Type-1) | VMware Workstation (Type-2) | Configuration Parity |
| :--- | :--- | :--- | :---: |
| **Virtual Machine Tag** | `CC-Experiment1-type1` | `CC-Expt1-Type2` | Standardized |
| **VM Host Identity** | `vm01@vm01-Standard-PC-i440FX-PIIX-1996` | `soumya@soumya-virtual-machine` | Independent Host Instances |
| **Guest Operating System** | Ubuntu 22.04 LTS (x86_64) | Ubuntu 22.04 LTS (x86_64) | **Identical** |
| **Virtual vCPU Cores** | 2 vCPUs (1 socket, 2 cores) | 2 vCPUs (1 processor, 2 cores) | **Identical (2 Cores)** |
| **Virtual Memory (RAM)** | 2048 MB (2.0 GiB) | 2048 MB (2.0 GiB) | **Identical (2 GB)** |
| **Virtual Storage** | 20.0 GB Virtual Disk | 20.0 GB Virtual Disk | **Identical (20 GB)** |
| **Benchmark Tool** | `sysbench 1.0.20` | `sysbench 1.0.20` | **Identical Version** |
| **Stress Workload** | CPU Prime calculation (limit: 20,000) | CPU Prime calculation (limit: 20,000) | **Identical Workload** |

---

## 3. Experimental Methodology

The experiment was carried out through the following structured phases:

1. **Hypervisor Provisioning**:
   - Deployed a target VM on Proxmox VE via the web administration interface attached to virtual bridge `vmbr0`.
   - Deployed a local VM on VMware Workstation Pro with NAT virtual network adapter.
2. **System Verification Inside Guests**:
   - Validated kernel and architecture via `uname -a` and `hostnamectl`.
   - Inspected active compute topology using `lscpu`.
   - Verified RAM and swap allocation using `free -h`.
   - Verified root partition disk sizing using `df -h /`.
3. **Benchmarking Execution**:
   - Installed the Sysbench benchmarking utility:
     ```bash
     sudo apt update && sudo apt install sysbench -y
     ```
   - Executed CPU computational stress test:
     ```bash
     sysbench cpu --cpu-max-prime=20000 run
     ```
4. **Data Acquisition**:
   - Extracted total execution duration, events completed within 10 seconds, events per second (throughput), and full latency distributions (min, avg, 95th percentile, max).

---

## 4. Empirical Results & Verified Evidence

### Type-1 Hypervisor Result (Proxmox VE Console)

Execution of Sysbench CPU benchmark inside the Proxmox VE guest environment:

![Proxmox VE Type-1 Benchmark Console](images/1.png)

*Figure 1: Proxmox VE (Type-1 Hypervisor) Sysbench execution output on VM `vm01`.*

---

### Type-2 Hypervisor Result (VMware Workstation Console)

Execution of Sysbench CPU benchmark on VMware Workstation within `soumya@soumya-virtual-machine`:

![VMware Workstation Type-2 Benchmark Terminal](images/2.png)

*Figure 2: VMware Workstation (Type-2 Hypervisor) Sysbench execution output on `soumya@soumya-virtual-machine`.*

---

## 5. Performance Comparison Matrix

The table below details the exact measurements recorded during both benchmark runs:

| Performance Metric | Proxmox VE (Type-1) | VMware Workstation (Type-2) | Measured Delta | Architectural Winner |
| :--- | :---: | :---: | :---: | :---: |
| **Hypervisor Architecture** | Bare-Metal (KVM) | Hosted (Windows Host) | Direct vs Indirect | **Type-1** |
| **Guest Virtual CPUs** | 2 vCPUs | 2 vCPUs | Parity | Matched |
| **Guest Allocated RAM** | 2 GB | 2 GB | Parity | Matched |
| **Benchmark Prime Limit** | 20,000 | 20,000 | Parity | Matched |
| **Benchmark Duration Window** | **10.0005 s** | **10.0016 s** | ~0.01% variance | Standard 10s Window |
| **Total Events Processed** | **15,877** | **6,370** | **+9,507 events (+149.25%)** | **Proxmox VE (Type-1)** |
| **Throughput (Events/sec)** | **1,587.47 EPS** | **636.80 EPS** | **+950.67 EPS (+149.29%)** | **Proxmox VE (2.49x Speedup)** |
| **Minimum Latency** | **0.59 ms** | **1.31 ms** | **-0.72 ms (-54.96%)** | **Proxmox VE (Lower)** |
| **Average Latency** | **0.63 ms** | **1.57 ms** | **-0.94 ms (-59.87%)** | **Proxmox VE (Lower)** |
| **95th Percentile Latency** | **0.65 ms** | **2.07 ms** | **-1.42 ms (-68.60%)** | **Proxmox VE (Tighter Variance)** |
| **Maximum Latency** | **1.34 ms** | **6.84 ms** | **-5.50 ms (-80.41%)** | **Proxmox VE (Fewer Spikes)** |

---

## 6. Analytical Visualizations & Charts

### Chart 1: Computational Throughput Comparison

Proxmox VE delivered **1,587.47 Events/sec** versus VMware Workstation's **636.80 Events/sec**, representing a **2.49x (+149.29%)** throughput advantage.

![Throughput Comparison](images/events_per_second_comparison.png)

*Figure 3: CPU Throughput comparison illustrating the bare-metal efficiency of Proxmox VE.*

---

### Chart 2: Latency Distribution Comparison

Proxmox VE achieved substantially lower latency across all percentiles. While VMware Workstation experienced scheduling latency spikes up to **6.84 ms**, Proxmox VE maintained a maximum latency of only **1.34 ms**.

![Latency Comparison](images/latency_comparison.png)

*Figure 4: Latency breakdown comparison across Min, Avg, 95th Percentile, and Max bounds.*

---

### Chart 3: Total Computational Events Completed

Within the standard 10-second test window, Proxmox VE successfully calculated **15,877 events**, whereas VMware Workstation completed **6,370 events**.

![Total Events Comparison](images/total_events_comparison.png)

*Figure 5: Total Sysbench prime-number verification events completed in 10 seconds.*

---

### Chart 4: Multi-Panel Performance Dashboard

A comprehensive four-quadrant overview combining throughput, event capacity, average latency, and 95th percentile latency:

![Overall Dashboard](images/overall_performance_dashboard.png)

*Figure 6: Comprehensive 4-panel performance dashboard summarizing Experiment 1 findings.*

---

## 7. In-Depth Technical Analysis

The experimental data establishes significant performance and latency disparities between bare-metal and hosted virtualization.

### 1. Direct Ring-0 Hardware Execution vs Trap-and-Emulate
- **Proxmox VE**: Leveraging Linux KVM, virtual CPU execution runs in hardware VMX non-root mode. User-space guest compute instructions (such as arithmetic loops in Sysbench) execute at near-native CPU speeds directly on the underlying processor cores without trapping into software emulation.
- **VMware Workstation**: VMware runs on top of the Windows NT OS. Even with hardware-assisted virtualization enabled, privileged transitions must coordinate with the host OS kernel. Instruction emulation and host-level API translations introduce cumulative microsecond-level penalties on every instruction boundary.

### 2. Operating System Scheduling & Contention
- **Proxmox VE**: Guest virtual CPU threads are managed directly by the Linux kernel's **Completely Fair Scheduler (CFS)** operating at Ring 0. The hypervisor has sole control over physical hardware allocation with negligible background process interference.
- **VMware Workstation**: Guest vCPU threads run as user-mode threads under Windows (`vmware-vmx.exe`). They compete for physical CPU time slices with Windows background services, GUI rendering processes (`dwm.exe`), antivirus scanning, and background network services. This explains why VMware exhibited a **6.84 ms maximum latency spike** compared to Proxmox's **1.34 ms**.

### 3. Memory Translation Hierarchy
- **Proxmox VE**: Employs Extended Page Tables (EPT / SLAT) to translate Guest Physical Addresses (GPA) directly to Host Physical Addresses (HPA) in hardware.
- **VMware Workstation**: Address translation traverses a two-tier mapping: GPA $\rightarrow$ Host Virtual Address (HVA) $\rightarrow$ Host Physical Address (HPA). The intermediate page table lookups amplify cache miss penalties during compute-intensive loops.

---

## 8. Practical Engineering Takeaways

| Decision Criteria | Type-1 Hypervisor (Proxmox VE / KVM) | Type-2 Hypervisor (VMware Workstation) |
| :--- | :--- | :--- |
| **Primary Deployment Domain** | Enterprise Data Centers, Private Cloud, Production Clusters | Local Software Development, Testing, Sandboxing |
| **Performance Efficiency** | **Maximum (~95–99% bare-metal performance)** | **Moderate (~40–70% bare-metal performance)** |
| **Latency Predictability** | **Extremely high (consistent < 1 ms latency)** | **Moderate (subject to host OS jitter & spikes)** |
| **Ease of Setup** | Requires dedicated server hardware or bare partition | Installs as a standard desktop software application |
| **Host System Requirement** | Installs as the standalone Host Operating System | Runs on existing Windows, macOS, or desktop Linux |
| **Cost & Licensing** | Open-source (Proxmox VE / KVM) with optional support | Proprietary / Desktop license |

---

## 9. Automation Scripts & Reproduction

All benchmark execution and analytical plotting tools are included in the [`scripts/`](scripts/) folder:

### 1. Execute Benchmark on Linux VM
Run the automated benchmark script inside your target Ubuntu VM:
```bash
chmod +x scripts/benchmark.sh
./scripts/benchmark.sh
```

### 2. Compare Results via Python Parser
Run the quantitative comparator script:
```bash
python scripts/parse_sysbench.py
```

### 3. Regenerate Performance Plots
Re-generate the 4 visualization charts in the `images/` directory:
```bash
python scripts/generate_plots.py
```

---

## 10. Repository Structure

```text
Cloud_Computing/
│
├── README.md                                  # Central Laboratory Documentation & Experiment 1 Overview
├── LAB_REPORT.md                              # Formal Academic Laboratory Report Submission
├── Lab-Manual-Hypervisor-Performance-Analysis... # Complete Hypervisor Performance Analysis Lab Manual
├── type1.pdf                                  # Type-1 Hypervisor – Proxmox VE Documentation
├── type2.pdf                                  # Type-2 Hypervisor – VMware Workstation Documentation
│
├── images/                                    # Experimental Evidence & Generated Visualizations
│   ├── 1.png                                  # Proxmox VE (Type-1) Benchmark Terminal Screenshot
│   ├── 2.png                                  # VMware Workstation (Type-2) Benchmark Screenshot
│   ├── events_per_second_comparison.png       # CPU Throughput Comparison Bar Chart
│   ├── latency_comparison.png                 # Latency Breakdown Bar Chart (Min, Avg, P95, Max)
│   ├── total_events_comparison.png            # Total Events Completed in 10s Chart
│   ├── overall_performance_dashboard.png      # Multi-panel Analytical Evaluation Dashboard
│   ├── proxmox_dashboard.jpg                  # Proxmox VE Cluster Resource Dashboard
│   ├── proxmox_vm_summary.jpg                 # Proxmox VE Hardware Allocation Summary
│   ├── proxmox_memory_graph.jpg               # Proxmox VE Memory Utilization Over Time
│   ├── proxmox_disk_io.jpg                    # Proxmox VE Storage I/O Graph
│   ├── vmware_top.jpg                         # VMware Guest Resource Consumption (top)
│   └── vmware_sysbench_install.jpg            # VMware Sysbench Package Setup
│
└── scripts/                                   # Automation & Analytical Scripts
    ├── benchmark.sh                           # Sysbench VM Execution & Hardware Logging Script
    ├── generate_plots.py                      # Matplotlib Visualization Generator
    └── parse_sysbench.py                      # Quantitative Delta & Speedup Calculator

```
---

