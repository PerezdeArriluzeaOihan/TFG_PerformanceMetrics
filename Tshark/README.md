1. tshark -D ----> List Interfaces
2. timeout 3600 tshark -i 2 -f "capture_filter" -w file.pcap
    - timeout t --> command/capture lasts t seconds
    - tshark -i D --> Captures D interface (name or list number)
    - -f is used to filter the capture:
        - "tcp and src host 192.168.192.3"
        - "tcp and not ip.addr == 192.168.192.1"
        - "udp and ip.dst == 192.168.192.2 and port 80"
    - -w file.pcap --> Writes the capture in file.pcap file
3. tshark -i 2 -c packet_count
    - capture will stop after n packets
4. tshark -r cap.pcap -Y "display_filter"
    - -Y falg is a display filter:
        - "ip.src == 192.168.192.5 and ip.dst == 192.168.192.3 and tcp and frame.number>=1320 and frame.number<1330"
5. gzip file.pcap
    - to compress an existing file
6. timeout 3600 tshark -i 22 -w - | gzip > file.pcap.gz