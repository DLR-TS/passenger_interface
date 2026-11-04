#!/bin/bash
set -e

source /opt/ros/jazzy/setup.bash

if [ ! -f /opt/pipeline_install/setup.bash ] || [ "${PIPELINE_REBUILD}" = "1" ]; then
    echo "Building adore_ros2_msgs and passenger_interface ..."
    colcon build \
        --symlink-install \
        --base-paths /workspace/src \
        --build-base /opt/pipeline_build \
        --install-base /opt/pipeline_install \
        --packages-select adore_ros2_msgs passenger_interface
fi

source /opt/pipeline_install/setup.bash

exec "$@"
