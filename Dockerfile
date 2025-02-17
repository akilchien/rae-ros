ARG ROS_DISTRO=humble
FROM luxonis/depthai-ros-rae AS builder
ARG SIM=0
ARG CORE_NUM=1
ARG BUILD_TYPE="RelWithDebInfo"

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
   && apt-get -y install --no-install-recommends \
    software-properties-common \
    git \
    nano \
    libusb-1.0-0-dev \
    wget \
    zsh \
    python3-colcon-common-extensions \
    python3-rosdep \
    build-essential \
    neovim \
    tmux \
    htop \
    net-tools \
    iputils-ping \
    gpiod \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-alsa \
    libasound2-dev \
    busybox

ENV WS=/ws
RUN mkdir -p $WS/src
COPY ./ .$WS/src/rae-ros

RUN cp -R .$WS/src/rae-ros/assets/. /usr/share
RUN rm -rf .$WS/src/rae-ros/assets
RUN rm -rf .$WS/src/rae-ros/rae_gazebo

RUN cd  .$WS/ && apt update && rosdep update && rosdep install --from-paths src --ignore-src  -y --skip-keys depthai --skip-keys depthai_bridge --skip-keys depthai_ros_driver --skip-keys audio_msgs --skip-keys laserscan_kinect --skip-keys ira_laser_tools

RUN cd .$WS/ && . /opt/ros/${ROS_DISTRO}/setup.sh && . $UNDERLAY_WS/install/setup.sh && colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=${BUILD_TYPE}

RUN echo "if [ -f ${WS}/install/setup.zsh ]; then source ${WS}/install/setup.zsh; fi" >> $HOME/.zshrc
RUN echo 'eval "$(register-python-argcomplete3 ros2)"' >> $HOME/.zshrc
RUN echo 'eval "$(register-python-argcomplete3 colcon)"' >> $HOME/.zshrc
RUN echo "if [ -f ${WS}/install/setup.bash ]; then source ${WS}/install/setup.bash; fi" >> $HOME/.bashrc
ENTRYPOINT [ "/ws/src/rae-ros/entrypoint.sh" ]
RUN rm -rf /usr/share/doc

CMD ["zsh"]