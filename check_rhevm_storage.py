#!/usr/bin/env python

from __future__ import division
from ovirtsdk.api import API
from ovirtsdk.xml import params
import re, argparse, sys

parser = argparse.ArgumentParser()
parser.add_argument('-d',required=True, help="datacenter name")
parser.add_argument('-r',required=True, help="rhevm api url")
parser.add_argument('-u',required=True, help="rhevm username")
parser.add_argument('-p',required=True, help="rhevm password")
parser.add_argument('-k',required=True, help="rhevm CA")
parser.add_argument('-w',required=True, help="warning in %", type=int)
parser.add_argument('-c',required=True, help="critical in %", type=int)
args = parser.parse_args()

try:
    api = API (url=args.r,
               username=args.u,
               password=args.p,
               ca_file=args.k)

    datacenter=api.datacenters.get(args.d)

    exit_state="OK"
    if  datacenter.get_status().get_state() != "up":
        out=datacenter.name + datacenter.get_status().get_state()
        exit_state="CRITICAL"
    else:
        out=datacenter.name + " up"

    storage_maintenance=0
    storage_active=0

    storages=datacenter.storagedomains.list()
    out_storage=""
    storage_total_used=0
    storage_total_available=0
    for storage in storages:
        if storage.get_status().get_state() == "active":
            storage_active += 1
            storage_usage=round(storage.get_used() / (storage.get_available() + storage.get_used()) * 100,1)
            storage_total_used += storage.get_used()/1024/1024/1024
            storage_total_available += storage.get_available()/1024/1024/1024
            storage_free=int(storage.get_available()/1024/1024/1024)
            storage_size=storage.get_available() + storage.get_used()
            if storage_usage >= args.c:
                exit_state="CRITICAL"
                out_storage=out_storage + " / CRITICAL " + storage.name + " " + str(storage_usage) + "% " + str(storage_free) + "Go Free"
            elif storage_usage >= args.w:
                exit_state="WARNING"
                out_storage=out_storage + " / WARNING " + storage.name + " " + str(storage_usage) + "% " + str(storage_free) + "Go Free"
            else:
                exit_state="OK"
        elif storage.get_status().get_state() == "maintenance":
            storage_maintenance += 1
        else:
            exit_state="CRITICAL"
            out=out + " / " + storage.name + " is " + storage.get_status().get_state()
    if storage_maintenance == 0:
        out=out + " (active:" + str(storage_active) + ")"
    else:
        out=out + " (active:" + str(storage_active) + " maintenance:" + str(storage_maintenance) + ")"
    
    api.disconnect()

    print out + out_storage + " | total_used=" + str(round(storage_total_used/1024,1)) + "TB total_avail=" + str(round(storage_total_available/1024,1)) + "TB"
    if exit_state == "OK":
        sys.exit(0)
    elif exit_state == "WARNING":
        sys.exit(1)
    elif exit_state == "CRITICAL":
        sys.exit(2)
    elif exit_state == "UNKNOWN":
        sys.exit(3)

except Exception as ex:
    print "Unexpected error: %s" % ex
