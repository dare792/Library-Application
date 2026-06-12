import multiprocessing
import time

def burn_resources(items_count):
    """Allocates a large dictionary in RAM, then pins the CPU core."""
    pid = multiprocessing.current_process().name
    print(f"[{pid}] Allocating memory...")
    
    # Each process builds its own high-memory dictionary
    # 1,000,000 items with 500-character strings takes a few hundred MBs per core
    mega_dict = {i: "X" * 500 for i in range(items_count)}
    
    print(f"[{pid}] Memory allocated. Now pinning CPU core...")
    
    # Infinite loop keeping the dictionary in memory and maxing out the CPU
    while True:
        _ = 9999 * 9999

if __name__ == "__main__":
    num_cores = multiprocessing.cpu_count()
    
    # Tweak this number to control how much RAM is used.
    # Total items across your system = ITEMS_PER_CORE * num_cores
    ITEMS_PER_CORE = 90000000 
    
    print("🔥 WARNING: Launching full system stress test (CPU + RAM) 🔥")
    print(f"Spawning {num_cores} processes...")
    print("Press Ctrl + C in this terminal to stop the test.")
    
    processes = []
    for _ in range(num_cores):
        p = multiprocessing.Process(target=burn_resources, args=(ITEMS_PER_CORE,))
        p.start()
        processes.append(p)
        
    try:
        # Keep the main script alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping the test and freeing up all resources...")
        # Terminating the processes instantly destroys the dictionaries, freeing the RAM
        for p in processes:
            p.terminate()
            p.join()
        print("System resources restored to normal!")