#!/usr/bin/env python3
"""
Implementation of generateds collector.

This has been split out from nml.py so that the collector can be used in
generatedssupersuper.py

File: neuroml/nml.py/generatedscollector.py

Copyright 2022 Ankur Sinha
Author: Ankur Sinha <sanjay DOT ankur AT gmail DOT com>
"""


class GdsCollector(object):
    def __init__(self, messages=None):
        if messages is None:
            self.messages = []
        else:
            self.messages = messages

    def add_message(self, msg):
        self.messages.append(msg)

    def get_messages(self):
        return self.messages

    def clear_messages(self):
        self.messages = []

    def print_messages(self):
        for msg in self.messages:
            print("Warning: {}".format(msg))

    def write_messages(self, outstream):
        for msg in self.messages:
            outstream.write("Warning: {}\n".format(msg))