# Cold Table - Smart Kitchen OPC-UA Integration with Azure IoT Central
![alt text](../Assets/commercial-cold-table.png "Cold Table")

This is a detailed overview of the following...

* <b>The Configuration for the OPC-UA Server</b> We will show the details of the configuration for emulation of the Server, Nodes and Variables for the OPC-UA Server.
* <b>Telemetry</b> The Telemetry that we are emulating.
* <b>Plug and Play Model</b> The Azure Plug and Play Model we are using with IoT Central.

## Cold Table

    Measurements
    ---------------------------------
      Temperature
      Compressor Health

    Baselines and Trends
    ---------------------------------
      Ideal Temperature = 39 F
      Compressor Health > 98

## Cold Table Telemetry Configuration
The telemetry used by the Telemetry Server and the OPC-UA Server components read from the config.json the applicances that are enumerated under the "Nodes" item.

````json
  {
    "Name": "ColdTable",
    "InterfacelId": "urn:larouexsmartkitchen:ColdTableInterface:1",
    "InterfaceInstanceName": "ColdTableInterface",
    "Variables": [
      {
        "DisplayName": "Cold Table Temperature",
        "TelemetryName": "cold_table_temperature",
        "IoTCDataType": "float",
        "Frequency": "Ring3",
        "OnlyOnValueChange": false,
        "RangeValues": [
          39.45,
          39.23,
          39.90,
          41.54,
          42.28,
          43.23
        ]
      },
      {
        "DisplayName": "Cold Table Compressor Health",
        "TelemetryName": "cold_table_compressor_health",
        "IoTCDataType": "integer",
        "Frequency": "Ring2",
        "OnlyOnValueChange": false,
        "RangeValues": [
          99,
          98,
          97,
          96,
          95
        ]
      }
    ]
  }
````