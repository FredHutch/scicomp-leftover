FROM ubuntu:noble
ENV DEBIAN_FRONTEND=noninteractive
ARG UID USERNAME
RUN <<EOF
apt-get update
apt-get install -y tzdata python3 python3-venv binutils python3-dev python3-build make vim
ln -fs /usr/share/zoneinfo/America/Los_Angeles /etc/localtime
dpkg-reconfigure -f noninteractive tzdata
EOF
RUN <<EOF
useradd -u ${UID} -d /home/${USERNAME} --shell /bin/bash -U -m ${USERNAME}
EOF
USER ${USERNAME}:${UID}
CMD [ "/bin/bash", "-il" ]
