#!/bin/bash
awk '{sum += $1; count++} END {printf "Total: %.2f GB\nAverage: %.2f MB\nCount: %d\n", sum/1e9, sum/count/1e6, count}' masterfilelist.txt