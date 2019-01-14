# Python scripts for RedHatⓇ RHEV-M

# Table of contents

- [Running](#running)
    - [Preconditions](#preconditions)
    - [Usage](#usage)


# Running

## Preconditions
The following software needs to be installed to run the scripts:
- [Red Hat Virtualization Python SDK](https://access.redhat.com/documentation/en-us/red_hat_virtualization/4.2/html-single/python_sdk_guide/index)

## Usage

### check_rhevm_storage
check_rhevm_storage is a nagios plugin script which checks all storages of the specified datacenter, alerting you rhen the threshold has ben reached.

You can use the `-h` argument for help :
```
$ ./check_rhevm_storage.py -h
usage: check_rhevm_storage.py [-h] -d D -r R -u U -p P -k K -w W -c C

optional arguments:
  -h, --help  show this help message and exit
  -d D        datacenter name
  -r R        rhevm api url
  -u U        rhevm username
  -p P        rhevm password
  -k K        rhevm CA
  -w W        warning in %
  -c C        critical in %
```

### snapshot_delete
snapshot_delete is a script that will delete all snapshots matching your pattern.

You can use the `-h` argument for help :
```
$ ./snapshot_delete.py -h
usage: snapshot_delete.py [-h] -r R -u U -p P -k K -s S

optional arguments:
  -h, --help  show this help message and exit
  -r R        rhevm api url
  -u U        rhevm username
  -p P        rhevm password
  -k K        rhevm CA
  -s S        snapshot pattern
```