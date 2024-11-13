# Leftover

> TBD describe leftover operations

## Building

### Build Docker Container

In this directory:

```
docker build --build-arg UID=$(id -u) --build-arg=USERNAME=$(whoami) -t scicomp-leftover .
```

### Run Docker Container

```
docker run -it --rm \
  --mount type=bind,source=$(pwd),target=/mnt \
  -e RELEASE=0.0.2 \
  -e PACKAGE=scicomp-leftover \
  scicomp-leftover
```

This will drop you to a command prompt inside the container

### Build Package

```
user@95cdeb870a74:/mnt $ cd /mnt/scicomp-leftover/
user@95cdeb870a74:/mnt/scicomp-leftover$ make deb
```
