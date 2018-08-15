#!/usr/bin/env python3

openvpn_log = '/var/log/openvpn/openvpn.log'
openvpn_index = '/opt/easy-rsa2/2.0/keys/index.txt'

import sys
from dateutil import parser

users = {}
last_logins = {}

with open(openvpn_index, 'r') as fh:
    for line in fh:
        fields = line.split("\t")
        status = fields[0]
        create = fields[1]
        key_id = fields[3]
        dn = fields[5]
        dn_fields = {}
        for dn_field in dn.lstrip('/').split('/'):
            dn_key = dn_field.split('=', 1)[0]
            dn_value = dn_field.split('=', 1)[1]
            dn_fields[dn_key] = dn_value
        user_id = dn_fields['CN']

        users[user_id] = {
            'status': status,
            'create': create,
            'key_id': key_id,
            'name': dn_fields['name'],
            'email': dn_fields['emailAddress'].strip(),
        }

with open(openvpn_log, 'r') as fh:
    for line in fh:
        if 'Peer Connection Initiated' in line:
            username = line.split('[', 1)[1].split(']', 1)[0]
            date_raw = line[0:24]
            date = parser.parse(date_raw)
            last_logins[username] = date

for user in users.keys():
    if users[user]['status'] != 'R' and user not in last_logins:
        print("{} Not logged in since beginning of log: {}".format(users[user]['status'], user))

for username in sorted(last_logins, key=last_logins.get):
    user_status = users[username]['status']
    if user_status != 'R':
        print ("{} {} {}".format(user_status, last_logins[username], username))

