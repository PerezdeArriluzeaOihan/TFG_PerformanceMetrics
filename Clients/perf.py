#!/usr/bin/env python

from pyModbusTCP.client import ModbusClient
import time
import logging
import socket
import random


# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("pymodbus")

# Configuration
host = 'openplc'  # Replace with your PLC host
server_ip_address = socket.gethostbyname(host)
server_port = 502
UNIT = 0x1
CYCLES = 1000  # Number of cycles to measure
INPUT_REGISTER_ADDRESS = 1  # Example input register address
OUTPUT_REGISTER_ADDRESS = 2  # Example output register address
NUM_REGISTERS = 3  # Number of registers to read/write

def measure_scan_time(client, cycles):
    scan_times = []

    for _ in range(cycles):
        # Measure start time
        start_time = time.perf_counter()

        # Read input registers
        input_registers = client.read_holding_registers(INPUT_REGISTER_ADDRESS, NUM_REGISTERS)
        if input_registers is None:
            logger.error("Failed to read input registers")
            continue

        # Simulate processing (execution) - Here we just manipulate the data read
        #processed_data = [value + random.randint(1, 10) for value in input_registers]

        # Write output registers
        #if not client.write_multiple_registers(OUTPUT_REGISTER_ADDRESS, processed_data):
        #    logger.error("Failed to write output registers")
         #   continue

        # Measure end time
        end_time = time.perf_counter()

        # Calculate scan time
        scan_time = end_time - start_time
        scan_times.append(scan_time)
        #logger.debug(f"Cycle completed in {scan_time:.6f} seconds")

    return scan_times

def main():
    client = ModbusClient(host=server_ip_address, port=server_port, auto_open=True, debug=False)
    if client.open():
        logger.info("Connected to PLC")
        
        scan_times = measure_scan_time(client, CYCLES)

        if scan_times:
            #print(f"{sum(scan_times)} the length {len(scan_times)}")
            avg_scan_time = sum(scan_times) / len(scan_times)
            logger.info(f"Total scan time: {sum(scan_times):.6f} seconds")
            logger.info(f"Average scan time: {avg_scan_time:.6f} seconds")
            logger.info(f"Minimum scan time: {min(scan_times):.6f} seconds")
            logger.info(f"Maximum scan time: {max(scan_times):.6f} seconds")
        else:
            logger.warning("No successful scans were completed")

        client.close()
    else:
        logger.error("Failed to connect to PLC")

if __name__ == "__main__":
    while True:
      main()
      time.sleep(1)
