# -*- coding: utf-8 -*-
__author__ = 'cabbyw'

import os
import subprocess
import io


def main():
    # sp = subprocess.Popen('python /Users/wangsiyong/workspace/github/practice/others/a.py', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    # out = sp.communicate(b'asdfgh', timeout=10)
    # print('111', out)

    p = os.popen('python /Users/wangsiyong/workspace/github/practice/others/a.py', 'w')
    p.write('password')


main()
