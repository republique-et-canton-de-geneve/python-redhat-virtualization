#!/usr/bin/env python

from ovirtsdk.api import API
from ovirtsdk.xml import params
import time, re, sys, datetime, argparse

parser = argparse.ArgumentParser()
parser.add_argument('-r',required=True, help="rhevm api url")
parser.add_argument('-u',required=True, help="rhevm username")
parser.add_argument('-p',required=True, help="rhevm password")
parser.add_argument('-k',required=True, help="rhevm CA")
parser.add_argument('-s',required=True, help="snapshot pattern")
args = parser.parse_args()

try:
    api = API (url=args.r, username=args.u, password=args.p, ca_file=args.k)
except Exception as ex:
    print "Unexpected error: %s" % ex

vms = api.vms.list()
for vm in vms:
    snapshot_list = vm.snapshots.list()
    for snapshot in snapshot_list:
        snapshot_date = snapshot.get_date()
        snapshot_description = snapshot.get_description()
        snapshot_description_match = re.match(args.s,snapshot_description)

        if snapshot_description == "Active VM":
            continue

        if snapshot_description_match:
            if snapshot.get_snapshot_status() == "ok":
                print time.strftime("%c") + " " + vm.name + " deleting: " + snapshot_description + " date: " + str(snapshot_date)
                try:
                    action = snapshot.delete()
                    job_id = action.get_job().get_id()
                except Exception as ex:
                    print "Unexpected error: %s" % ex
                time.sleep(5)
		if api.jobs.get(id=job_id).get_status().get_state() == "STARTED":
                    while (vm.snapshots.get(id=snapshot.id) is not None):
                        time.sleep(10)
                        print time.strftime("%c") + " " + vm.name + " wait for deletion, snap_status: " + snapshot.get_snapshot_status() + " job_status: " + api.jobs.get(id=job_id).get_status().get_state()
                        if api.jobs.get(id=job_id).get_status().get_state() == "FAILED":
                            break
api.disconnect()
