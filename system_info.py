import socket
import platform
import os
import time


# Hostname
def get_hostname():
	return socket.gethostname()

# Operating System
def get_operating_system():
	return platform.system()

# Kernel Version
def get_kernel_version():
	return platform.release()

# Processor Search
def get_processor():
	with open("/proc/cpuinfo", "r") as cpu_info:
		for line in cpu_info:
			if line.startswith("model name"):
				processor = line.split(":", 1)[1].strip()
				break
		else:
			processor = "Unknown"

	return processor

# Memory Calculations
def get_memory():
	memory_total = 0
	memory_available = 0

	with open("/proc/meminfo", "r") as memory_info:
		for line in memory_info:
			if line.startswith("MemTotal:"):
				memory_total = int(line.split()[1])
			elif line.startswith("MemAvailable:"):
				memory_available = int(line.split()[1])

	memory_total_gib = memory_total / 1024 / 1024
	memory_available_gib = memory_available / 1024 / 1024

	memory_used = memory_total - memory_available
	memory_used_gib = memory_used / 1024 / 1024

	memory_usage_percent = (memory_used / memory_total) * 100

	return(memory_total_gib, memory_available_gib, memory_used_gib, memory_usage_percent)

# CPU Count
def get_cpu_count():
	return os.cpu_count()

# CPU Usage Calculations
def get_cpu_times():
	with open("/proc/stat", "r") as cpu_info:
		first_line = cpu_info.readline()
	values = first_line.split()[1:]
	return [int(value) for value in values]

def get_cpu_usage():
	cpu_start = get_cpu_times()
	time.sleep(1)
	cpu_end = get_cpu_times()
	cpu_differences = []

	for start, end in zip(cpu_start, cpu_end):
		cpu_differences.append(end - start)

	total_cpu_time = sum(cpu_differences)
	idle_time = cpu_differences[3]

	busy_cpu_time = total_cpu_time - idle_time

	cpu_usage_percent = (busy_cpu_time / total_cpu_time) * 100

	return cpu_usage_percent

# System Info
def get_system_info():
	memory_total, memory_available, memory_used, memory_usage = get_memory()

	return {
		"hostname": get_hostname(),
		"operating_system": get_operating_system(),
		"kernel_version": get_kernel_version(),
		"processor": get_processor(),
		"cpu_count": get_cpu_count(),
		"memory_total": memory_total,
		"memory_available": memory_available,
		"memory_used": memory_used,
		"memory_usage": memory_usage,
		"cpu_usage": get_cpu_usage()
	}

# Process IDs
def get_process_ids():
	process_ids = []

	for entry in os.listdir("/proc"):
		if entry.isdigit():
			process_ids.append(int(entry))
	return process_ids

# Process Statuses
def get_process_status(pid):
	status = {}
	with open(f"/proc/{pid}/status", "r") as  process_info:
		for line in process_info:
			key, value = line.split(":", 1)
			status[key] = value.strip()
	return status

# Processes
def get_processes():
	processes = []
	process_ids = get_process_ids()

	for pid in process_ids:
		try:
			process = get_process_status(pid)
			processes.append({
				"pid": pid,
				"name": process["Name"],
				"parent_pid": process["PPid"],
				"uid": process["Uid"],
				"state": process["State"],
				"memory": process.get("VmRSS"),
				"kernel_thread": process["Kthread"]
	})
		except FileNotFoundError:
			continue
	return processes
