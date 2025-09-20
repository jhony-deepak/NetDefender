from scapy.all import *
import time

target = "104.18.32.47"  # cloudflare.com IP, just for test
ports = range(20, 41)

print(f"🚨 Simulating scan to {target}")

for port in ports:
    pkt = IP(dst=target)/TCP(dport=port, flags="S")
    send(pkt, verbose=False)
    print(f"Sent SYN to port {port}")
    time.sleep(0.05)

print("✅ Test scan done.")