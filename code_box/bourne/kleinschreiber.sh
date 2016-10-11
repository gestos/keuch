#!/bin/bash



max_depth=$(find | sed s:[^/]::g | sort -u | tail -n1 | wc -c)
echo "$max_depth"
