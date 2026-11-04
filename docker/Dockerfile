FROM ros:jazzy-ros-base

RUN apt-get update && apt-get install -y --no-install-recommends \
        libportaudio2 \
        python3-colcon-common-extensions \
        python3-venv \
        ros-jazzy-geometry-msgs \
        ros-jazzy-nav-msgs \
        ros-jazzy-shape-msgs \
        ros-jazzy-std-msgs \
    && rm -rf /var/lib/apt/lists/*

ENV VIRTUAL_ENV=/opt/pipeline_venv
RUN python3 -m venv --system-site-packages ${VIRTUAL_ENV}
ENV PATH=${VIRTUAL_ENV}/bin:${PATH}

RUN pip install --no-cache-dir \
        sounddevice==0.5.2 \
        faster-whisper==1.2.0 \
        ollama==0.6.2 \
        scipy \
        nvidia-cublas-cu12==12.9.2.10 \
        nvidia-cudnn-cu12==9.25.0.15

ENV PYTHONDONTWRITEBYTECODE=1
ENV SOURCE_DIRECTORY=/workspace

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

WORKDIR /workspace
ENTRYPOINT ["/entrypoint.sh"]
CMD ["ros2", "launch", "passenger_interface", "speech_to_command_pipeline.py"]
