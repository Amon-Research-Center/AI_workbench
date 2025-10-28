#!/bin/bash
destination_ip="54.90.190.193"

# Set initial packet size
packet_size=1500

# Loop to find the maximum MTU size
while true; do
  ping -M do -c 1 -s $packet_size $destination_ip &> /dev/null
  if [ $? -ne 0 ]; then
    echo "Maximum MTU size: $((packet_size -28))"
    break
  fi
packet_size=$((packet_size + 10))
done
