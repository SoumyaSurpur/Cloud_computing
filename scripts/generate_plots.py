import os
import matplotlib.pyplot as plt
import numpy as np

# Ensure images directory exists
os.makedirs('images', exist_ok=True)

# Visual styling
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig_dpi = 300

# Color palette: Proxmox Blue & VMware Amber-Orange
c_proxmox = '#1a56db'  # Rich enterprise blue
c_vmware = '#e05638'   # Crimson-orange
colors = [c_proxmox, c_vmware]

hypervisors = ['Proxmox VE\n(Type-1 Bare-Metal)', 'VMware Workstation\n(Type-2 Hosted)']

# Empirical benchmark data
eps_values = [1587.47, 636.80]
events_values = [15877, 6370]
proxmox_lat = [0.59, 0.63, 0.65, 1.34]  # min, avg, p95, max
vmware_lat = [1.31, 1.57, 2.07, 6.84]   # min, avg, p95, max
latency_labels = ['Min Latency', 'Avg Latency', '95th Percentile', 'Max Latency']

# -------------------------------------------------------------------------
# Plot 1: Events Per Second (Throughput)
# -------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 6), dpi=fig_dpi)
bars = ax.bar(hypervisors, eps_values, color=colors, width=0.45, edgecolor='#2c3e50', linewidth=1.2)

ax.set_ylabel('Events per Second (Throughput / EPS)', fontsize=12, fontweight='bold', color='#1e293b')
ax.set_title('CPU Throughput Comparison (Sysbench 20k Primes)\nProxmox VE vs VMware Workstation', 
             fontsize=13, fontweight='bold', pad=15, color='#0f172a')
ax.set_ylim(0, 2000)
ax.grid(axis='y', linestyle='--', alpha=0.6)

for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{height:,.2f} EPS',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 6),
                textcoords="offset points",
                ha='center', va='bottom', fontsize=11, fontweight='bold', color='#0f172a')

# Speedup annotation
pct_diff = ((eps_values[0] - eps_values[1]) / eps_values[1]) * 100
ax.text(0.5, 0.84, f'Proxmox VE (Type-1) delivers\n+{pct_diff:.2f}% Higher Throughput\n({eps_values[0]/eps_values[1]:.2f}x Speedup)', 
        transform=ax.transAxes, fontsize=11, fontweight='bold', ha='center',
        bbox=dict(boxstyle="round,pad=0.6", facecolor='#eff6ff', edgecolor='#1d4ed8', alpha=0.95))

plt.tight_layout()
plt.savefig('images/events_per_second_comparison.png')
plt.close()

# -------------------------------------------------------------------------
# Plot 2: Latency Breakdown Comparison
# -------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6), dpi=fig_dpi)
x = np.arange(len(latency_labels))
width = 0.35

rects1 = ax.bar(x - width/2, proxmox_lat, width, label='Proxmox VE (Type-1 Bare-Metal)', 
                color=c_proxmox, edgecolor='#1e293b', linewidth=1.1)
rects2 = ax.bar(x + width/2, vmware_lat, width, label='VMware Workstation (Type-2 Hosted)', 
                color=c_vmware, edgecolor='#1e293b', linewidth=1.1)

ax.set_ylabel('Latency (milliseconds - ms)', fontsize=12, fontweight='bold', color='#1e293b')
ax.set_title('Sysbench CPU Latency Metrics Comparison (Lower is Better)', 
             fontsize=13, fontweight='bold', pad=15, color='#0f172a')
ax.set_xticks(x)
ax.set_xticklabels(latency_labels, fontsize=11, fontweight='bold', color='#1e293b')
ax.legend(fontsize=11, loc='upper left', frameon=True, facecolor='#ffffff', edgecolor='#cbd5e1')
ax.set_ylim(0, 8.0)
ax.grid(axis='y', linestyle='--', alpha=0.6)

for rect in rects1:
    h = rect.get_height()
    ax.annotate(f'{h:.2f} ms', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 4),
                textcoords="offset points", ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#1e3a8a')

for rect in rects2:
    h = rect.get_height()
    ax.annotate(f'{h:.2f} ms', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 4),
                textcoords="offset points", ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#991b1b')

plt.tight_layout()
plt.savefig('images/latency_comparison.png')
plt.close()

# -------------------------------------------------------------------------
# Plot 3: Total Events Processed
# -------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 6), dpi=fig_dpi)
bars = ax.bar(hypervisors, events_values, color=colors, width=0.45, edgecolor='#2c3e50', linewidth=1.2)

ax.set_ylabel('Total Events Completed (10-second window)', fontsize=12, fontweight='bold', color='#1e293b')
ax.set_title('Total Computational Events Processed\nSysbench CPU Prime Calculation (20,000 Primes)', 
             fontsize=13, fontweight='bold', pad=15, color='#0f172a')
ax.set_ylim(0, 20000)
ax.grid(axis='y', linestyle='--', alpha=0.6)

for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{height:,} events',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 6),
                textcoords="offset points",
                ha='center', va='bottom', fontsize=11, fontweight='bold', color='#0f172a')

delta_events = events_values[0] - events_values[1]
ax.text(0.5, 0.84, f'Proxmox VE processed\n+{delta_events:,} more events\n(+{pct_diff:.2f}% higher compute efficiency)', 
        transform=ax.transAxes, fontsize=11, fontweight='bold', ha='center',
        bbox=dict(boxstyle="round,pad=0.6", facecolor='#eff6ff', edgecolor='#1d4ed8', alpha=0.95))

plt.tight_layout()
plt.savefig('images/total_events_comparison.png')
plt.close()

# -------------------------------------------------------------------------
# Plot 4: Comprehensive Performance Dashboard
# -------------------------------------------------------------------------
fig, axs = plt.subplots(2, 2, figsize=(14, 10), dpi=fig_dpi)
fig.suptitle('Comparative Hypervisor Performance Dashboard\nProxmox VE (Type-1 Bare-Metal) vs VMware Workstation (Type-2 Hosted)', 
             fontsize=15, fontweight='bold', y=0.98, color='#0f172a')

# Subplot 1: Throughput (EPS)
axs[0, 0].bar(hypervisors, eps_values, color=colors, width=0.42, edgecolor='#1e293b', linewidth=1.1)
axs[0, 0].set_title('Events per Second / Throughput (Higher is Better)', fontsize=11.5, fontweight='bold', color='#0f172a')
axs[0, 0].set_ylabel('Events / sec', fontsize=10, fontweight='bold')
axs[0, 0].set_ylim(0, 1950)
axs[0, 0].grid(axis='y', linestyle='--', alpha=0.5)
for bar in axs[0, 0].patches:
    axs[0, 0].annotate(f'{bar.get_height():,.2f}', (bar.get_x() + bar.get_width()/2, bar.get_height()),
                       xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontweight='bold')

# Subplot 2: Total Events in 10s
axs[0, 1].bar(hypervisors, events_values, color=colors, width=0.42, edgecolor='#1e293b', linewidth=1.1)
axs[0, 1].set_title('Total Events in ~10s (Higher is Better)', fontsize=11.5, fontweight='bold', color='#0f172a')
axs[0, 1].set_ylabel('Total Events', fontsize=10, fontweight='bold')
axs[0, 1].set_ylim(0, 19500)
axs[0, 1].grid(axis='y', linestyle='--', alpha=0.5)
for bar in axs[0, 1].patches:
    axs[0, 1].annotate(f'{int(bar.get_height()):,}', (bar.get_x() + bar.get_width()/2, bar.get_height()),
                       xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontweight='bold')

# Subplot 3: Average Latency
avg_lats = [0.63, 1.57]
axs[1, 0].bar(hypervisors, avg_lats, color=colors, width=0.42, edgecolor='#1e293b', linewidth=1.1)
axs[1, 0].set_title('Average Latency (Lower is Better)', fontsize=11.5, fontweight='bold', color='#0f172a')
axs[1, 0].set_ylabel('Latency (ms)', fontsize=10, fontweight='bold')
axs[1, 0].set_ylim(0, 2.0)
axs[1, 0].grid(axis='y', linestyle='--', alpha=0.5)
for bar in axs[1, 0].patches:
    axs[1, 0].annotate(f'{bar.get_height():.2f} ms', (bar.get_x() + bar.get_width()/2, bar.get_height()),
                       xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontweight='bold')

# Subplot 4: 95th Percentile Latency
p95_lats = [0.65, 2.07]
axs[1, 1].bar(hypervisors, p95_lats, color=colors, width=0.42, edgecolor='#1e293b', linewidth=1.1)
axs[1, 1].set_title('95th Percentile Latency (Lower is Better)', fontsize=11.5, fontweight='bold', color='#0f172a')
axs[1, 1].set_ylabel('Latency (ms)', fontsize=10, fontweight='bold')
axs[1, 1].set_ylim(0, 2.6)
axs[1, 1].grid(axis='y', linestyle='--', alpha=0.5)
for bar in axs[1, 1].patches:
    axs[1, 1].annotate(f'{bar.get_height():.2f} ms', (bar.get_x() + bar.get_width()/2, bar.get_height()),
                       xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontweight='bold')

plt.tight_layout(rect=[0, 0, 1, 0.94])
plt.savefig('images/overall_performance_dashboard.png')
plt.close()

print('All 4 publication-quality plots generated successfully in images/ folder.')
