#!/bin/bash

# Run all 5 mock Flask sites in the background
echo "Starting all mock sites..."

python3 site1.py &
echo "site1 running on port 5001"
python3 site2.py &
echo "site2 running on port 5002"
python3 site3.py &
echo "site3 running on port 5003"
python3 site4.py &
echo "site4 running on port 5004"
python3 site5.py &
echo "site5 running on port 5005"

wait
