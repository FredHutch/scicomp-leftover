# Leftover

`leftover` runs on Slurm daemon nodes (compute nodes) and monitors the process stack for processes that are running without an allocation.

More precisely, it kills processes from "regular" users who do not have an allocation on the node.  It compares the process table and the list of users who have jobs running on the node.

The config file is a simple JSON file that contains a list of users who should be exempted from `leftover` pruning.

Ultimately, this list of exempt users is combined with passwd(5) entries with UID less than 1000 to create a full list of users who's processes are allowed to run on the node.

`leftover` uses `squeue` to get UIDs with allocations on the node- if `squeue` should fail for any reason or if `squeue` doesn't return in a timely fashion (2 seconds) it will bail out and note the problem in syslog.

## Building

Building the `leftover` package uses `pyinstaller` to create a binary package which is then bundled into a .deb package for installation on the node.

A Docker container is used to build this- see the `Dockerfile` in this repo.

### Get

Check out this source and make it your working directory.

```
git clone git@github.com:FredHutch/scicomp-leftover.git
cd scicomp-leftover
```

All the steps below assume that the source directory is your working directory.

Make any modifications- test and then choose a new version number.  Update `pyproject.toml` and note the new version for the commands below.  Update the changelog, commit all changes, and tag with the version number.

Check out the tag prior to building the package.

### Build Docker Container

In this directory:

```
docker build --build-arg UID=$(id -u) --build-arg=USERNAME=$(whoami) -t scicomp-leftover .
```

### Run Docker Container

When running the docker container, update the environment variable in this command to match the release you are building.

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
user@95cdeb870a74:/mnt$ make deb
```

Package will show up in the `debian` subdirectory.
