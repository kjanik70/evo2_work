#!/bin/bash
docker run --gpus all -it --rm \
    -p 8888:8888 \
    -v "$(pwd)":/workspace \
    nvcr.io/nvidia/pytorch:25.09-py3