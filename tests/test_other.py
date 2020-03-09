#!/usr/bin/env python

import pytest
import time
from pyzatt.misc import *
import pyzatt.pyzatt as pyzatt
import pyzatt.zkmodules.defs as defs

"""
Test script to test/show several functions of the "other" spec/lib.

WARNING: Apply this test to devices that aren't under current use,
    if a deployed device is used, remember to upload the data to
    the device(Sync) using the ZKAccess software, that would
    overwrite any changes made by the script.

Author: Alexander Marin <alexanderm2230@gmail.com>
"""

def enroll(id, fp_idx, fp_flag):
    print_info("Enrolling user:")
    print("User ID = ", id)
    print("Finger index = ", fp_idx)
    print("Fingerprint type = ", fp_flag)

    print_info("Delete previous fingerprint")
    z.delete_fp(id, fp_idx)

    print_info("Ready to enroll!")
    if z.enroll_user(id, fp_idx, fp_flag):
        print("Enrolling was successful")
        z.read_all_user_id()
        z.refresh_data()
    else:
        print("Something went wrong")

@pytest.mark.skip(reason="manual test")
@pytest.mark.manual
def test_enroll(parse_options):
    assert parse_options, "Invalid run settings"
    opts = parse_options

    ip_address = opts['ip-address']  # set the ip address of the device to test
    machine_port = 4370

    z = pyzatt.ZKSS()
    z.connect_net(ip_address, machine_port)

    print_header("1. Enrolling a users fingerprints")

    print_info("Before enrolling users")
    z.read_all_user_id()
    z.read_all_fptmp()
    z.print_users_summary()

    print_info("Enrolling User 1")
    user1_id = "8888"
    user1_fp_idx = 4
    enroll(id=user1_id, fp_idx=user1_fp_idx, fp_flag=1)

    z.disable_device()
    with open('fp1.bin', 'wb') as outfile:
        outfile.write(z.download_fp(user1_id, user1_fp_idx))

    z.enable_device()
    print_info("Enrolling User 2")
    user2_id = "9999"
    user2_fp_idx = 3
    enroll(id=user2_id, fp_idx=user2_fp_idx, fp_flag=1)

    z.disable_device()
    with open('fp2.bin', 'wb') as outfile:
        outfile.write(z.download_fp(user2_id, user2_fp_idx))

    print_info("After enrolling users")
    z.read_all_user_id()
    z.read_all_fptmp()
    z.print_users_summary()

    z.enable_device()
    z.disconnect()
