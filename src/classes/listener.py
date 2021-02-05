# ==================================================================================
#   File:   listener.py
#   Author: Larry W Jordan Jr (larouex@gmail.com)
#   Use:    A simple pub/sub listener that returns the payload
#
#   Online:   https://github.com/Larouex/SmartKitchenForAzureIoTCentral
#
#   (c) 2021 Larouex Software Design LLC
#   This code is licensed under MIT license (see LICENSE.txt for details)
# ==================================================================================
import  getopt, sys, time, string, threading, asyncio, os, kwargs
import logging as Log

# PubSub module
from pubsub import pub

class Listener():

    def __init__(self):
      self.payload = {}

    def __call__(self, **kwargs):
      # read and parse the payload
      self.payload = kwargs["result"]

    def read_payload(self):
      return self.payload
