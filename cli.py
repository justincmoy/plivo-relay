from actions import action_handler

import argparse
import random
import time

parser = argparse.ArgumentParser()
parser.add_argument('--action', action='append')
args = parser.parse_args()

sleep_time = random.randint(0, 300)
print('sleeping {0} seconds'.format(sleep_time))
time.sleep(sleep_time)
for action in args.action:
    action_handler('cli', action)
