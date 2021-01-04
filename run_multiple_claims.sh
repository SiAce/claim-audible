#!/bin/bash

source venv/bin/activate

for i in {1..11}; do
    python claim_audible.py & >>& "output$i.txt"
done