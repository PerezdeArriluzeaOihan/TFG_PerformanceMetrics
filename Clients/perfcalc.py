#!/usr/bin/env python

from pyModbusTCP.client import ModbusClient
import time
import logging
import socket
import random
from collections import Counter
from threading import Thread as Worker
from threading import Lock

_thread_lock = Lock()

try:
    from multiprocessing import log_to_stderr
except ImportError:
    import logging
    logging.basicConfig()
    log_to_stderr = logging.getLogger

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("pymodbus")

# Configuration
host = '10.63.28.65'  # Replace with your PLC host
server_ip_address = socket.gethostbyname(host)
server_port = 502
workers = 1 

UNIT = 0x1
CYCLES = 20  # Number of cycles to measure
INPUT_REGISTER_ADDRESS = 201  # Example input register address
OUTPUT_REGISTER_ADDRESS = 206  # Example output register address
NUM_REGISTERS = 3  # Number of registers to read/write

client = ModbusClient(host=server_ip_address, port=server_port, auto_open=True, debug=False)

def client_execute():
    """Performs a single threaded test of a synchronous client against the specified host

    :param host: The host to connect to
    :param cycles: The number of iterations to perform
    """
    with _thread_lock:
        # Read input registers
        input_registers = client.read_holding_registers(INPUT_REGISTER_ADDRESS, NUM_REGISTERS)
        if input_registers is None:
            logger.error("Failed to read input registers")
        

            # Simulate processing (execution) - Here we just manipulate the data read
        #processed_data = [value + random.randint(1, 10) for value in input_registers]

            # Write output registers
        #if not client.write_multiple_registers(OUTPUT_REGISTER_ADDRESS, processed_data):
        #    logger.error("Failed to write output registers")
            


def measure_scan_time(client, cycles):
    scan_times = []

    for _ in range(cycles):
        # Measure start time
       
        procs = [Worker(target=client_execute) for _ in range(workers)]
        start_time = time.perf_counter()
        for p in procs:
            p.start()  # Start the workers
            continue
        for p in procs:
            p.join()  # Wait for the workers to finish
            continue

        # Measure end time
        end_time = time.perf_counter()

        # Calculate scan time
        scan_time = end_time - start_time
        scan_times.append(scan_time)
        #logger.debug(f"Cycle completed in {scan_time:.6f} seconds")

    return scan_times

def main():
   

    if client.open():
        logger.info("Connected to PLC")
        
        scan_times = measure_scan_time(client, CYCLES)

        if scan_times:
            print(f"{sum(scan_times)} the length {len(scan_times)}")
            avg_scan_time = sum(scan_times) / len(scan_times)
            logger.info(f"Average scan time: {avg_scan_time:.6f} seconds")
            logger.info(f"Minimum scan time: {min(scan_times):.6f} seconds")
            logger.info(f"Maximum scan time: {max(scan_times):.6f} seconds")
            counter = Counter(scan_times)
            most_common = counter.most_common(1)[0] 
            logger.info (f"Scan time {most_common[1]} (Most Frequent): {most_common[0]:.6f} seconds")
        else:
            logger.warning("No successful scans were completed")
    else:
        logger.error("Failed to connect to PLC")

if __name__ == "__main__":
    while True:
      main()
      client.close()
      time.sleep(1)
      