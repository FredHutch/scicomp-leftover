#!/usr/bin/env python3

import subprocess
import sys
import json
import logging
import logging.handlers
from time import sleep
from time import time
from random import randint

crier = logging.getLogger('crybaby')
crier.setLevel(logging.DEBUG)
syslog = logging.handlers.SysLogHandler(
    address='/dev/log',
    facility='daemon'
)
crier.addHandler(syslog)

crier.info('INFO: leftover starting')

configs = {}

try:
    with open('/etc/leftover.conf') as f:
        configs = json.loads(f.read())
except FileNotFoundError:
    crier.warning("WARNING: no config file found, proceeding with defaults")

# Sleep for a random number of seconds to keep the leftovers on all the nodes
# from dogpiling on the Slurm controller
# https://github.com/FredHutch/scicomp-todo/issues/294
if "slew" in configs:
    slew = configs['slew']
    if "slew_max" in configs:
        slew = randint(slew, configs['slew_max'])
else:
    slew = 2

if "debuglevel" in configs:
    debuglevel=configs['debuglevel']
    crier.debug('DEBUG: setting loglevel to %s', debuglevel)
    match debuglevel:
        case "debug":
            crier.setLevel(logging.DEBUG)
        case "info":
            crier.setLevel(logging.INFO)
        case "warning":
            crier.setLevel(logging.WARNING)
        case "error":
            crier.setLevel(logging.ERROR)
        case "critical":
            crier.setLevel(logging.CRITICAL)


crier.info('INFO: leftover sleeping %s seconds', slew)
sleep(slew)
crier.info('INFO: leftover starting process audit')

protected_users = []

with open('/etc/passwd', 'r') as passwd:
    entry = passwd.readline()
    while entry:
        (user, pw, uid, gid, grp, home, shell) = entry.split(':')
        if int(uid) < 1000:
            protected_users.append(user)
            crier.debug(
                    "DEBUG: leftover aded {} to protected users".format(user)
                    )
        entry = passwd.readline()

if "protected_users" in configs:
    protected_users = protected_users + configs['protected_users']
    crier.debug(
            "DEBUG: leftover aded {} ".format(configs['protected_users']) +
            "to protected users from config"
            )


# find all the nodes configured on this host when
# multiple slurmd's are running

cmd = ['scontrol', 'show', 'aliases']
try:
    result = subprocess.run(cmd, capture_output=True, text=True)
except subprocess.CalledProcessError as err:
    crier.critical(
        'CRITICAL: scontrol failed to find aliases: %s %s',
        err.returncode,
        err.output
    )
    sys.exit(1)

nodenames = ','.join(result.stdout.rstrip().split())

if nodenames == '':
    crier.critical(
        'CRITICAL: \'nodenames\' is empty- is this node in the cluster?'
    )
    sys.exit(1)

crier.debug(
    'DEBUG: set node names to \'%s\'', nodenames
)

cmd = ['squeue', '-a', '-h', '-w', nodenames, '-o', '%u']

time_squeue_start = time()

try:
    result = subprocess.run(cmd, capture_output=True, text=True)
except subprocess.CalledProcessError as err:
    crier.critical(
        'CRITICAL: squeue command failed with error %s: %s',
        err.returncode,
        err.output
    )
    sys.exit(1)

squeue_elapsed = time() - time_squeue_start
crier.debug(
    'DEBUG: squeue run took %i seconds', squeue_elapsed
)

if squeue_elapsed > 2:
    # if squeue doesn't respond within 2 seconds we'll consider
    # the output "stale" so we don't kill jobs that are started
    # while this script runs
    crier.error('ERROR: squeue did not respond in a timely manner, exiting')
    sys.exit(0)

valid_users = set(result.stdout.rstrip('\n').split('\n'))
valid_users = valid_users.union(protected_users)

cmd = ['ps', '--no-headers', '-e', '-o', 'user']
result = subprocess.run(cmd, capture_output=True, text=True)
running_users = set(result.stdout.rstrip('\n').split('\n'))

invalid_users = running_users.difference(valid_users)

if len(invalid_users) == 0:
    crier.debug('DEBUG: leftover found no users with invalid jobs,' +
                'len(invalid_users)=%s', len(invalid_users))
    exit

for u in invalid_users:
    crier.info('killing processes belonging to user %s', u)
    cmd = ['pkill', '-TERM', '-u', u]
    try:
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as err:
        crier.debug('pkill exited with %s %s', err.returncode, err.output)
        crier.error('ERROR: pkill could not TERM processes from %s', u)
        continue

    sleep(8)

    cmd = ['pkill', '-KILL', '-u', u]
    try:
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as err:
        if err.returncode == 1:
            crier.debug("DEBUG: pkill exited non-zero," +
                        "no processes left to kill")
            continue
        else:
            crier.debug(
                'DEBUG: pkill exited with %s %s', err.returncode, err.output
            )
            crier.error('ERROR: pkill could not KILL processes from %s', u)
            continue
