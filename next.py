#! /usr/bin/env python

import os
import re
import sys
import copy
import time
import random
import argparse

def parse_dir(folder):
    results = []
    for cwd, dirs, files in os.walk(folder):
        for filename in files:
            fullname =  os.path.join(cwd, filename)
            results.append(fullname)

    random.shuffle(results)
    for result in results:
        tf = TodoFile(result)
        n = tf.next()
        if n:
            return tf


class TodoFile():
    def __init__(self, filename):
        self.line_counter = 0

        def line_not_empty(line):
            return True if line != '' else False

        self.filename = filename
        self.lines = map(self.level,
                         filter(line_not_empty,
                                open(filename).read().splitlines()))
    def level(self, line):
        self.line_counter += 1
        level_string, todo_string = re.match(r'^(\s*)(.*)$', line).group(1, 2)
        level = level_string.replace('    ', '\t').count('\t')
        return (self.line_counter, level, todo_string)

    def prev(self, offset):
        for i in range(offset, -1, -1):
            line_number, level, data = line = self.lines[i]
            if data and data[0] != 'x':
                return line
        return [-1, -1, '']

    def next(self):
        last_level = -1
        skipping = False
        skipping_level = 0
        data = ''
        line = (0, 0, '')
        for i in range(len(self.lines)):
            line_number, level, data = line = self.lines[i]
            if level == skipping_level:
                skipping = False
            elif level < skipping_level:
                skipping = False
                pln, pl, pd = prev_line = self.prev(i-1)
                if level == pl:
                    return prev_line
                else:
                    return line
            if data[0] == 'x':
                skipping = True
                skipping_level = level
            if skipping:
                pass
            else:
                if level <= last_level:
                    pln, pl, pd = prev_line = self.prev(i-1)
                    if level == pl:
                        return prev_line
                    else:
                        return line
            last_level = level
        return line


class DailyFile():
    def __init__(self, folder):
        self.daily_filename = os.path.join(folder, "daily.otl")
        self.log_filename = os.path.join(folder, ".daily_log")
        self.toggle_filename = os.path.join(folder, ".daily_toggle")

        self.parse_toggle()
        if self.turn:
            self.parse_log()
            self.parse_daily()
            self.write_log()

    def parse_toggle(self):
        try:
            toggle = open(self.toggle_filename).readline()
            self.turn = not int(toggle)
        except (IOError, ValueError):
            self.turn = True
        with open(self.toggle_filename, 'w') as toggle:
            toggle.write("{}\n".format(int(self.turn)))

    def parse_log(self):
        self.history = []
        self.todays_date = todays_date = time.strftime('%Y%m%d')
        try:
            log = open(self.log_filename).read().splitlines()
        except IOError:
            log = []
        if log:
            file_date = log[0]
            if len(log) > 1 and file_date == todays_date:
                self.history = log[1:]

    def parse_daily(self):
        found_new_item = False
        for line_number, item in enumerate(open(self.daily_filename).read().splitlines(), 1):
            if item in self.history:
                continue
            else:
                found_new_item = True
                break
        if not found_new_item:
            self.turn = False
        self.next_item = item
        self.next_action = (line_number, 0, item)

    def write_log(self):
        with open(self.log_filename, 'w') as log:
            log.write('%s\n' % self.todays_date)
            for history_item in self.history:
                log.write('%s\n' % history_item)
            log.write('%s\n' % self.next_item)

    def next(self):
        return self.next_action


class DoThisNext():
    def __init__(self):
        parser = argparse.ArgumentParser(description='Echo next action.')
        parser.add_argument('--edit', action='store_true', help='sets output format to editor arguments')
        parser.add_argument('folder', help='location of todo files')

        self.args = parser.parse_args()

        folder = self.args.folder

        self.inbox_filename = os.path.join(folder, 'inbox.otl')
        self.projects_dir = os.path.join(folder, 'projects')

        self.daily = DailyFile(folder)

    def run(self):
        if os.path.getsize(self.inbox_filename):
            tf = todo_file(self.inbox_filename)
            filename = tf.filename
            n = tf.next()
        else:
            if self.daily.turn:
                df = self.daily
                filename = df.daily_filename
                n = df.next()
            else:
                tf = parse_dir(self.projects_dir)
                filename = tf.filename
                n = tf.next()

        if n:
            line_number, level, data = n
            if self.args.edit:
                print '+%d %s' % (line_number, filename)
            else:
                print os.path.basename(filename)
                print data

if __name__ == '__main__':
    DoThisNext().run()

