# ==================================================================================
#   File:   gateway.py
#   Author: Larry W Jordan Jr (larouex@gmail.com)
#   Use:    Gateway acts a Client to the OPC Server and Handles Protocol
#           translation to Azure IoT Central
#
#   Online:   https://github.com/Larouex/SmartKitchenForAzureIoTCentral
#
#   (c) 2021 Larouex Software Design LLC
#   This code is licensed under MIT license (see LICENSE.txt for details)
# ==================================================================================
import json, sys, time, string, threading, asyncio, os, copy, datetime
import logging

# opcua
from asyncua import Client, Node, ua

# uses the Azure IoT Device SDK for Python (Native Python libraries)
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message
from azure.iot.device import MethodResponse

# our classes
from classes.config import Config
from classes.secrets import Secrets
from classes.maptelemetry import MapTelemetry
from classes.varianttype import VariantType
from classes.deviceclient import DeviceClient
from classes.devicescache import DevicesCache

class Gateway():

    def __init__(self, Log):
      self.logger = Log

      self.nodes = []

      # load up configuration and mapping files
      config = Config(self.logger)
      self.config = config.data

      # Device Information
      self.devices_cache = []
      self.load_devicescache()

      # Map Telemetry
      self.map_telemetry = []
      self.load_map_telemetry()
      self.telemetry_msg = {}
      self.telemetry_dict = {}

      # Azure Device List
      self.device_client_dict = {}

    # -------------------------------------------------------------------------------
    #   Function:   run
    #   Usage:      The start function loads configuration and starts the OPC Server
    # -------------------------------------------------------------------------------
    async def run(self):

      # Gateway Loop
      try:

        # configure the endpoint
        url = self.config["ClientUrlPattern"].format(port = self.config["Port"])
        self.logger.info("[GATEWAY] SEEKING ENDPOINT %s" % url)

        async with Client(url=url) as client:

          # Capture the index and list of connections
          index = 0

          # Create the device instances
          for device in self.map_telemetry["Devices"]:
            device_proxy = DeviceClient(self.logger, device["Name"])
            self.logger.info("[GATEWAY] DEVICE %s" % device_proxy)
            await device_proxy.connect()
            self.logger.info("[GATEWAY] CONNECTED %s" % device_proxy)
            self.device_client_dict[device["Name"]] = device_proxy
            #self.device_client.append(device_proxy)
            self.map_telemetry["Devices"][index]["Connected"] = True
            self.map_telemetry["Devices"][index]["ConnectedDateTime"] = str(datetime.datetime.now())
            index = index + 1

          self.update_map_telemetry()

          while True:

            await asyncio.sleep(self.config["ClientFrequencyInSeconds"])

            #for device_name, device_client in enumerate(self.device_client_dict):
            for device in self.map_telemetry["Devices"]:
            #for device in self.device_client:

              for interface in device["Interfaces"]:

                self.logger.info("[GATEWAY] InterfacelId: %s" % interface["InterfacelId"])
                self.logger.info("[GATEWAY] InterfaceInstanceName: %s" % interface["InterfaceInstanceName"])

                self.telemetry_dict = {}

                for variable in interface["Variables"]:

                  read_node = client.get_node(variable["NodeId"])
                  val = await read_node.get_value()
                  log_msg = "[GATEWAY] TELEMETRY: *NAME: {tn} *VALUE: {val} *NODE ID: {ni} *DISPLAY NAME: {dn}"
                  self.logger.info(log_msg.format(tn = variable["TelemetryName"], val = val, ni = variable["NodeId"], dn = variable["DisplayName"]))

                  # Assign variable name and value to dictionary
                  self.telemetry_dict[variable["TelemetryName"]] = val
                  self.logger.info("[GATEWAY] DICTIONARY: %s" % self.telemetry_dict)

                self.logger.info("[GATEWAY] SENDING PAYLOAD IOT CENTRAL")
                device_proxy = self.device_client_dict[device["Name"]]
                await device_proxy.send_telemetry(self.telemetry_dict, interface["InterfacelId"], interface["InterfaceInstanceName"])
                self.logger.info("[GATEWAY] SUCCESS")
                #await device_client.disconnect()
                await asyncio.sleep(3)

      except Exception as ex:
        self.logger.error("[ERROR] %s" % ex)
        self.logger.error("[TERMINATING] We encountered an error in Gateway" )
        return 999

      finally:

        await client.disconnect()

        index = 0
        for device in self.device_client:
          device_proxy = self.device_client_dict[device["Name"]]
          await device_proxy.disconnect()
          self.logger.info("[GATEWAY] DISCONNECTING: %s" % device)
          self.map_telemetry["Devices"][index]["Connected"] = False
          index = index + 1

        self.update_map_telemetry()

        return 0

      return 0

    # -------------------------------------------------------------------------------
    #   Function:   load_devicescache
    #   Usage:      Loads the Devices that have been registered and provisioned.
    #               This file is generated from the as-is state of the system
    #               when the OpcUaServer is started.
    # -------------------------------------------------------------------------------
    def load_devicescache(self):

      devicescache = DevicesCache(self.logger)
      self.devicescache = devicescache.data
      return

    # -------------------------------------------------------------------------------
    #   Function:   load_map_telemetry
    #   Usage:      Loads the Map Telemetry File that Maps Telemtry for Azure
    #               Iot Central to the Node Id's for the Opc Server.
    # -------------------------------------------------------------------------------
    def load_map_telemetry(self):

      # Load all the map
      map_telemetry = MapTelemetry(self.logger)
      map_telemetry.load_file()
      self.map_telemetry = map_telemetry.data
      return

    # -------------------------------------------------------------------------------
    #   Function:   update_map_telemetry
    #   Usage:      Saves the generated Map Telemetry File
    # -------------------------------------------------------------------------------
    def update_map_telemetry(self):
      map_telemetry_file = MapTelemetry(self.logger)
      map_telemetry_file.update_file(self.map_telemetry)
      return
