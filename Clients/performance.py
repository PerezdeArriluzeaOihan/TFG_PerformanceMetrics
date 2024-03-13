#!/usr/bin/env python
"""
Pymodbus Performance Example
--------------------------------------------------------------------------

The following is an quick performance check of the synchronous
modbus client.
"""
# --------------------------------------------------------------------------- # 
# import the necessary modules
# --------------------------------------------------------------------------- #
from __future__ import print_function
import logging, os, socket
from time import time
from pymodbus.client import ModbusTcpClient
import time
import random
# from pymodbus.client.sync import ModbusSerialClient

try:
    from multiprocessing import log_to_stderr
except ImportError:
    import logging
    logging.basicConfig()
    log_to_stderr = logging.getLogger

# --------------------------------------------------------------------------- # 
# choose between threads or processes
# --------------------------------------------------------------------------- # 

#from multiprocessing import Process as Worker
from threading import Thread as Worker
from threading import Lock
_thread_lock = Lock()
# --------------------------------------------------------------------------- # 
# initialize the test
# --------------------------------------------------------------------------- # 
# Modify the parameters below to control how we are testing the client:
#
# * workers - the number of workers to use at once
# * cycles  - the total number of requests to send
# * host    - the host to send the requests to
# --------------------------------------------------------------------------- # 
workers = 1     # El número de hilos
cycles = 1000
host = 'openplc' # ESTO ES SOLO PARA DOCKER COMPOSE, SI NO ES localhost
server_ip_address=socket.gethostbyname(host)
server_port=502
UNIT= 0x1

maxtime=0.0
mintime=0.0
avgtime=0.0

# --------------------------------------------------------------------------- # 
# perform the test
# --------------------------------------------------------------------------- # 
# This test is written such that it can be used by many threads of processes
# although it should be noted that there are performance penalties
# associated with each strategy.
# --------------------------------------------------------------------------- # 
def single_client_test(host, cycles):
    """ Performs a single threaded test of a synchronous
    client against the specified host

    :param host: The host to connect to
    :param cycles: The number of iterations to perform
    """
    #logger = log_to_stderr()
    #logger.setLevel(logging.DEBUG)
    #logger.debug("starting worker: %d" % os.getpid())
    try:
        count = 0
        client = ModbusTcpClient(host, server_port)
        client.connect()
        #client = ModbusSerialClient(method="rtu",
        #port="/dev/ttyp0", baudrate=9600)
        while count < cycles:
            RandomQri=random.randint(15000,65535)
            RandomQw=random.randint(600,1200)
            RandomKla=random.randint(50,175)
            with _thread_lock:
                # client.write_registers(0,[25000,106,100]) #Cambia las direcciones 0,1,2 a los valores iniciales
                client.write_register(0,RandomQri) #Cambia el valor de la dirección de memoria 0 (Qri)
                client.write_register(1,RandomQw) #Cambia el valor de la dirección de memoria 1 (Qw)
                client.write_register(2,RandomKla) #Cambia el valor de la dirección de memoria 2 (Kla)
                # client.write_register(0,count) #Cambia el valor de la dirección de memoria 0 (Qri)
                # client.write_register(1,count) #Cambia el valor de la dirección de memoria 1 (Qw)
                # client.write_register(2,count) #Cambia el valor de la dirección de memoria 2 (Kla)
                rr = client.read_holding_registers(0, 3, unit=1)
                # print("Reading Holding Registers %s" % (rr.registers))
                count += 1
        client.close()
    except:
        logger.exception("failed to run test successfully")
    #logger.debug("finished worker: %d" % os.getpid())

# --------------------------------------------------------------------------- # 
# run our test and check results
# --------------------------------------------------------------------------- # 
# We shard the total number of requests to perform between the number of
# threads that was specified. We then start all the threads and block on
# them to finish. This may need to switch to another mechanism to signal
# finished as the process/thread start up/shut down may skew the test a bit.

# RTU 32 requests/second @9600
# TCP 31430 requests/second

# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    args = (host, int(cycles * 1.0 / workers))
    logger = log_to_stderr()
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    n=0
    totaltime=0
    while True:
        time.sleep(1)
        procs = [Worker(target=single_client_test, args=args)
                for _ in range(workers)]
        tic= time.perf_counter()
        any(p.start() for p in procs)   # start the workers
        any(p.join() for p in procs)   # wait for the workers to finish
        toc= time.perf_counter()
        logger.debug("%d requests/second" % ((1.0 * cycles) / (toc - tic)))
        logger.debug("time taken to complete %s cycle by "
            "%s workers is %s seconds" % (cycles, workers, toc-tic))
        n += 1
        if n>6:
            totaltime=totaltime+(toc-tic)
            maxtime=max(maxtime,toc-tic)
            mintime=min(mintime,toc-tic)
            avgtime=(totaltime/(n-6))
            logger.debug("Maximun time taken by %d cycles is %s seconds" % (cycles, maxtime))
            logger.debug("Minimun time taken by %d cycles is %s seconds" % (cycles, mintime))
            logger.debug("Average time of all %d cycles is %s seconds" % (cycles, avgtime))