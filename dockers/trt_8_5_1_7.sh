#!/bin/bash

export PATH=$(echo $PATH | sed 's|/opt/TensorRT-8.5.10.4/bin|/opt/TensorRT-8.5.1.7/bin|g')
export LD_LIBRARY_PATH=$(echo $LD_LIBRARY_PATH | sed 's|/opt/TensorRT-8.5.10.4/lib|/opt/TensorRT-8.5.1.7/lib|g')
export TENSORRT_DIR=/opt/TensorRT-8.5.1.7
export TRT_VERSION=8.5.1.7

# switch python version
sudo pip install /opt/TensorRT-8.5.1.7/python/tensorrt-8.5.1.7-cp38-none-linux_x86_64.whl
