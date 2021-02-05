# ==================================================================================
#   File:   createiotctemplate.py
#   Author: Larry W Jordan Jr (larouex@gmail.com)
#   Use:    Loads the Config and Generates a Device Template for use with Azure
#           IoT Central
#
#   Online: https://github.com/Larouex/SmarftKitchenForAzureIoTCentral
#
#   (c) 2021 Larouex Software Design LLC
#   This code is licensed under MIT license (see LICENSE.txt for details)    
# ==================================================================================
import getopt, sys, time, string, threading, asyncio, os
import logging as Log

# our classes
from classes.createiotctemplate import CreateIoTCTemplate
from classes.config import Config
from classes.varianttype import VariantType

# -------------------------------------------------------------------------------
#   Create the Template
# -------------------------------------------------------------------------------
async def create_template(infilename, outfilename, model_type):

  create_iotc_template = CreateIoTCTemplate(Log, infilename, outfilename, model_type)
  await create_iotc_template.create()

  return

async def main(argv):

    infilename = None
    outfilename = None
    model_type = "twin"

    # execution state from args
    short_options = "hvdi:o:m:"
    long_options = ["help", "verbose", "debug", "infilename=", "outfilename=", "modeltype="]
    full_cmd_arguments = sys.argv
    argument_list = full_cmd_arguments[1:]

    try:
      arguments, values = getopt.getopt(argument_list, short_options, long_options)
    except getopt.error as err:
      print (str(err))
    
    for current_argument, current_value in arguments:
      
      if current_argument in ("-h", "--help"):
        print("")
        print("------------------------------------------------------------------------------------------------------------------------------------------")
        print("HELP for createiotctemplate.py")
        print("------------------------------------------------------------------------------------------------------------------------------------------")
        print("")
        print("  BASIC PARAMETERS...")
        print("")
        print("  -h or --help - Print out this Help Information.")
        print("  -v or --verbose - Verbose Mode with lots of INFO will be Output to Assist with Tracing and Debugging.")
        print("  -d or --debug - Debug Mode with lots of DEBUG Data will be Output to Assist with Tracing and Debugging.")
        print("")
        print("  OPTIONAL PARAMETERS...")
        print("")
        print("    -i or --infilename - Name of the configuration file to process for generation of the DTDL mapping.")
        print("       USAGE: -i config_smartkitchen.json")
        print("       DEFAULT: config.json")
        print("")
        print("    -o or --outfilename - OPTIONAL: PREFIX Name of the DCM File that will be output into ./DeviceTemplates Folder.")
        print("       USAGE: -o filename_prefix")
        print("       DEFAULT: It will use the NameSpace value specified in the config.json or the --infilename")
        print("")
        print("    -m or --modeltype - OPTIONAL: Create the DCM as a collective Twin Pattern or by Device Pattern.")
        print("       USAGE: -m device")
        print("       DEFAULT: twin")
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

      if current_argument in ("-i", "--infilename"):
        infilename = current_value
        Log.info("In File Name is Specified...")
        
      if current_argument in ("-o", "--outfilename"):
        outfilename = current_value
        Log.info("Out File Name is Specified...")

      if current_argument in ("-m", "--modeltype"):
        model_type = current_value
        Log.info("Model Type is Specified as...{model_type}".format(model_type = model_type))

        if (model_type != "twin" and model_type != "device"):
          print("[ERROR] -m --modeltype must be specified as either twin | device")
          return
        

    # Create the Template
    await create_template(infilename, outfilename, model_type)

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
