#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1.0
@author: Carrot 
@contact: huxueli1986@163.com
@software: PyCharm
@file: weipan.py
@time: 16-9-1 下午11:08
"""

from wpbService import WPBService as WPBS

def main():
    service = WPBS()
    print service
    print WPBS()

if __name__ == '__main__':
    main()