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
import json, sys, time, string, threading, asyncio, os, copy
import logging

# For dumping and Loading Address Space option
from pathlib import Path

# opcua
from asyncua import ua, Server
from asyncua.common.methods import uamethod

# our classes
from classes.config import Config
from classes.dcmtemplate import DcmTemplate
from classes.varianttype import VariantType

class CreateIoTCTemplate():
    
    def __init__(self, Log, InFileName, OutFileName, ModelType):
      self.logger = Log
      self.in_file_name = InFileName
      self.out_file_name = OutFileName
      self.model_type = ModelType
      self.config = []
      self.dcm_template = None
      self.dcm_template_data = []
      self.nodes = []
      self.device_name = None
      self.load_config()
      self.load_dcm_template()
        
    # -------------------------------------------------------------------------------
    #   Function:   create
    #   Usage:      The start function loads configuration and creates the DCM
    # -------------------------------------------------------------------------------
    async def create(self):

      self.prep_dcm()
      
      for node in self.nodes:
        interface = self.create_interface(node["InterfaceInstanceName"], node["InterfacelId"], node["Name"])
        self.logger.info("[INTERFACE] %s" % interface)
        
        for variable in node["Variables"]:
          telemetry = self.create_telemetry(variable["DisplayName"], variable["TelemetryName"], variable["IoTCDataType"])
          self.logger.info("[TELEMETRY] %s" % telemetry)
          interface["schema"]["contents"].append(telemetry)
        
        self.dcm_template_data["implements"].append(interface)
    
      if self.out_file_name == None:
        self.out_file_name = self.config["NameSpace"] + ".json"
      else:
        self.out_file_name = self.out_file_name + ".json"  
      
      self.dcm_template.update_file(self.out_file_name, self.dcm_template_data)
      self.logger.info("[DCM] %s" % self.dcm_template_data)

      return

    # -------------------------------------------------------------------------------
    #   Function:   load_config
    #   Usage:      Loads the configuration from file and setup iterators for
    #               sending telemetry in sequence
    # -------------------------------------------------------------------------------
    def load_config(self):
      
      # Load all the configuration
      config = Config(self.logger)
      self.config = config.data
      self.nodes = self.config["Nodes"]

      return

    # -------------------------------------------------------------------------------
    #   Function:   load_dcm_template
    #   Usage:      Loads the dcm template for generatig a new DCM file
    # -------------------------------------------------------------------------------
    def load_dcm_template(self):

      # Load the template file
      self.dcm_template = DcmTemplate(self.logger)
      self.dcm_template_data = self.dcm_template.data

      return

    def prep_dcm(self):

      self.dcm_template_data["@id"] = self.dcm_template_data["@id"].format(id = self.config["DeviceCapabilityModelId"])           
      self.dcm_template_data["displayName"] = self.dcm_template_data["displayName"].format(displayName = self.config["ServerDiscoveryName"])
      
      self.dcm_template_data["description"] = self.dcm_template_data["description"].format(description = self.config["Description"])

      return


    def create_interface(self, name, id, displayName):
      newInterface = {
        "@type": "InterfaceInstance",
        "name": name, 
        "schema": {
          "@id": id,
          "@type": "Interface",
          "displayName": displayName,
          "contents": [
          ]
        }
      }

      return newInterface 
    
    def create_telemetry(self, displayName, telemetryName, schema):
      newTelemetry = {
        "@type": "Telemetry",
        "displayName": {
          "en": displayName
        },
        "name": telemetryName,
        "schema": schema
      }

      return newTelemetry 
