#!/home/Larouex/Python
# ==================================================================================
#   File:   telemetryserver.py
#   Author: Larry W Jordan Jr (larouex@gmail.com)
#   Use:    This module instantiates the class TelemetryServer that reads in the
#           IoTCentralPatterns from config.json and emits a pub/sub model for a
#           device to emulate values that map to the model associated with the device.
#
#   Online:   https://github.com/Larouex/device-twin-diff-viewer
#
#   (c) 2021 Larouex Software Design LLC
#   This code is licensed under MIT license (see LICENSE.txt for details)
# ==================================================================================
import  getopt, sys, time, string, threading, asyncio, os, kwargs
import logging as Log

# PubSub module
from pubsub import pub

# our classes
from classes.telemetryserver import TelemetryServer
from classes.config import Config
from classes.maptelemetry import MapTelemetry
from classes.listener import Listener

# -------------------------------------------------------------------------------
#   Setup the Telemetry Server for the Device Patterns
# -------------------------------------------------------------------------------
async def setup_server(TelemetryServer):

  try:

    Log.info("[SERVER] setup_server...")
    return await TelemetryServer.setup()

  except Exception as ex:
    Log.error("[ERROR] %s" % ex)
    Log.error("[TERMINATING] We encountered an error in [setup_server]" )

    return


# -------------------------------------------------------------------------------
#   Start the OPC Server for Multiple Twin and Device Patterns
# -------------------------------------------------------------------------------
async def run_server(TelemetryServer):

  try:

    config = Config(Log)
    config_data = config.data

    # Logging Mapper
    data = [x for x in config_data["ClassLoggingMaps"] if x["Name"] == "TelemetryServer"]
    class_name_map = data[0]["LoggingId"]

    # Grab the Telemetry Enumeration (populated in TelemetryServer.setup())
    map_telemetry = TelemetryServer.get_map_telemetry()

    # Subscribe to the Telemetry Server Publication of Telemetry Data
    listener = Listener()
    pub.subscribe(listener, pub.ALL_TOPICS)

    # We run the Telemetry Server on its own here...
    while True:

      for telemetry in map_telemetry:
        Log.info("[%s LOOP] NAME: %s" % (class_name_map, telemetry["Name"]))
        Log.info("[%s LOOP] INTERFACE: %s" % (class_name_map, telemetry["InterfacelId"]))

        await TelemetryServer.run(telemetry)

        payload = listener.read_payload()
        map_telemetry_interfaces = TelemetryServer.create_map_telemetry_root(payload["Name"], payload["InterfacelId"], payload["InterfaceInstanceName"])
        map_telemetry_interfaces["Variables"] = payload["Payload"]
        Log.info("[%s LOOP] PUBLISHED: %s" % (class_name_map, map_telemetry_interfaces))

      Log.info("[%s LOOP] WAITING: %s" % (class_name_map, config_data["ServerFrequencyInSeconds"]))
      await asyncio.sleep(config_data["ServerFrequencyInSeconds"])

  except Exception as ex:
    Log.error("[ERROR] %s" % ex)
    Log.error("[TERMINATING] We encountered an error in [run_server]" )

  finally:
    await stop_server(TelemetryServer)

# -------------------------------------------------------------------------------
#   Start the OPC Server for Multiple Twin and Device Patterns
# -------------------------------------------------------------------------------
async def stop_server(TelemetryServer):

  try:

    Log.info("[SERVER] stop_server...")
    await TelemetryServer.stop()
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
      print("------------------------------------------------------------------------------------------------------------------------------------------")
      print("HELP for telemetryservers.py")
      print("------------------------------------------------------------------------------------------------------------------------------------------")
      print("")
      print("  BASIC PARAMETERS...")
      print("")
      print("  -h or --help - Print out this Help Information")
      print("  -v or --verbose - Debug Mode with lots of Data will be Output to Assist with Debugging")
      print("  -d or --debug - Debug Mode with lots of DEBUG Data will be Output to Assist with Tracing and Debugging")
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

  # Configure Server
  telemetry_server = TelemetryServer(Log)
  await setup_server(telemetry_server)
  Log.info("[SERVER] Instance Info (telemetry_server): %s" % telemetry_server)

  # Start the server loop
  await run_server(telemetry_server)

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))

