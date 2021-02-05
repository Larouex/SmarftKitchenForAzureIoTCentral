# Configuration of the OPC-UA Client - Smart Kitchen OPC-UA Integration with Azure IoT Central
This document outlines the capabilities and configuration for the OPC-UA client.

## Define and Configure Nodes and Variables for our OPC Server.

The defintion of our Nodes and Variables (<i>and Device Interfaces and Telemetry in Azure IoT Central</i>) is contained in the "config.json" file in the root of the project.

Here are the default contents of the file...

````json
{
    "ServerUrlPattern": "opc.tcp://{ip}:{port}/Larouex-Industrial-Manufacturing/Server",
    "ClientUrlPattern": "opc.tcp://localhost:{port}/Larouex-Industrial-Manufacturing/Server",
    "Port": 4840,
    "IPAddress":"0.0.0.0",
    "ApplicationUri": "urn:LarouexIndustrialManufacturing:Server",
    "DeviceCapabilityModelId": "urn:LarouexIndustrialManufacturing:Server:1",
    "ServerDiscoveryName": "Larouex Industrial Manufacturing Server",
    "Description": "Larouex Industrials LLC. Heavy Equipment and Adhesive Manufacturing Device Template.",
    "DeviceName": "larouex-industrial-manufacturing-{id}",
    "NameSpace": "Larouex-Industrial-Manufacturing",
    "CacheAddrSpaceFileName": "cache.opc",
    "ServerFrequencyInSeconds": 10,
    "ClientFrequencyInSeconds": 15,
    "Nodes": [
      {
        "Name": "Ambient",
        "InterfacelId": "urn:larouexindustrialmanufacturing:AmbientInterface:1",
        "InterfaceInstanceName": "AmbientInterface",
        "Variables":[
          {
            "DisplayName": "Temperature",
            "TelemetryName": "temperature",
            "IoTCDataType": "float",
            "RangeValues":[
              72.45,
              73.23,
              85.90,
              91.54,
              73.28,
              67.54,
              69.28,
              81.54,
              73.68,
              81.23
            ]
          },
          {
            "DisplayName": "Humidity",
            "TelemetryName": "humidity",
            "IoTCDataType": "float",
            "RangeValues":[
              68.8, 
              71.0,
              72.3,
              64.1,
              89.2,
              67.3
            ]
          }
        ]
      },
      {
        "Name": "Process",
        "InterfacelId": "urn:larouexindustrialmanufacturing:ProcessInterface:1",
        "InterfaceInstanceName": "ProcessInterface",
        "Variables":[
          {
            "DisplayName": "Temperature",
            "TelemetryName": "temperature",
            "IoTCDataType": "float",
            "RangeValues":[
              112.45,
              113.23,
              115.90,
              121.54,
              143.28,
              151.23
            ]
          },
          {
            "DisplayName": "Pressure",
            "TelemetryName": "pressure",
            "IoTCDataType": "integer",
            "RangeValues":[
              157, 
              151,
              223,
              289,
              190,
              162,
              203,
              209,
              154,
              299
            ]
          },
          {
            "DisplayName": "Mixing Ratio",
            "TelemetryName": "mixratio",
            "IoTCDataType": "float",
            "RangeValues":[
              9.6,
              12.9,
              13.4,
              10.2,
              9.9,
              13.2
            ]
          }
        ]
      }
    ],
    "ProvisioningScope": "NEW",
    "GatewayType": "TRANSPARENT"
}
````

The table below defines and explains the configuration options...
| Item | Explanation |
|---|---|
| ServerUrlPattern | The URL that the OPC Server advertises as its endpoint. The ip and port are assigned in the code. |
| ClientUrlPattern | The URL that the OPC Client Gateway connects to the OPC Server endpoint. The port is assigned in the code. |
| ApplicationUri | The urn for the Application Namespace |
| DeviceCapabilityModelId | This urn is used when generating the Device Template as the DCM @id |
| ServerDiscoveryName | The name that is advertised when discovering the OPC Server |
| Description | This is a description that is added to the Device Template when generating |
| DeviceName | The "Prefix" name used for the OPC Server when provisioned as a Device in Azure IoT Central. You will indicate an enumeration argument when you run the provisioning.py app (i.e. -i "001") [Provisioning our OPC Server as a Device in Azure IoT Central](#provisioning-our-opc-server-as-a-device-in-azure-iot-central) |
| NameSpace | The OPC Server Namespace |
| CacheAddrSpaceFileName | File name for caching the OPC Server Address Space |
| ServerFrequencyInSeconds | Number of seconds to pause between sending value updates to the Variables |
| ClientFrequencyInSeconds | Number of seconds to pause between reading the values from the OPC Server Variables |


Next we have the "Node" array and this is where all of the configuration for your OPC Server and the Telemetry for Azure IoT Central happens. Let's look at the simple scenario of an Ambient Node that publishes two Variables; Temperature and Humidity...

````json
    "Nodes": [
      {
        "Name": "Ambient",
        "InterfacelId": "urn:larouexindustrialmanufacturing:AmbientInterface:1",
        "InterfaceInstanceName": "AmbientInterface",
        "Variables":[
          {
            "DisplayName": "Temperature",
            "TelemetryName": "temperature",
            "IoTCDataType": "float",
            "RangeValues":[
              72.45,
              73.23,
              85.90,
              91.54,
              73.28,
              67.54,
              69.28,
              81.54,
              73.68,
              81.23
            ]
          },
          {
            "DisplayName": "Humidity",
            "TelemetryName": "humidity",
            "IoTCDataType": "float",
            "RangeValues":[
              68.8, 
              71.0,
              72.3,
              64.1,
              89.2,
              67.3
            ]
          }
        ]
      },

````
| Item | Explanation |
|---|---|
| DisplayName | The Name that will be displayed in the OPC Server when browsing and the Display Name in Azure IoT Central.  |
| TelemetryName | The Telemetry name that will be sent in the payload to IoT Central for mapping to the Device Template. |
| IoTCDataType | The datatype as it is selected in Azure IoT Central. |
| RangeValues | This is a Array of values mapping to the datatype that will be sent in sequence when cycling throught the item. |

You can have many Nodes and many Variable in your configuration file. It represents your address space in the OPC Server and the interfaces and telemtery values in Azure Iot Central.
