# Migración a QGIS 4 (Qt6) y actualización a OpenPlanetaryMap

Plugin `opmtileloader` v1.0. Rama `migracion-qgis4-opm`. Entorno de pruebas: QGIS 4.2.3 (macOS, Apple Silicon), Python 3.12.11, PyQt6 6.11.0 / Qt 6.11.1. Fecha de verificación: 2026-10-01.

## Decisiones
- Solo QGIS >= 4.0 (`qgisMinimumVersion=4.0`, sin `qgisMaximumVersion`, sin `supportsQt6`). Versión 0.1 → **1.0** (sin changelog en metadata.txt).
- Se borran `resources.qrc` y `resources.py` (pyrcc5); el icono se carga por ruta relativa a `__file__`.
- URLs y nombres centralizados en `basemaps.py` (dict `BASEMAPS`), sustituyendo el `if/elif` de `loadtile()`.
- Mercurio: nueva sección «Mercury» en el diálogo (el diálogo es vertical: Luna / Mercury / Marte), con «(DRAFT)» en el nombre y aviso en el tooltip.
- No se descargan miniaturas de OPM (la web no declara licencia ni atribución; ver pendientes). No hay iconos por mapa en el plugin, así que no se creó icono para Mercurio.
- Pie del diálogo: un único enlace «About» → `https://github.com/robermaps/opmtileloader` (nuevo repositorio). Se eliminaron los enlaces «Provided by OpenPlanetary».
- la pestaña Basemaps usa el mismo árbol por cuerpo (Mars/Mercury/The Moon) + «Add to QGIS» que Datasets; icono nuevo (luna con cráteres, diseño propio, sin material de terceros).

## Cambios automáticos (`pyqt5_to_pyqt6.py --qgis3-incompatible-changes`, commit `7621ed0`)
8 cambios en 3 ficheros: 2 enums QGIS (`Qgis.MessageLevel.*`), 4 enums Qt con ámbito, 1 `exec_()`→`exec()`, 1 `PyQt5`→`qgis.PyQt` (en `resources.py`, luego borrado). Requiere `tokenize-rt` (se instaló con `pip --target` en un directorio temporal).

## Cambios manuales
- `QAction` → `qgis.PyQt.QtGui`; eliminado `from .resources import *`.
- Tests: `QDialogButtonBox`/`QDialog` desde `QtWidgets`; `test_resources.py` usa la ruta del icono.
- `Makefile`, `pb_tool.cfg`: eliminadas las reglas/ficheros de `pyrcc5`; `scripts/update-strings.sh`: `pylupdate6 --no-obsolete`; nota de `lrelease` Qt6.
- `QSettings().value('locale/userLocale', 'en')`: antes fallaba con `None` en un perfil limpio.
- `README.txt/html`: líneas de `pyrcc5` marcadas como obsoletas.
- Traducciones: solo existe `i18n/af.ts` de plantilla (sin cadenas del plugin); no se añadieron `.ts`. Nueva cadena traducible: «Draft / preliminary basemap». Instalar herramientas Qt6: `brew install qt` (lrelease en `$(brew --prefix qt)/share/qt/libexec`) y `pip install PyQt6` (pylupdate6) en un entorno propio.

## Tabla de conciliación OPM final
Todas las URLs XYZ coinciden con las fichas (salvo el `{-y}`, ver riesgos).

| Mapa (H1) | Ficha | HTTP z=0 y z=3 | Estado |
|---|---|---|---|
| OPM Mars Basemap v0.2 | /basemaps/mars/opm-mars-basemap-v0-2/ | 200 image/png | igual |
| Mars Colour MOLA Elevation | …/opm-mars-colour-mola-elevation/ | 200 image/png | igual (nombre ahora con «Elevation» como el H1) |
| Mars Shaded Grayscale MOLA Elevation | …/opm-mars-shaded-grayscale-mola-elevation/ | 200 image/png | igual |
| Mars Hillshade | …/opm-mars-hillshade/ | 200 image/png | igual |
| Mars Shaded Colour MOLA Elevation | …/opm-mars-shaded-colour-mola-elevation/ | 200 image/png | igual |
| Mars Shaded Surface Texture | …/opm-mars-colour-celestia/ | 200 image/png | igual |
| Mars Viking MDIM2.1 | …/opm-mars-viking-mdim21/ | 200 image/png | nombre cambiado («VIKING MDIM 2.1») |
| OPM Mercury Basemap v0.1 (DRAFT) | /basemaps/mercury/opm-mercury-basemap-v0-1-draft/ | 200 image/png | **nuevo** |
| OPM Moon Basemap v0.1 | /basemaps/moon/opm-moon-basemap-v0-1/ | 200 image/png | igual |
| Moon Hillshaded Albedo | …/opm-moon-hillshaded-albedo/ | 200 image/png | igual |

Todas las fichas devuelven 200. No hay mapas retirados ni mapas nuevos aparte de Mercurio. Enlaces antiguos: `https://www.openplanetary.org/opm` → 404 (sustituido) y `https://roberer.github.io` → 404 (sustituido).

## Pendientes y riesgos
1. **`{-y}` (TMS):** OPM publica `{y}` para los 7 mapas en S3, pero esas teselas son TMS (comprobado visualmente: z=1/x=0/y=0 de `mola-gray` es el hemisferio sur, el del basemap CARTO el norte). Se mantiene `{-y}`; no «corregir» a `{y}`. Mercurio usa `{y}`.
2. **Licencia/atribución:** la web de OPM no declara licencia (`/license` 404, el repositorio `opm-website` no tiene licencia). Por eso no se descargaron miniaturas. Conviene contactar con OPM antes de redistribuir imágenes. La sección «Data Layers» de las fichas se renderiza con JS y no se pudo leer.
3. **SRC:** teselas planetarias cargadas como EPSG:3857 terrestre (comportamiento original, sin tocar).
4. Mezcla `http://` (S3 `whereonmars`) y `https://`: funciona, pero es frágil.
5. Servicios de terceros (CARTO, S3) sin garantía de continuidad: OPM busca un socio institucional para mantener los mapas.
6. Deuda técnica: el diálogo usa posiciones absolutas (sin layouts); tests de plantilla Plugin Builder de poco valor; `plugin_upload.py` y `help/` son boilerplate; `from qgis.utils import iface` a nivel de módulo (es `None` fuera de QGIS).
7. `ruff`/`pyflakes` no están instalados; la validación estática fue `compileall` + grep de patrones residuales.

## Cómo probar
```sh
PY=/Applications/QGIS-final-4_2_3.app/Contents/MacOS/python
$PY -m compileall -q .
python3 scripts/check_tiles.py .    # una tesela z=0 y z=3 por mapa + ficha
# plugin enlazado en el perfil QGIS4:
ls -l ~/Library/Application\ Support/QGIS/QGIS4/profiles/default/python/plugins/opmtileloader
```
Smoke test (offscreen, `qgis.testing.start_app()`): `classFactory`, `initGui()`/`unload()`, diálogo con los 10 botones, `run()` + clic en botones, y los 10 `QgsRasterLayer.isValid()` → todo OK en QGIS 4.2.3.

### Comprobaciones manuales en QGIS 4
1. Plugins → Administrar → activar «OpenPlanetaryMap Tile Loader» (sin errores en el log).
2. Abrir el diálogo: secciones Luna, Mercury, Marte; tooltips con enlace a la ficha (Mercurio con aviso de borrador).
3. Cargar visualmente, en este orden: **Mercury Basemap v0.1 (DRAFT)**, Moon Basemap, Moon Hillshaded Albedo, Mars Basemap v0.2, Mars Colour MOLA, Shaded Grayscale MOLA, Hillshade, Shaded Colour MOLA, Shaded Surface Texture, Viking MDIM2.1. Comprobar que el norte queda arriba en los mapas `{-y}`.
4. Pulsar los dos enlaces del pie del diálogo.
5. Desactivar el plugin: desaparece el icono y el menú.

## Datasets
Nueva pestaña **Datasets** (el diálogo pasa a `QTabWidget`: Basemaps / Datasets) con los 8 datasets de https://openplanetarymap.org/datasets/ agrupados en Marte y Luna (`datasets.py`).
- **Fuente:** API SQL de CARTO `https://opmbuilder.carto.com/api/v2/sql` (formato GeoJSON, EPSG:4326). Se descarga a un `.geojson` temporal y se carga con OGR; el usuario exporta la capa si quiere conservarla. Estilo por defecto de QGIS.
- **Grandes:** si la tabla tiene más de 20 000 filas se pregunta «Current map extent» / «Whole dataset» / Cancelar. La extensión se transforma a EPSG:4326 y filtra con `the_geom && ST_MakeEnvelope(...)` (instantánea, no se actualiza al mover el mapa). Descarga paginada de 20 000 filas con barra de progreso cancelable.
- **Tamaños (filas):** Mars nomenclature 1 652; Mars contours lines 203 341 (~149 MB en GeoJSON completo); Mars contours polygons 87 945; Mars TES albedo 246; Moon nomenclature 8 790; Moon contours 235 799 (~224 MB); Luna sites 8; Apollo sites 6.
- **Hallazgos del servidor OPM/CARTO:**
  1. Un `select *` sin paginar se trunca en silencio (Mars contours polygons devolvía 284 de 87 945 filas).
  2. `select *` incluye `the_geom_webmercator`, que duplica el tamaño de la fila; una fila supera el límite de ~11 MB («Row too large»). Se excluye esa columna (no se pierden datos) y se verificó 87 945/87 945 filas.
  3. La web llama «polygons» a los contornos de la Luna (`opm_301_moon_contours_polygons_1km_interval`) pero la geometría es MULTILINESTRING; se mantiene el nombre de la web.
  4. El driver `Carto:` de GDAL funciona en `ogrinfo` pero el proveedor OGR de QGIS lo rechaza, por eso se usa GeoJSON.
- **Riesgos:** dependencia de `opmbuilder.carto.com` (sin garantía de continuidad); las coordenadas son lon/lat planetarias etiquetadas EPSG:4326 (terrestre), igual que los basemaps tratados como 3857; descarga síncrona (la UI queda bloqueada, con `processEvents`, durante la descarga); las capas descargadas viven en la carpeta temporal del sistema.
- **Probado (QGIS 4.2.3 offscreen):** pestañas y árbol, Apollo (6), Luna (8) y Albedo (246) completos con `isValid()`, paginación completa de Mars contours polygons (87 945/87 945, ~24 s) y flujo «extensión» sobre Mars contours lines (157 entidades en 0–5°). No probados: descarga completa de contornos de la Luna/Marte (líneas) ni nomenclatura de la Luna.
- **Comprobación manual adicional:** pestaña Datasets → añadir Luna Sites y Apollo Sites (puntos), Mars Nomenclature, y un dataset grande con «Current map extent»; comprobar que se alinean con el basemap correspondiente.
