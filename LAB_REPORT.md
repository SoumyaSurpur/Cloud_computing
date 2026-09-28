# LABORATORY REPORT

## Experiment 01: Performance Analysis of Type-1 and Type-2 Hypervisors

---

### Student & Course Metadata
- **Course Name:** Cloud Computing Laboratory
- **Experiment No:** 01
- **Student Name:** Soumya
- **Environment:** Ubuntu Linux 22.04 LTS on Proxmox VE & VMware Workstation Pro
- **Date of Experiment:** September 2026

---

## 1. Aim & Objectives

### Aim
To provision identically configured Ubuntu Linux Virtual Machines across a **Type-1 Bare-Metal Hypervisor (Proxmox VE)** and a **Type-2 Hosted Hypervisor (VMware Workstation Pro)**, inspect their underlying virtualization and virtual hardware configurations, execute standard CPU computational stress benchmarks using `sysbench`, and quantitatively analyze performance and latency trade-offs.

### Key Objectives
1. **Infrastructure Provisioning**: Deploy two independent guest virtual machines with matched virtual resource baselines: 2 vCPU cores, 2048 MB RAM, and 20 GB disk capacity.
2. **System Verification**: Use standard Linux system administration utilities (`hostnamectl`, `lscpu`, `free -h`, `df -h`, `top`) to inspect hardware virtualization abstractions inside both guests.
3. **Benchmarking Execution**: Subject both virtual machines to identical CPU prime-number verification workloads (`--cpu-max-prime=20000`) using `sysbench 1.0.20`.
4. **Data Acquisition & Analysis**: Record empirical metrics including execution duration, total events completed, events per second (throughput), minimum latency, average latency, 95th percentile latency, and maximum latency spikes.
5. **Architectural Assessment**: Understand how host OS scheduling layers, trap-and-emulate instruction translation, and memory page tables impact virtualization efficiency.

---

## 2. Theoretical Background

Virtualization is the fundamental technology enabling cloud computing, allowing physical computing hardware to be abstracted into multiple isolated execution environments known as Virtual Machines (VMs). Hypervisors (Virtual Machine Monitors - VMMs) are categorized into two primary architectural paradigms:

### 2.1 Type-1 Hypervisor (Bare-Metal Hypervisor)
A Type-1 hypervisor runs directly on the bare metal of the host physical server without an intermediate host operating system.
- **Architectural Hierarchy**:
  $$\text{Hardware} \longrightarrow \text{Type-1 Hypervisor (KVM / Proxmox)} \longrightarrow \text{Guest OS (Ubuntu)}$$
- **Representative Systems**: Proxmox VE (Linux KVM), VMware ESXi, Microsoft Hyper-V Server, Xen.
- **Key Characteristics**:
  - The hypervisor operates in Ring-0 / VMX root mode.
  - Guest operating systems execute non-privileged CPU instructions directly on the physical processor using Intel VT-x or AMD-V hardware extensions.
  - Minimal context-switching overhead and near-native hardware execution throughput.
  - Suited for enterprise production cloud data centers, HPC clusters, and mission-critical cloud hosting.

### 2.2 Type-2 Hypervisor (Hosted Hypervisor)
A Type-2 hypervisor runs as a software application on top of an existing, general-purpose host operating system (e.g., Windows 11, macOS, desktop Linux).
- **Architectural Hierarchy**:
  $$\text{Hardware} \longrightarrow \text{Host OS (Windows NT)} \longrightarrow \text{Type-2 Hypervisor (VMware Workstation)} \longrightarrow \text{Guest OS (Ubuntu)}$$
- **Representative Systems**: VMware Workstation, Oracle VM VirtualBox, Parallels Desktop.
- **Key Characteristics**:
  - The hypervisor must request hardware resources via host OS system calls and device drivers.
  - Guest instructions undergo dual layers of scheduling and address translation.
  - Physical resources are shared and contested by both the virtual machine and background host applications/services.
  - Ideal for local software engineering, testing, sandboxing, and educational laboratories.

---

## 3. Hardware & Virtual Machine Configuration

To ensure rigorous experimental control, both virtual machines were configured with identical resource limits:

| Parameter | Proxmox VE (Type-1 Baseline) | VMware Workstation (Type-2 Environment) | Parity Status |
| :--- | :--- | :--- | :---: |
| **Virtual Machine Tag** | `CC-Experiment1-type1` | `CC-Expt1-Type2` | Standardized |
| **VM Host Identity** | `vm01@vm01-Standard-PC-i440FX-PIIX-1996` | `soumya@soumya-virtual-machine` | Independent |
| **Guest Operating System** | Ubuntu 22.04 LTS (64-bit) | Ubuntu 22.04 LTS (64-bit) | **Matched** |
| **Virtual Processor (vCPU)** | 2 vCPUs (1 socket, 2 cores) | 2 vCPUs (1 processor, 2 cores) | **Matched** |
| **Virtual Memory (RAM)** | 2048 MB (2.0 GiB) | 2048 MB (2.0 GiB) | **Matched** |
| **Virtual Disk Allocation** | 20.0 GB SCSI / VirtIO | 20.0 GB NVMe / Virtual SCSI | **Matched** |
| **Network Adapter Mode** | Linux Bridge (`vmbr0`) | Network Address Translation (NAT) | Standardized |
| **Benchmark Utility** | `sysbench 1.0.20` | `sysbench 1.0.20` | **Matched** |
| **Workload Parameter** | Prime calculation up to 20,000 | Prime calculation up to 20,000 | **Matched** |

---

## 4. Step-by-Step Experimental Procedure

### Part A: Type-1 Hypervisor Setup (Proxmox VE)
1. **Accessing Proxmox VE**: Connected to the central Proxmox VE server web GUI over HTTPS (`https://<PROXMOX_SERVER_IP>:8006`).
2. **VM Provisioning**: Used the "Create VM" wizard to allocate VM ID `101`, assigning 2 vCPU cores, 2048 MB memory, and 20 GB disk.
3. **OS Installation**: Mounted the Ubuntu 22.04 ISO image, started the virtual machine, and performed standard OS installation.
4. **Configuration Inspection**: Opened the noVNC terminal console and verified system architecture using `hostnamectl`, `lscpu`, and `free -h`.
5. **Benchmark Execution**: Ran `sysbench cpu --cpu-max-prime=20000 run` and recorded full output metrics.

### Part B: Type-2 Hypervisor Setup (VMware Workstation)
1. **VM Creation**: Launched VMware Workstation Pro on the Windows host and initiated the "New Virtual Machine Wizard".
2. **Hardware Allocation**: Configured 2 vCPU cores, 2048 MB RAM, and 20 GB disk partition; attached Ubuntu 22.04 ISO.
3. **OS Installation & Login**: Completed Ubuntu installation and logged into the newly created guest instance `soumya@soumya-virtual-machine`.
4. **Configuration Inspection**: Executed `hostnamectl`, `lscpu`, `free -h`, and `top` to verify guest state.
5. **Benchmark Execution**: Installed sysbench via `sudo apt update && sudo apt install sysbench -y` and executed the identical benchmark workload:
   ```bash
   sysbench cpu --cpu-max-prime=20000 run
   ```
6. **Data Capture**: Saved console screenshots and output logs for comparative analysis.

---

## 5. Linux System Commands Utilized

| Command | Purpose in Experiment |
| :--- | :--- |
| `hostnamectl` | Displays system hostname, OS distribution, kernel version, and hypervisor identification. |
| `lscpu` | Reports CPU architecture, number of cores, sockets, threads, and hardware virtualization flags. |
| `free -h` | Summarizes total, used, free, and available physical memory and swap space in human-readable units. |
| `df -h /` | Validates root filesystem disk capacity, storage utilization, and mount points. |
| `top` | Live dynamic process viewer to observe CPU utilization, memory consumption, and load averages. |
| `sysbench --version` | Confirms the installed version of the benchmark suite (`sysbench 1.0.20`). |
| `sysbench cpu --cpu-max-prime=20000 run` | Executes prime-number stress test evaluating integer compute throughput and latency. |

---

## 6. Experimental Observations & Screenshot Evidence

### 6.1 Type-1 Hypervisor Evidence (Proxmox VE)

Below is the verified benchmark terminal output from the Proxmox VE guest VM (`vm01`):

![Proxmox VE Type-1 Sysbench Result](images/1.png)

*Figure 1: Proxmox VE (Type-1) Sysbench CPU benchmark execution showing 1,587.47 EPS and 0.63 ms average latency.*

---

### 6.2 Type-2 Hypervisor Evidence (VMware Workstation - Soumya Surpur)

Below is the verified benchmark terminal output from VMware Workstation on `soumya@soumya-virtual-machine`:

![VMware Workstation Type-2 Sysbench Result](images/2.png)

*Figure 2: VMware Workstation (Type-2) Sysbench CPU benchmark execution on `soumya@soumya-virtual-machine` showing 636.80 EPS and 1.57 ms average latency.*

---

## 7. Performance Comparison & Quantitative Matrix

The following table summarizes the raw empirical results recorded from both runs:

| Performance Metric | Proxmox VE (Type-1) | VMware Workstation (Type-2) | Measured Delta | Architectural Advantage |
| :--- | :---: | :---: | :---: | :---: |
| **Virtual Machine Identity** | `vm01` | `soumya-virtual-machine` | Independent | Standardized Baseline |
| **Total Test Duration** | **10.0005 s** | **10.0016 s** | +0.0011 s | Standard 10s Window |
| **Total Events Processed** | **15,877** | **6,370** | **+9,507 events (+149.25%)** | **Proxmox VE (Higher Capacity)** |
| **Throughput (Events/sec)** | **1,587.47 EPS** | **636.80 EPS** | **+950.67 EPS (+149.29%)** | **Proxmox VE (2.49x Faster)** |
| **Minimum Latency** | **0.59 ms** | **1.31 ms** | **-0.72 ms (-54.96%)** | **Proxmox VE (Faster)** |
| **Average Latency** | **0.63 ms** | **1.57 ms** | **-0.94 ms (-59.87%)** | **Proxmox VE (Lower Latency)** |
| **95th Percentile Latency** | **0.65 ms** | **2.07 ms** | **-1.42 ms (-68.60%)** | **Proxmox VE (Predictable)** |
| **Maximum Latency** | **1.34 ms** | **6.84 ms** | **-5.50 ms (-80.41%)** | **Proxmox VE (Fewer Spikes)** |

---

## 8. Graphical Analysis & Visual Comparisons

### Throughput Analysis (Events per Second)

![Throughput Comparison Chart](images/events_per_second_comparison.png)

*Figure 3: CPU Throughput comparison illustrating Proxmox VE's 2.49x speedup.*

**Analysis**: Proxmox VE completed 1,587.47 prime-search events per second compared to 636.80 EPS on VMware Workstation. In a CPU-bound mathematical benchmark, this +149.29% throughput increase highlights the substantial efficiency gained when user-space guest instructions execute directly in hardware VMX non-root mode without intermediate host OS abstraction.

---

### Latency Metrics Breakdown

![Latency Comparison Chart](images/latency_comparison.png)

*Figure 4: Latency comparison (Min, Avg, 95th Percentile, Max) between Proxmox VE and VMware Workstation.*

**Analysis**: 
- **Minimum & Average Latency**: Proxmox VE completed event iterations in an average of 0.63 ms, compared to 1.57 ms on VMware Workstation (a 59.87% latency reduction).
- **95th Percentile**: 95% of all events on Proxmox VE completed within 0.65 ms, showing exceptional scheduling uniformity. Conversely, VMware Workstation’s 95th percentile rose to 2.07 ms.
- **Maximum Latency Spike**: VMware Workstation registered a maximum latency of 6.84 ms (over 5x higher than Proxmox’s 1.34 ms max). This tail latency is directly attributable to Windows thread preemption, host service interrupts, and VMM context switching.

---

### Total Computational Capacity in 10 Seconds

![Total Events Chart](images/total_events_comparison.png)

*Figure 5: Total computational events processed within the identical 10-second test window.*

---

### Comprehensive Multi-Quadrant Performance Dashboard

![Comprehensive Dashboard](images/overall_performance_dashboard.png)

*Figure 6: Complete 4-quadrant comparative performance dashboard.*

---

## 9. Technical Discussion & Architectural Root Causes

The empirical divergence between Proxmox VE and VMware Workstation is explained by several core architectural factors:

### 9.1 Host Operating System Interception & Scheduling Contention
In VMware Workstation (Type-2), the guest virtual machine runs as an application process (`vmware-vmx.exe`) governed by the Windows NT kernel scheduler. The physical CPU cores are simultaneously shared among:
1. Windows kernel interrupts and Deferred Procedure Calls (DPCs).
2. Background operating system services (e.g., Windows Defender, Search Indexer, Telemetry).
3. Foreground GUI applications and Desktop Window Manager (`dwm.exe`).

Whenever the Windows scheduler preempts VMware's thread to serve a host process, the guest VM experiences execution stalls. This manifests as higher tail latency (6.84 ms) and depressed throughput.

In contrast, Proxmox VE (Type-1) runs KVM directly in kernel space. Guest vCPUs are scheduled directly by Linux's Completely Fair Scheduler (CFS) at Ring-0, with zero competing desktop background applications.

### 9.2 VMX Hardware Virtualization vs Emulation Overhead
Proxmox VE delegates CPU instruction execution directly to hardware via Intel VT-x / AMD-V. Guest code runs natively in VMX non-root mode. When privileged operations occur, VM-exits are handled swiftly within the KVM kernel module. In VMware Workstation, VM-exits must be trapped by VMware's VMM and often routed through Windows user/kernel mode barriers (`NtDeviceIoControlFile`), multiplying instruction latency.

### 9.3 Two-Dimensional Memory Virtualization (EPT vs Hosted Paging)
- **Proxmox VE**: Directly maps Guest Physical Addresses (GPA) to Host Physical Addresses (HPA) via hardware Extended Page Tables (EPT / SLAT).
- **VMware Workstation**: Involves a multi-step address mapping: $\text{GPA} \rightarrow \text{HVA (Host Virtual Address)} \rightarrow \text{HPA}$. The added translation level causes higher TLB miss overhead and reduces L1/L2 cache locality during memory-intensive loops.

---

## 10. Conclusion & Key Inferences

1. **Definitive Performance Superiority**: Proxmox VE (Type-1 Bare-Metal) demonstrated a **2.49x throughput advantage (+149.29%)** over VMware Workstation (Type-2) under an identical CPU computational load.
2. **Latency Consistency**: Proxmox VE exhibited **59.87% lower average latency** and eliminated severe tail latency spikes, making it the appropriate choice for latency-sensitive applications (databases, financial trading, real-time microservices).
3. **Deployment Recommendations**:
   - **Type-1 Hypervisors (Proxmox VE / ESXi / KVM)**: Essential for Enterprise Data Centers, Production Cloud Infrastructure, and High-Performance Computing (HPC).
   - **Type-2 Hypervisors (VMware Workstation / VirtualBox)**: Recommended for Local Software Development, Sandboxed Testing, and Educational Classroom Labs where ease of installation on a desktop OS is prioritized over absolute throughput.

---

---
---

# LABORATORY REPORT - EXPERIMENT 02

## Performance Analysis of Virtual Machines and Containers (Docker)

---

### Student & Course Metadata
- **Course Name:** Cloud Computing Laboratory
- **Experiment No:** 02
- **Student Name:** Soumya
- **USN:** 01FE24BCI121
- **Roll No:** 245
- **Environment:** Ubuntu Linux 22.04 LTS (x86_64), Docker Community Edition (CE)
- **Date of Experiment:** September 2026
- **Evaluation Status:** Evaluated and Documented

---

## 1. Aim & Objectives

### Aim
To provision and configure a standardized Linux Virtual Machine and a Docker Container environment, execute multi-subsystem stress benchmarks across CPU compute, memory bandwidth, storage I/O, and networking, quantitatively evaluate performance overheads, and analyze the architectural differences between hardware-level virtualization and operating system-level containerization.

### Key Objectives
1. **Environment Setup & Verification:** Provision an Ubuntu 22.04 LTS execution environment, configure Docker Engine, build a benchmarking container image, and verify hardware parameters using `lscpu`, `free -m`, `df -h`, and `docker info`.
2. **CPU Scalability Benchmarking:** Subject both the Virtual Machine and Docker Container to standardized prime-number calculation workloads using `sysbench cpu` across 1, 2, 4, and 8 thread allocations to measure throughput (events/sec) and latency (ms).
3. **Memory Throughput Benchmarking:** Evaluate sequential memory write bandwidth and access latency using `sysbench memory` under matched block sizes (1 MB) and total volume constraints (512 MB).
4. **Storage I/O Performance Analysis:** Benchmark direct I/O performance using `fio` across Sequential Read/Write (1 MB block size) and Random Read/Write (4 KB block size, queue depth 4) to quantify IOPS, transfer rates, and completion latency.
5. **Network Throughput & Protocol Stability:** Measure TCP bandwidth, total volume transferred, and packet retransmission rates using `iperf3` over local loopback (`127.0.0.1`) and Docker bridge networking (`docker0` / `172.17.0.1`).
6. **Application Microservice Staging:** Containerize a lightweight Python FastAPI microservice to prepare for application-level HTTP request benchmarking using `wrk` / `ab`.

---

## 2. Theoretical Background

### 2.1 Hardware-Level Virtualization (Virtual Machines)
Virtual Machines (VMs) abstract physical server hardware through a hypervisor (Virtual Machine Monitor - VMM).
- **Architecture:** Physical Hardware -> Hypervisor (Type-1 / Type-2) -> Guest OS Kernel -> User Applications.
- **Key Characteristics:**
  - Complete isolation: Each VM runs an independent operating system kernel and complete driver stack.
  - Resource Partitioning: CPU cores, RAM, and storage controllers are statically or dynamically allocated via hardware virtualization extensions (Intel VT-x / AMD-V, EPT/NPT).
  - Overhead: Additional execution layers arise from virtual device emulation (virtio / emulated SCSI), memory address translation, and guest kernel scheduling.

### 2.2 Operating System-Level Virtualization (Containers)
Containers isolate applications at the operating system level, executing as isolated user-space processes on top of the host Linux kernel.
- **Architecture:** Physical Hardware -> Host Linux Kernel (cgroups + namespaces) -> Containerized Process.
- **Core Isolation Primitives:**
  - **Linux Namespaces:** Provide process-level resource virtualization: `pid`, `net`, `mnt`, `ipc`, `uts`, `user`.
  - **Control Groups (cgroups):** Enforce strict accounting and hard limits on resource consumption (CPU time slices, memory usage, block I/O bandwidth, network priority).
- **Performance Characteristics:**
  - Bare-metal instruction execution without hypervisor trap-and-emulate penalties.
  - Direct Virtual File System (VFS) access.
  - Near-instantaneous process start times and minimal memory footprint.

---

## 3. Experimental Hardware & Virtual System Specifications

| Parameter | Virtual Machine (VM Host) | Docker Container |
| :--- | :--- | :--- |
| **Operating System** | Ubuntu 22.04 LTS (x86_64) | Ubuntu 22.04 LTS Base Image |
| **Kernel Version** | Linux `5.15.0-x-generic` | Shared Host Linux Kernel |
| **Processor Allotment** | 2 vCPU Cores | Access to 2 Host Cores (CFS scheduled) |
| **System Memory** | 2048 MB (2.0 GB) RAM | Shared Host Memory with cgroup limits |
| **Storage Subsystem** | Virtual SCSI / Ext4 File System | Overlay2 Storage Driver / Host VFS Mount |
| **Network Interface** | Virtual NIC (Local Loopback `127.0.0.1`) | Virtual Ethernet Pair (`veth`) on `docker0` (`172.17.0.1`) |

---

## 4. Benchmark Execution Procedure

1. **Baseline Profiling:** Run `sysbench cpu --threads=2 --time=30 run` to establish system equilibrium.
2. **CPU Scalability:**
   ```bash
   for t in 1 2 4 8; do
       sysbench cpu --threads=$t --cpu-max-prime=20000 --time=30 run
   done
   ```
3. **Memory Throughput:**
   ```bash
   for t in 1 2; do
       sysbench memory --threads=$t --memory-block-size=1M --memory-total-size=512M --memory-oper=write run
   done
   ```
4. **Storage I/O (FIO):**
   - Sequential Read & Write: `--rw=read / write`, `--bs=1M`, `--size=512M`, `--direct=1`
   - Random Read & Write: `--rw=randread / randwrite`, `--bs=4k`, `--size=512M`, `--iodepth=4`, `--direct=1`
5. **Network Bandwidth (iperf3):**
   - Server: `iperf3 -s`
   - Client: `iperf3 -c <target_ip> -t 30`
6. **Application Microservice Staging:**
   - Configure FastAPI service in `api/main.py`.
   - Build lightweight container image via `api/Dockerfile`.

---

## 5. Observations & Empirical Results

### 5.1 Baseline Performance (30s Execution, 2 Threads)

| Environment | Throughput (Events/sec) | Total Events | Avg Latency (ms) | 95th Percentile Latency (ms) | Max Latency Spike (ms) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Virtual Machine** | 934.44 | 28,036 | 2.14 | 3.36 | 36.89 |
| **Docker Container** | 915.55 | 27,469 | 2.18 | 3.49 | 18.72 |

---

### 5.2 CPU Scalability Matrix

| Threads | VM Throughput (EPS) | Container Throughput (EPS) | VM Avg Latency (ms) | Container Avg Latency (ms) | VM P95 Latency (ms) | Container P95 Latency (ms) | Performance Comparison |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | 515.84 | 517.19 | 1.94 | 1.93 | 2.71 | 2.76 | Container +0.26% |
| **2** | 883.55 | 894.38 | 2.26 | 2.23 | 3.82 | 3.43 | Container +1.23% |
| **4** | 928.17 | 900.45 | 4.30 | 4.43 | 7.43 | 7.56 | VM +3.08% |
| **8** | 905.17 | 914.42 | 8.82 | 8.73 | 15.55 | 15.83 | Container +1.02% |

---

### 5.3 Memory Bandwidth & Latency Matrix

| Threads | VM Bandwidth (MiB/s) | Container Bandwidth (MiB/s) | VM Operations/sec | Container Operations/sec | VM Avg Latency (ms) | Container Avg Latency (ms) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | **9,541.97** | 5,152.43 | 9,541.97 | 5,152.43 | 0.09 | 0.12 |
| **2** | **9,880.38** | 6,970.16 | 9,880.38 | 6,970.16 | 0.16 | 0.22 |

---

### 5.4 Storage I/O Performance (fio) Matrix

| I/O Pattern | Block Size | VM Bandwidth | Container Bandwidth | VM IOPS | Container IOPS | VM Avg Latency (ms) | Container Avg Latency (ms) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sequential Read** | 1 MB | 461 MiB/s | **500 MiB/s** | 461 | **500** | 2.16 | **1.99** |
| **Sequential Write** | 1 MB | **358 MiB/s** | 291 MiB/s | **358** | 291 | **2.78** | 3.42 |
| **Random Read** | 4 KB | 5,253 KiB/s | **7,072 KiB/s** | 1,313 | **1,767** | 0.75 | **0.56** |
| **Random Write** | 4 KB | 5,325 KiB/s | **5,387 KiB/s** | 1,331 | **1,346** | 0.74 | **0.73** |

---

### 5.5 Network Throughput & Quality Matrix (iperf3)

| Metric | Virtual Machine (Loopback) | Docker Container (Bridge Network) | Observation |
| :--- | :---: | :---: | :--- |
| **Sender Bitrate** | **14.1 Gbits/sec** | 13.7 Gbits/sec | Direct memory loopback |
| **Receiver Bitrate** | **14.1 Gbits/sec** | 10.3 Gbits/sec | Bridge traversal latency |
| **Data Transferred** | **49.3 GBytes** | 47.9 GBytes | Matched transfer volume |
| **TCP Retransmissions** | **3 packets** | 13 packets | Bridge network buffer contention |

---

### 5.6 Application Benchmark Staging (FastAPI Microservice)
- **Status:** Infrastructure evaluations completed. Application-level microservice stress testing (Exercise 6) using FastAPI and `wrk` load generator is fully coded, dockerized, and ready for deployment in the subsequent lab session.

---

## 6. Graphical Analysis

### Comprehensive Overall Performance Dashboard
The multi-panel analytical dashboard below summarizes the empirical comparison across CPU throughput, memory write speeds, storage bandwidth, and network bitrates:

![Overall Dashboard](vm-vs-container-performance/results/figures/overall_performance_dashboard.png)

*Figure 7: Quad-panel comparative performance evaluation between Virtual Machine and Docker Container.*

---

### Subsystem Visualizations
- **CPU Scalability:** [`vm-vs-container-performance/results/figures/cpu_scalability.png`](vm-vs-container-performance/results/figures/cpu_scalability.png) demonstrates identical execution efficiency up to 2 cores and shows predictable latency increase under over-subscription.
- **Memory Bandwidth:** [`vm-vs-container-performance/results/figures/memory_performance.png`](vm-vs-container-performance/results/figures/memory_performance.png) illustrates memory throughput and latency across thread scales.
- **Disk I/O Analysis:** [`vm-vs-container-performance/results/figures/disk_io_performance.png`](vm-vs-container-performance/results/figures/disk_io_performance.png) shows container superiority in random 4K read operations (+34.58% IOPS).
- **Network Bandwidth:** [`vm-vs-container-performance/results/figures/network_performance.png`](vm-vs-container-performance/results/figures/network_performance.png) contrasts loopback throughput against Docker virtual bridge traversal.

---

## 7. Technical Discussion & Inferences

1. **CPU Computation Parity:** Because Docker containers run as native processes directly scheduled by the Linux host kernel, CPU-bound prime-number calculations show virtually no performance degradation compared to VM/host execution.
2. **Storage I/O Architecture:** For random 4K reads, Docker demonstrated a **34.58% higher IOPS** (1,767 vs. 1,313 IOPS) and lower latency (0.56 ms vs. 0.75 ms). Virtual machines incur storage virtualization penalties due to virtual SCSI controller interrupts and virtual disk format translation.
3. **Memory Subsystem Overhead:** Memory write operations within containers exhibited reduced bandwidth compared to unconstrained VM execution. This reflects the kernel's `memory` cgroup controller overhead in maintaining per-container page accounting and dirty page tracking.
4. **Network Virtualization Cost:** Bridged container networking introduces routing overhead across virtual ethernet pairs (`veth`), Linux bridge forwarders (`docker0`), and iptables NAT packet filtering, leading to 13 TCP retransmissions compared to 3 on the VM loopback.

---

## 8. Conclusion

This experiment successfully established an empirical performance baseline comparing Virtual Machines and Docker Containers:
- **Containers are superior** for compute-intensive workloads and I/O-intensive random read applications, offering bare-metal CPU throughput, lower startup overhead, and higher random storage IOPS.
- **Virtual Machines provide stronger security isolation** through dedicated kernel instances and hardware-level virtualization, making them suitable for multi-tenant and heterogeneous operating system deployments.
- The infrastructure evaluation is complete across CPU, Memory, Disk, and Network tiers, providing the foundation for microservice load testing in subsequent laboratory exercises.

---

*Report prepared and submitted by **Soumya** (USN: `01FE24BCI121`, Roll No: `245`) for Cloud Computing Laboratory.*
