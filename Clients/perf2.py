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

scan_times = []
failure_register_count = 0
success_register_count = 0
total_success_time_reg = 0.0
total_failure_time_reg = 0.0

def measure_scan_time(client, cycles):
    
    for _ in range(cycles):
        # Measure start time
        start_time = time.perf_counter()

        # Read input registers
        input_registers = client.read_holding_registers(INPUT_REGISTER_ADDRESS, NUM_REGISTERS)

        # Measure end time
        end_time = time.perf_counter()
        scan_time = end_time - start_time
        scan_times.append(scan_time)

        # Check if reading registers was successful or failed
        if input_registers is None:
            failure_register_count = failure_register_count + 1
            total_failure_time_reg = total_failure_time_reg + scan_time
            logger.error("Failed to read input registers")
        else:
            success_register_count = success_register_count + 1
            total_success_time_reg = total_success_time_reg + scan_time

    # Return all required information
    return {
        "scan_times": scan_times,
        "success_count": success_register_count,
        "failure_count": failure_register_count,
        "total_success_time": total_success_time_reg,
        "total_failure_time": total_failure_time_reg
    }

def main():
    success_count = 0
    failure_count = 0
    total_failure_time = 0.0
    total_success_time = 0.0

    client = ModbusClient(host=server_ip_address, port=server_port, auto_open=True, debug=False)

    while True:
        connection_start_time = time.time()
        if client.open():
            logger.info("Connected to PLC")
            success_count += 1
            total_success_time = total_success_time + (time.time() - connection_start_time)

            scan_times = measure_scan_time(client, CYCLES)
            client.close()

            if scan_times:
                #print(f"{sum(scan_times)} the length {len(scan_times)}")
                avg_scan_time = sum(scan_times["scan_times"]) / len(scan_times["scan_times"])
                logger.info(f"Total scan time: {sum(scan_times["scan_times"]):.6f} seconds")
                logger.info(f"Average scan time: {avg_scan_time:.6f} seconds")
                logger.info(f"Minimum scan time: {min(scan_times["scan_times"]):.6f} seconds")
                logger.info(f"Maximum scan time: {max(scan_times["scan_times"]):.6f} seconds")
            else:
                logger.warning("No successful scans were completed")

        else:
            failure_count += 1
            total_failure_time = total_failure_time + (time.time() - connection_start_time)
            logger.error("Failed to connect to PLC")
        
        total_time = total_failure_time + total_success_time
        print("----------------------------------------------------------------------------")
        print("----------------------------------------------------------------------------")

        logger.info(f"Total connection successes: {success_count:}")
        logger.info(f"Total connection failures: {failure_count:}")
        logger.info(f"Total read register failures: {scan_times["failure_count"]:}")
        logger.info(f"Total read register success: {scan_times["success_count"]:}")
        logger.info(f"Total failure read holding registers time: {scan_times["failure_count"]:.6f} seconds")
        logger.info(f"Total success read holding registers time: {scan_times["success_count"]:.6f} seconds")
        logger.info(f"Total success connection time: {total_success_time:.6f} seconds")
        logger.info(f"Total failure connection time: {total_failure_time:.6f} seconds")
        logger.info(f"Total run time: {total_time:.6f} seconds")

        time.sleep(1)

if __name__ == "__main__":
    main()