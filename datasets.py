"""OpenPlanetaryMap vector datasets.

Catalogue: https://openplanetarymap.org/datasets/
The data lives in CARTO tables served by the SQL API as GeoJSON (EPSG:4326
planetary lon/lat). Big tables are downloaded in pages: the server silently
truncates large unpaged exports (and rejects rows over ~11 MB).
"""
import json
import os
import tempfile
from urllib.parse import urlencode

from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtNetwork import QNetworkRequest
from qgis.core import QgsBlockingNetworkRequest

DATASETS_URL = 'https://openplanetarymap.org/datasets/'
SQL_URL = 'https://opmbuilder.carto.com/api/v2/sql'
CARTO_TABLE_URL = 'https://openplanetary.carto.com/u/opmbuilder/dataset/'

PAGE_SIZE = 20000
# Above this number of rows the user is asked whether to load the whole table
LARGE_ROWS = 20000

BODIES = [('mars', 'Mars'), ('moon', 'The Moon')]

# Names follow the OPM datasets page. Note: the page calls the Moon contours
# "polygons" in the table name but the geometry is MULTILINESTRING.
DATASETS = {
    'mars_nomenclature': {
        'name': 'Mars Nomenclature (polygons)',
        'body': 'mars',
        'table': 'opm_499_mars_nomenclature_polygons',
    },
    'mars_contours_lines': {
        'name': 'Mars Topography Contours (lines)',
        'body': 'mars',
        'table': 'opm_499_mars_contours_200m_lines',
    },
    'mars_contours_polygons': {
        'name': 'Mars Topography Contours (polygons)',
        'body': 'mars',
        'table': 'opm_499_mars_contours_200m_polygons',
    },
    'mars_albedo': {
        'name': 'Mars TES Albedo (7 classes)',
        'body': 'mars',
        'table': 'opm_499_mars_albedo_tes_7classes',
    },
    'moon_nomenclature': {
        'name': 'Moon Nomenclature (polygons)',
        'body': 'moon',
        'table': 'opm_301_moon_nomenclature_polygons',
    },
    'moon_contours': {
        'name': 'Moon Topography Contours (1km interval)',
        'body': 'moon',
        'table': 'opm_301_moon_contours_polygons_1km_interval',
    },
    'moon_luna_sites': {
        'name': 'Moon Luna Sites',
        'body': 'moon',
        'table': 'opm_301_luna_sites',
    },
    'moon_apollo_sites': {
        'name': 'Moon Apollo Sites',
        'body': 'moon',
        'table': 'opm_301_apollo_sites',
    },
}


class DatasetError(Exception):
    """Raised when a dataset cannot be downloaded."""


def info_url(key):
    """Return the CARTO page of the dataset."""
    return CARTO_TABLE_URL + DATASETS[key]['table']


def _where(bbox):
    if bbox is None:
        return ''
    return ' where the_geom && ST_MakeEnvelope({},{},{},{},4326)'.format(*bbox)


def _request(sql, fmt=None):
    params = {'q': sql}
    if fmt:
        params['format'] = fmt
    request = QgsBlockingNetworkRequest()
    error = request.get(QNetworkRequest(QUrl(SQL_URL + '?' + urlencode(params))))
    if error != QgsBlockingNetworkRequest.ErrorCode.NoError:
        raise DatasetError(request.errorMessage())
    return json.loads(bytes(request.reply().content()).decode('utf-8'))


def _columns(table):
    """Columns to export. the_geom_webmercator duplicates the geometry and makes rows too large for the server."""
    fields = _request('select * from {} limit 0'.format(table))['fields']
    return ','.join('"{}"'.format(c) for c in fields if c != 'the_geom_webmercator')


def count_rows(key, bbox=None):
    """Number of rows of the dataset, optionally inside bbox (xmin, ymin, xmax, ymax, EPSG:4326)."""
    table = DATASETS[key]['table']
    return int(_request('select count(*) n from {}{}'.format(table, _where(bbox)))['rows'][0]['n'])


def download(key, bbox=None, total=None, progress=None):
    """Download the dataset as a GeoJSON file in a temporary folder and return its path.

    :param progress: optional callable(done, total) returning False to cancel.
    """
    table = DATASETS[key]['table']
    if total is None:
        total = count_rows(key, bbox)
    columns = _columns(table)
    path = os.path.join(tempfile.mkdtemp(prefix='optileloader_'), table + '.geojson')
    done = 0
    with open(path, 'w', encoding='utf-8') as out:
        out.write('{"type":"FeatureCollection","features":[')
        first = True
        while done < total:
            sql = 'select {} from {}{} order by cartodb_id limit {} offset {}'.format(
                columns, table, _where(bbox), PAGE_SIZE, done)
            features = _request(sql, 'geojson')['features']
            if not features:
                break
            for feature in features:
                out.write(('' if first else ',') + json.dumps(feature))
                first = False
            done += len(features)
            if progress is not None and not progress(done, total):
                raise DatasetError('cancelled')
        out.write(']}')
    return path
