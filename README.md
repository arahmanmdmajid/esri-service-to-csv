# esri-service-to-csv

A script that lists the services on an ArcGIS Server site and writes them to a CSV file.

It uses the ArcGIS Server Administrator API (`/arcgis/admin`, port 6443). It does not work with ArcGIS Online.

## What it does

1. Asks for an admin or publisher user name and password.
2. Gets a token from the admin API.
3. Goes through the root folder and every folder except `System`.
4. For each service, reads its properties and its running state.
5. Writes one CSV row per service.

## Requirements

- Python 3 with the `requests` package:

```
pip install -r requirements.txt
```

- An ArcGIS Server site you can reach on port 6443, and an admin or publisher account.

The script runs on Python 3.

## Usage

```
python service_csv.py
```

It asks for:

| Prompt | Example |
|--------|---------|
| User name | `siteadmin` |
| Password | typed without echo |
| Server name | `https://gis.example.com` (include `https://`, no port) |
| Output file | `services.csv` |

## Output

One row per service. Services of these types are included: Geometry, Search, Image, Globe, GP, Geocode, GeoData and Map.

Columns:

`ServiceName, Folder, Type, Status, Min Instances, Max Instances, FeatureService, kml, wms, Max Records, Cluster, Cache Directory, Jobs Directory, Output Directory`

A value that does not apply to a service type is written as `NA`.

## License

[MIT](LICENSE)
