# OpenPlanetary Tile Loader for QGIS

<img src="https://robermaps.github.io/img/mars-moon.jpg" width=60% height=60% >

A plugin to easily load basemaps of Mars, Mercury and The Moon directly to your QGIS project. 

Data is provided by <a href="https://openplanetarymap.org/basemaps/">OpenPlanetaryMap</a>

📥 You can download the plugin directly inside QGIS or <a href="https://plugins.qgis.org/plugins/opmtileloader/">from the official QGIS Python Plugins Repository</a> 

Just press a button and the tile will be loaded to your QGIS project

The **Datasets** tab adds the OpenPlanetaryMap vector datasets (<a href="https://openplanetarymap.org/datasets/">list</a>): Mars and Moon nomenclature, topographic contours, Mars TES albedo and Luna/Apollo sites. Large datasets (contours, Moon nomenclature) can be loaded for the current map extent only. Datasets are downloaded as GeoJSON (EPSG:4326, planetary lon/lat) into a temporary folder: export the layer to keep it.

🗺️ <a href="https://robermaps.github.io/maps/mars-moon-explorer">Explore all basemaps</a> before download.

## Notes
* <b>Basemaps are Web Mercator (EPSG:3857) tiles; datasets are loaded as GeoJSON in planetary lon/lat (labelled EPSG:4326)</b>
* This is not an official tool from OpenPlanetary
* Requires QGIS 4.0 or later (Qt6).
* OPM Mercury Basemap v0.1 is a draft / preliminary map
* Thanks to <a href="https://plugins.qgis.org/plugins/pluginbuilder3/">Plugin Builder 3</a> and <a href="https://plugins.qgis.org/plugins/plugin_reloader/">Plugin reloader</a>

