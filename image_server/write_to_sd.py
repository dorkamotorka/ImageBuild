#!/usr/bin/env python

import os

sd_cards = ['sda, sdb, sdc, sdd']

if __name__ == '__main__':
    for sd in sd_cards:
        if (os.path.join('dev', sd)):
            pass


'''
1. Is sd card plugged
2. Is sd card unplugged
3. Is new sd card plugged
4. Which img is installed
5. Is installed img latest
'''
