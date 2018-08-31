#!/usr/bin/python3
"""
Slimcoin (SLM) Transaction Bot
Testing daemon load and network speed
Based on https://github.com/pallas1/Cryptonite_TxBot
(C) 2018 The Slimcoin Developers
"""
import sys
import json
import time
import random
import requests

# Bot Version
VERSION = '0.0.1'

# Delay
NO_DELAY = False
DELAY_RANGE = [100, 1000]

# Txn amount range, the upper
# bound is exclusive
AMOUNT_RANGE = [0, 5]

# Limiters, set -1 to disable
# type of limitation
MAX_TXN_COUNT = 100
MIN_SELF_BALANCE = -1

# Destination Address
DEST_ADDRESS = 'SZi78yGXFxsdLqTyyYmYtDA28uC3DPjYLc'

# Connection, It is probably a good idea to run
# the daemon locally.
JSON_RPC_URL_BASE = 'http://{username}:{password}@127.0.0.1:41683/'


def get_connect_details():
    try:
        user, password = sys.argv[-2:]
        return user, password
    except:
        print('account, rpc username and password '
              'needs to be passed as cli args')
        sys.exit(1)


# hacky global variable,
# please do not mind.
_cli_count_register = 1
def cli(url, method, *params):
    jid = str(_cli_count_register)

    payload = {
        'id': jid,
        'jsonrpc': '1.0',
        'method': method,
        'params': params,
    }

    response = requests.post(url=url,
                    data=json.dumps(payload),
                    headers={
                        'Content-Type': 'text/plain',
                    })

    if response.status_code != 200 :
        raise Exception(response.status_code)

    result = response.json()

    if result['error'] is not None:
        raise Exception(result['error'])

    return jid, result['result']


def get_random_amount():
    whole_amount = random.randint(*AMOUNT_RANGE)
    decimal_amount = random.randint(1, 99999999)
    decimal_amount = decimal_amount/100000000.0
    
    amount = (whole_amount + decimal_amount)
    amount = float(format(amount, '.6f'))

    return (amount + 0.1) if amount < 0.01 else amount


def main(url):
    print('Starting Slimcoin Transaction Bot {}'.format(VERSION))

    # check for limiting conditions
    if MAX_TXN_COUNT == MIN_SELF_BALANCE == -1:
        print('no bot txn limiting condition was set')
        return

    if MAX_TXN_COUNT != -1 and MIN_SELF_BALANCE != -1:
        print('multiple txn limiting condition are set, '
              'strictly requires only one')
        return

    # url passed should represent the json rpc endpoint of
    # the slimcoin node along with credential.
    try:
        _, result = cli(url, 'getinfo')
        print('Found Slimcoin daemon {}, total balance {}'.format(
            result['version'], result['balance']))
    except Exception:
        print('Cannot connect to Slimcoin JSON-RPC daemon')

    txn_count_register = 0
    while True:

        # check count limiting condition
        if MAX_TXN_COUNT != -1:
            if txn_count_register >= MAX_TXN_COUNT:
                print('max txn count reached ({})'.format(
                      txn_count_register))
                return

        # check for balance limiting condition 
        if MIN_SELF_BALANCE != -1:
            _, balance = cli(url, 'getbalance')
            if balance <= MIN_SELF_BALANCE:
                print('min self account balance reached ({})'
                      .format(balance))
                return

        try:
            amount = get_random_amount()
            
            _, txn = cli(url, 'sendtoaddress', DEST_ADDRESS, amount)
            txn_count_register += 1

            print('#{} @{:.3f} txn initiated {}'.format(
                  txn_count_register, time.time(), txn))
        except Exception as exp:
            print('#{} failed initiating transaction, aborting...\n{}'
                  .format(txn_count_register+1, exp))
            return

        if not NO_DELAY:
            delay = random.randint(*DELAY_RANGE)
            print('delaying {} μs'.format(delay))
            time.sleep(delay/1000.0)


if __name__ == '__main__':
    username, password = get_connect_details()
    url = JSON_RPC_URL_BASE.format(username=username,
                                   password=password)

    main(url)
