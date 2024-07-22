import multiprocessing
import time, random

class MyParallelClass:
    def my_function(self, name, queue):
        for i in range(5):
            queue.put(f"Process {name}: {i}")
            time.sleep(random.randint(10, 1001)/1000)

def start_processes(processes, obj, queue, count):
    for _ in range(3 - len(processes)):  # Start up to three processes
        process = multiprocessing.Process(target=obj.my_function, args=(f"Process-{count}", queue))
        process.daemon = True  # Set the process as daemon
        process.start()
        processes.append((process, count))
        count += 1
    return count

if __name__ == "__main__":
    # Create an instance of the class
    obj = MyParallelClass()

    # Create a queue for shared stdout
    queue = multiprocessing.Queue()

    # List to hold the processes and a counter for naming
    processes = []
    count = 1

    # Start initial processes
    count = start_processes(processes, obj, queue, count)

    # Continuously monitor and restart processes
    while True:
        # Read from the queue and print to stdout
        try:
            while not queue.empty():
                message = queue.get_nowait()
                print(message)
        except multiprocessing.queues.Empty:
            pass

        # Check and restart any finished processes
        for process, proc_id in processes[:]:
            if not process.is_alive():
                process.join()  # Ensure the process has fully terminated
                processes.remove((process, proc_id))
                count = start_processes(processes, obj, queue, count)
        
        time.sleep(0.1)  # Short delay to prevent high CPU usage