#!/usr/bin/env python3
"""
Sysbench Output Parser & Hypervisor Performance Comparator
Calculates exact deltas, speedup ratios, and latency differences
between Proxmox VE (Type-1 Bare-Metal) and VMware Workstation (Type-2 Hosted).
"""

def compare_hypervisors():
    proxmox = {
        "hypervisor": "Proxmox VE (Type-1 Bare-Metal)",
        "vm_host": "vm01@vm01-Standard-PC-i440FX-PIIX-1996",
        "eps": 1587.47,
        "total_time": 10.0005,
        "total_events": 15877,
        "min_lat": 0.59,
        "avg_lat": 0.63,
        "max_lat": 1.34,
        "p95_lat": 0.65,
    }

    vmware = {
        "hypervisor": "VMware Workstation (Type-2 Hosted)",
        "vm_host": "soumya@soumya-virtual-machine",
        "eps": 636.80,
        "total_time": 10.0016,
        "total_events": 6370,
        "min_lat": 1.31,
        "avg_lat": 1.57,
        "max_lat": 6.84,
        "p95_lat": 2.07,
    }

    eps_diff = ((proxmox["eps"] - vmware["eps"]) / vmware["eps"]) * 100
    speedup = proxmox["eps"] / vmware["eps"]
    events_diff = proxmox["total_events"] - vmware["total_events"]
    avg_lat_diff = ((vmware["avg_lat"] - proxmox["avg_lat"]) / vmware["avg_lat"]) * 100
    p95_lat_diff = ((vmware["p95_lat"] - proxmox["p95_lat"]) / vmware["p95_lat"]) * 100
    max_lat_diff = ((vmware["max_lat"] - proxmox["max_lat"]) / vmware["max_lat"]) * 100

    print("=" * 88)
    print("       HYPERVISOR CPU PERFORMANCE COMPARISON: TYPE-1 VS TYPE-2")
    print("=" * 88)
    print(f"{'Metric':<30} {'Proxmox VE (Type-1)':<22} {'VMware (Type-2)':<20} {'Advantage / Delta'}")
    print("-" * 88)
    print(f"{'VM Identifier':<30} {proxmox['vm_host'][:20]:<22} {vmware['vm_host'][:18]:<20} Matched baseline")
    print(f"{'Throughput (Events/sec)':<30} {proxmox['eps']:<22.2f} {vmware['eps']:<20.2f} +{eps_diff:.2f}% ({speedup:.2f}x faster)")
    print(f"{'Total Events (10s)':<30} {proxmox['total_events']:<22} {vmware['total_events']:<20} +{events_diff:,} events (+{eps_diff:.2f}%)")
    print(f"{'Minimum Latency (ms)':<30} {proxmox['min_lat']:<22.2f} {vmware['min_lat']:<20.2f} Proxmox {vmware['min_lat']-proxmox['min_lat']:.2f}ms lower")
    print(f"{'Average Latency (ms)':<30} {proxmox['avg_lat']:<22.2f} {vmware['avg_lat']:<20.2f} Proxmox -{avg_lat_diff:.2f}% lower")
    print(f"{'95th Percentile Latency (ms)':<30} {proxmox['p95_lat']:<22.2f} {vmware['p95_lat']:<20.2f} Proxmox -{p95_lat_diff:.2f}% lower")
    print(f"{'Maximum Latency (ms)':<30} {proxmox['max_lat']:<22.2f} {vmware['max_lat']:<20.2f} Proxmox -{max_lat_diff:.2f}% lower")
    print("=" * 88)
    print(f"Summary: Type-1 (Proxmox VE) demonstrated a {speedup:.2f}x throughput speedup over Type-2")
    print(f"(VMware Workstation) with {avg_lat_diff:.2f}% lower average latency and substantially tighter")
    print(f"latency distribution under identical CPU prime calculation stress.")
    print("=" * 88)

if __name__ == "__main__":
    compare_hypervisors()
