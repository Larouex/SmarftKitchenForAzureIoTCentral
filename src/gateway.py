#/usr/bin/env python3.8
# ==================================================================================
#   File:   gateway.py
#   Author: Larry W Jordan Jr (larouex@gmail.com)
#   Use:    Transparent Gateway OPC Server for Telemetry to Azure IoT Central
#
#   Online:   https://github.com/Larouex/SmartKitchenForAzureIoTCentral
#
#   (c) 2021 Larouex Software Design LLC
#   This code is licensed under MIT license (see LICENSE.txt for details)
# ==================================================================================
import  hmac, getopt, sys, time, binascii, \
        struct, string, threading, asyncio, os

import logging as Log

# our classes
from classes.config import Config
from classes.gateway import Gateway

# Workers
config_data = None

# -------------------------------------------------------------------------------
#   Start Gateway
# -------------------------------------------------------------------------------
async def gateway_run():

  gateway = Gateway(Log)
  await gateway.run()

  return True

async def main(argv):

    # execution state from args
    whatif = False

    short_options = "hvd"
    long_options = ["help", "verbose", "debug"]
    full_cmd_arguments = sys.argv
    argument_list = full_cmd_arguments[1:]

    try:
        arguments, values = getopt.getopt(argument_list, short_options, long_options)
    except getopt.error as err:
        print (str(err))

    for current_argument, current_value in arguments:

      if current_argument in ("-h", "--help"):
          print("HELP for gateway.py")
          print("------------------------------------------------------------------------------------------------------------------")
          print("-h or --help - Print out this Help Information")
          print("-v or --verbose - Debug Mode with lots of Data will be Output to Assist with Debugging")
          print("-d or --debug - Debug Mode with lots of DEBUG Data will be Output to Assist with Tracing and Debugging")
          print("------------------------------------------------------------------------------------------------------------------")
          return

      if current_argument in ("-v", "--verbose"):
          Log.basicConfig(format="%(levelname)s: %(message)s", level=Log.INFO)
          Log.info("Verbose Logging Mode...")
      else:
          Log.basicConfig(format="%(levelname)s: %(message)s")

      if current_argument in ("-d", "--debug"):
          Log.basicConfig(format="%(levelname)s: %(message)s", level=Log.DEBUG)
          Log.info("Debug Logging Mode...")
      else:
          Log.basicConfig(format="%(levelname)s: %(message)s")

    await gateway_run()

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))

