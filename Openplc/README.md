1. http://localhost:8080/
2. Username/Password - openplc/openplc
3. Go to settings and make sure the following are enabled:
	- Enable Modbus Server - Port 502
	- Enable DNP Server - Port 20000
	- Enable EtherNet/IP Server Port 44818
	- Saves Changes
4. Go to Hardware
	- Select Simulink with DNP3 (Linux Only)
5. Go to Programs
	- Upload and compile the program.
	- Launch the program
	- The program will compile again.
6. Start the OpenPLC.
7. Go to Monitoring