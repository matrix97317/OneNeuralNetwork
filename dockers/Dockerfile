# This dockerfile is used to Training/Evaluation/Deploy.

# Specific Source Image FROM:
# https://docs.nvidia.com/deeplearning/frameworks/pytorch-release-notes/
ARG NVIDIA_PYTORCH_VERSION=22.12
FROM nvcr.io/nvidia/pytorch:${NVIDIA_PYTORCH_VERSION}-py3

# General settings.
ARG DEBIAN_FRONTEND=noninteractive

# Config Ubuntu Mirror.
ARG UBUNTU_MIRROR=mirrors.ustc.edu.cn
RUN sed -i -e "s/security.ubuntu.com/${UBUNTU_MIRROR}/g" -e "s/archive.ubuntu.com/${UBUNTU_MIRROR}/g" /etc/apt/sources.list

# System-level package installation.
# - curl, openssh-server, sudo: Necessary dependency for NIO cluster.
# - ffmpeg: For visualization.
# - libboost-all-dev: Boost dev C++ lib for read_cache_op_py.
# - libgl1: For OpenCV.
# - libturbojpeg: TurboJPEG's lib
# - lsb-release: Gather release information for docker installation.
RUN apt-get update && apt-get install -y \
    curl \
    ffmpeg \
    libboost-python-dev \
    libgl1 \
    libturbojpeg \
    lsb-release \
    openssh-server \
    python3.8-venv \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# Config Docker gpg key and repository with custom mirror.
# Reference: https://docs.docker.com/engine/install/ubuntu/#set-up-the-repository
ARG DOCKER_MIRROR=mirrors.ustc.edu.cn/docker-ce
RUN curl -fsSL https://${DOCKER_MIRROR}/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
RUN echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://${DOCKER_MIRROR}/linux/ubuntu \
    $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

# Software-level package installation.
# - docker-ce-cli: docker client for image build.
RUN apt-get update && apt-get install -y \
    docker-ce-cli \
    && rm -rf /var/lib/apt/lists/*

# Hack for dirty partial installation of opencv python package.
RUN rm -rf /opt/conda/lib/python3.8/site-packages/cv2

# Upgrade pip to the latest version.
RUN python3 -m pip install --no-cache-dir --upgrade pip

# Install NVIDIA apex
RUN git clone --recursive https://github.com/NVIDIA/apex.git /opt/apex
RUN cd /opt/apex && git checkout 2386a912164b0c5cfcd8be7a2b890fbac5607c82
RUN cd /opt/apex && MAX_JOBS=32 pip3 install --no-build-isolation --no-cache-dir -v  --config-settings="--global-option=--cpp_ext"  --config-settings="--global-option=--cuda_ext" --config-settings="--global-option=--permutation_search" --config-settings="--global-option=--peer_memory" --config-settings="--global-option=--cudnn_gbn" ./

# Install pypcd
RUN git clone --recursive https://github.com/dimatura/pypcd /opt/pypcd
RUN cd /opt/pypcd && git fetch origin pull/9/head:python3 && git checkout python3 \
    && python3 setup.py install && rm -rf /opt/pypcd

# Config PyPI Mirror.
ARG PIP_INDEX_URL=https://mirror.sjtu.edu.cn/pypi/web/simple
ENV PIP_INDEX_URL=${PIP_INDEX_URL}

# Install and config pipx (with conda python).
RUN python3 -m pip install --no-cache-dir pipx
ENV PIPX_HOME=/usr/local/pipx
ENV PIPX_BIN_DIR=/usr/local/bin

# Install requirements and dev requirements in conda python.
COPY requirements.txt requirements-dev.txt ./
RUN python3 -m pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt

# Hack for the inconsistent behavior of tensorboard in base image.
# This should be deleted after the strange behavior reverted in base image.
# https://github.com/tensorflow/tensorboard/issues/5648

# RUN [[ -f /opt/conda/lib/python3.8/site-packages/tensorboard/plugins/core/core_plugin.py ]] \
#     && sed -i "s/\"--bind_all\", default=True,/\"--bind_all\",/g" /opt/conda/lib/python3.8/site-packages/tensorboard/plugins/core/core_plugin.py

# /usr/local/lib/python3.8/dist-packages/tensorboard/plugins/core/core_plugin.py

RUN [[ -f /usr/local/lib/python3.8/dist-packages/tensorboard/plugins/core/core_plugin.py ]] \
    && sed -i "s/\"--bind_all\", default=True,/\"--bind_all\",/g" /usr/local/lib/python3.8/dist-packages/tensorboard/plugins/core/core_plugin.py

# Install requirements to satisfy niofs installation.
# This should be deleted after upstream bug fix.
RUN python3 -m pip install --no-cache-dir boto3 requests

# Install and config pipenv via pipx.
RUN pipx install pipenv --pip-args="--no-cache-dir"
ENV PIPENV_VENV_IN_PROJECT=true
ENV PIPENV_MAX_DEPTH=0

# Install pre-commit via pipx.
RUN pipx install pre-commit --pip-args="--no-cache-dir"

# Install onnxruntime lib
RUN cd /opt && wget https://github.com/microsoft/onnxruntime/releases/download/v1.8.1/onnxruntime-linux-x64-1.8.1.tgz
RUN cd /opt && tar -xzvf onnxruntime-linux-x64-1.8.1.tgz
RUN chmod a+rwx /opt/onnxruntime-linux-x64-1.8.1
RUN export ONNXRUNTIME_DIR=/opt/onnxruntime-linux-x64-1.8.1
RUN export LD_LIBRARY_PATH=$ONNXRUNTIME_DIR/lib:$LD_LIBRARY_PATH
RUN rm -f /opt/onnxruntime-linux-x64-1.8.1.tgz

# Install tensorrt lib
# Please download TensorRT-8.5.1.7.Linux.x86_64-gnu.cuda-11.8.cudnn8.6.tar.gz to local.
COPY TensorRT-8.5.1.7.Linux.x86_64-gnu.cuda-11.8.cudnn8.6.tar.gz /opt
RUN cd /opt && tar -xzvf TensorRT-8.5.1.7.Linux.x86_64-gnu.cuda-11.8.cudnn8.6.tar.gz
RUN chmod a+rwx /opt/TensorRT-8.5.1.7
RUN export TENSORRT_DIR=/opt/TensorRT-8.5.1.7
RUN export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$TENSORRT_DIR/lib
RUN export PATH=$PATH:$TENSORRT_DIR/bin
RUN rm -f /opt/TensorRT-8.5.1.7.Linux.x86_64-gnu.cuda-11.8.cudnn8.6.tar.gz

# Dev pacakge installation.
RUN apt-get update && apt-get install -y \
    bash-completion \
    htop \
    locales \
    python3.8-tk \
    sshpass \
    tmux \
    zsh \
    zsh-autosuggestions \
    zsh-syntax-highlighting \
    && rm -rf /var/lib/apt/lists/*
RUN locale-gen en_US.UTF-8

# Various settings mostly for dev.
# - Disable pip without virtual env for dev.
ENV PIP_REQUIRE_VIRTUALENV=true
# - Disable local python packages for dev.
ENV PYTHONNOUSERSITE=1
# - Set default editor to vim mostly for git.
ENV EDITOR=vim
# - Set locale related env.
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV LC_CTYPE=en_US.UTF-8

# build docker images all environment vars
COPY env_vars /opt
RUN chmod a+rwx /opt/env_vars
RUN cat /opt/env_vars | while read line; do echo $line; done  >> ~/.bashrc

# build 2 versions of trt environment vars
COPY trt_8_5_1_7.sh /opt
