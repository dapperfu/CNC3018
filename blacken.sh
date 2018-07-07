#!/usr/bin/env bash

while [ 1 ]
do
black --py36 --line-length 80 python_g*/*/*.py
sleep 5
done
