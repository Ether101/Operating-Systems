# OS Project: Process Scheduling and Memory Management Simulation in Python
# ===============================================================

# Libraries Used
import time
from collections import deque

# Process Representation
class Process:
    def __init__(self, pid, arrival_time, burst_time, memory_required):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.memory_required = memory_required
        self.start_time = None
        self.completion_time = None

# Memory Management
class MemoryManager:
    def __init__(self, total_memory):
        self.total_memory = total_memory
        self.memory = [None] * total_memory

    def allocate_memory(self, process):
        for i in range(self.total_memory - process.memory_required + 1):
            if all(self.memory[j] is None for j in range(i, i + process.memory_required)):
                for j in range(i, i + process.memory_required):
                    self.memory[j] = process.pid
                return True
        return False

    def deallocate_memory(self, pid):
        self.memory = [None if x == pid else x for x in self.memory]

    def get_utilization(self):
        used = sum(1 for x in self.memory if x is not None)
        return (used / self.total_memory) * 100

# Round Robin Scheduler
class Scheduler:
    def __init__(self, time_quantum):
        self.time_quantum = time_quantum
        self.ready_queue = deque()
        self.time = 0
        self.completed_processes = []
        self.waiting_times = {}
        self.turnaround_times = {}

    def run(self, processes, memory_manager):
        process_list = sorted(processes, key=lambda p: p.arrival_time)

        while process_list or self.ready_queue:
            # Load newly arrived processes
            for process in list(process_list):
                if process.arrival_time <= self.time:
                    if memory_manager.allocate_memory(process):
                        self.ready_queue.append(process)
                        process_list.remove(process)

            if self.ready_queue:
                current = self.ready_queue.popleft()

                if current.start_time is None:
                    current.start_time = self.time

                execute_time = min(current.remaining_time, self.time_quantum)
                self.time += execute_time
                current.remaining_time -= execute_time

                if current.remaining_time == 0:
                    current.completion_time = self.time
                    memory_manager.deallocate_memory(current.pid)
                    self.completed_processes.append(current)
                    self.turnaround_times[current.pid] = current.completion_time - current.arrival_time
                    self.waiting_times[current.pid] = self.turnaround_times[current.pid] - current.burst_time
                else:
                    self.ready_queue.append(current)
            else:
                self.time += 1

        avg_waiting = sum(self.waiting_times.values()) / len(self.waiting_times)
        avg_turnaround = sum(self.turnaround_times.values()) / len(self.turnaround_times)
        mem_util = memory_manager.get_utilization()

        return self.completed_processes, avg_waiting, avg_turnaround, mem_util

# Command-line Interface

def main():
    print("\n--- Operating Systems Project ---")
    print("Simulating Round Robin Scheduling with First-Fit Memory Allocation\n")

    num_processes = int(input("Enter total number of processes: "))
    processes = []

    for i in range(num_processes):
        pid = i + 1
        arrival_time = int(input(f"Enter arrival time for Process {pid}: "))
        burst_time = int(input(f"Enter burst time for Process {pid}: "))
        memory = int(input(f"Enter memory required by Process {pid}: "))
        processes.append(Process(pid, arrival_time, burst_time, memory))

    memory_size = int(input("Enter total memory size: "))
    time_quantum = int(input("Enter time quantum for Round Robin: "))

    memory_manager = MemoryManager(memory_size)
    scheduler = Scheduler(time_quantum)

    completed, avg_wait, avg_turnaround, mem_util = scheduler.run(processes, memory_manager)

    print("\nExecution Results:")
    for p in completed:
        print(f"Process {p.pid}: Start Time = {p.start_time}, Completion Time = {p.completion_time}, Burst = {p.burst_time}, Memory = {p.memory_required}")

    print(f"\nAverage Waiting Time: {avg_wait:.2f} units")
    print(f"Average Turnaround Time: {avg_turnaround:.2f} units")
    print(f"Final Memory Utilization: {mem_util:.2f}%")

if __name__ == '__main__':
    main()
