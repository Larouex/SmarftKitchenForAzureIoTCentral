#!/home/Larouex/Python
# ==================================================================================
#   File:   opcuaserver.py
#   Author: Larry W Jordan Jr (larouex@gmail.com)
#   Use:    Complex OPC/UA Server for testing Azure IoT Central Scenarios that
#           supports multiple OPC-UA servers on an endpoint mapping to the
#           multiple twin apporach or many devices
#
#   Online:   https://github.com/Larouex/SmartKitchenForAzureIoTCentral
#
#   (c) 2021 Larouex Software Design LLC
#   This code is licensed under MIT license (see LICENSE.txt for details)
# ==================================================================================
import  getopt, sys, time, string, threading, asyncio, os
import logging as Log

# our classes
from classes.opcuaserver import OpcUaServer

from classes.config import Config
from classes.varianttype import VariantType

# -------------------------------------------------------------------------------
#   Setup the OPC Server for Multiple Twin and Device Patterns
# -------------------------------------------------------------------------------
async def setup_server(WhatIf, OpcuaServer):

  try:

    Log.info("[SERVER] setup_server...")
    return await OpcuaServer.setup()

  except Exception as ex:
    Log.error("[ERROR] %s" % ex)
    Log.error("[TERMINATING] We encountered an error in [setup_server]" )
    return

# -------------------------------------------------------------------------------
#   Load the Devices previously registered and provisioned and set to Namespaces
#   for Device or Twin when browsing
# -------------------------------------------------------------------------------
async def load_nodes_from_devicecache(WhatIf, OpcuaServer):

  try:

    Log.info("[SERVER] load_nodes_from_devicecache...")
    return await OpcuaServer.load_nodes_from_devicecache()

  except Exception as ex:
    Log.error("[ERROR] %s" % ex)
    Log.error("[TERMINATING] We encountered an error in [load_nodes_from_devicecache]" )
    return

# -------------------------------------------------------------------------------
#   Start the OPC Server for Multiple Twin and Device Patterns
# -------------------------------------------------------------------------------
async def run_server(WhatIf, OpcuaServer):

  try:

    Log.info("[SERVER] start_server...")
    return await OpcuaServer.run()

  except Exception as ex:
    Log.error("[ERROR] %s" % ex)
    Log.error("[TERMINATING] We encountered an error in [start_server]" )

  finally:
    await stop_server(WhatIf, OpcuaServer)

# -------------------------------------------------------------------------------
#   Start the OPC Server for Multiple Twin and Device Patterns
# -------------------------------------------------------------------------------
async def stop_server(WhatIf, OpcuaServer):

  try:

    Log.info("[SERVER] stop_server...")
    await OpcuaServer.stop()
    return

  except Exception as ex:
    Log.error("[ERROR] %s" % ex)
    Log.error("[TERMINATING] We encountered an error in [stop_server]" )


# -------------------------------------------------------------------------------
#   main()
# -------------------------------------------------------------------------------
async def main(argv):

  # parameters
  whatif = False

  # execution state from args
  short_options = "hvdw"
  long_options = ["help", "verbose", "debug", "whatif"]
  full_cmd_arguments = sys.argv
  argument_list = full_cmd_arguments[1:]
  try:
    arguments, values = getopt.getopt(argument_list, short_options, long_options)
  except getopt.error as err:
    print (str(err))

  for current_argument, current_value in arguments:

    if current_argument in ("-h", "--help"):
      print("------------------------------------------------------------------------------------------------------------------------------------------")
      print("HELP for opcuaservers.py")
      print("------------------------------------------------------------------------------------------------------------------------------------------")
      print("")
      print("  BASIC PARAMETERS...")
      print("")
      print("  -h or --help - Print out this Help Information")
      print("  -v or --verbose - Debug Mode with lots of Data will be Output to Assist with Debugging")
      print("  -d or --debug - Debug Mode with lots of DEBUG Data will be Output to Assist with Tracing and Debugging")
      print("  -w or --whatif - Combine with Verbose it will Output the Configuration sans starting the Server")
      print("------------------------------------------------------------------------------------------------------------------------------------------")
      return
      
    if current_argument in ("-v", "--verbose"):
      Log.basicConfig(format="%(levelname)s: %(message)s", level = Log.INFO)
      Log.info("Verbose Logging Mode...")
    else:
      Log.basicConfig(format="%(levelname)s: %(message)s")

    if current_argument in ("-d", "--debug"):
      Log.basicConfig(format="%(levelname)s: %(message)s", level = Log.DEBUG)
      Log.info("Debug Logging Mode...")
    else:
      Log.basicConfig(format="%(levelname)s: %(message)s")

    if current_argument in ("-w", "--whatif"):
      whatif = True
      Log.info("WhatIf Mode...")

  # Configure Server
  opcua_server = OpcUaServer(Log, whatif)
  await setup_server(whatif, opcua_server)
  Log.info("[SERVER] Instance Info (opcua_server): %s" % opcua_server)

  # Load the meta-data and map OPC-UA to IoTC Interfaces
  await load_nodes_from_devicecache(whatif, opcua_server)

  # Start the server loop
  await run_server(whatif, opcua_server)

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))

