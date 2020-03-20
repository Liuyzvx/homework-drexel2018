#!/usr/bin/env/python3
# -*- coding:UTF-8 -*-
"""
This program can get git log information.
In order to use it easily, it has three parameters:
-v: The version of git
-r: The range of revision from the base version
-c: cumulative
"""
__author__ = "LiuYueze"
__copyright__ = "Copyright 2019, OpenTech Research"
__credits__ = ["LiuYueze"]
__version__ = "2"
__maintainer__ = "Linux maintainer"
__email__ = "liuyz18@lzu.edu.com"
__status__ = "Experimental"

import os
import re
import sys
import subprocess
import argparse
from datetime import datetime as dt


class ExistException(BaseException): #Basic error detection statement
    def __str__(self):
        error = 'Wrong git'
        return error


class GitLog: #Get basic git version information
    def __init__(self):
        parser = argparse.ArgumentParser(description="parse")
        parser.add_argument('-v', '--version', default='V4.4', required=True, help='The version of git')
        parser.add_argument('-r', '--range', default=2, required=True, help='The range of revision from the base version')
        parser.add_argument('-c', '--cumulative', help='cumulative')
        args = parser.parse_args()

        self.rev = args.version
        if args.cumulative == "c":
            cumulative = 1
        else:
            print("Error: No meaning with {0}".format(args.cumulative))
            cumulative = 0
            sys.exit(1)
        rev_range = int(args.range)
        self.git(cumulative, rev_range)

    def getcommit(self, git_cmd): #Count the number of commits
        try:
            raw_counts = git_cmd.communicate()[0]
            if raw_counts == 0:
                raise ExistException
        except ExistException as error:
            print(error)
            sys.exit(2)

        cnt = re.findall('[0-9]*-[0-9]*-[0-9]*', str(raw_counts))
        return len(cnt)

    def gettag(self, git_cmd, base): #Get time information for each commit
        try:
            seconds = git_cmd.communicate()[0]
            if seconds == 0:
                raise ExistException
        except ExistException as err:
            print(err)
            sys.exit(2)
        return (int(seconds) - base) // (3600 * 24)

    def git(self, cumulative, rev_range): #Main functions of capturing git log
        gettime = "git log -1 --pretty=format:\"%ct\" " + self.rev
        getime = subprocess.Popen(gettime, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
        basetime = int(getime.communicate()[0])

        print("#sublevel commits {0} stable fixes".format(self.rev))
        print("lv days bugs")
        rev1 = self.rev

        for sl in range(1, rev_range + 1):
            rev2 = self.rev + "." + str(sl)
            gitcnt = "git rev-list --pretty=format:\"%ai\" " + rev1 + "..." + rev2
            gittag = "git log -1 --pretty=format:\"%ct\" " + rev2
            git_rev_list = subprocess.Popen(gitcnt, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
            commit_cnt = self.getcommit(git_rev_list)
            if cumulative == 0:
                rev1 = rev2
            if commit_cnt:
                git_tag_date = subprocess.Popen(gittag, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
                days = self.gettag(gittag, basetime)
                print("%d %d %d" % (sl, days, commit_cnt))
            else:
                break

if __name__ == '__main__':
    collect = GitLog()

