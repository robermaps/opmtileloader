"""OpenPlanetaryMap basemap definitions (single source of truth).

Catalogue: https://openplanetarymap.org/basemaps/
Tile URLs keep the placeholders URL-encoded ({z}=%7Bz%7D, {-y}=%7B-y%7D) as
required by the QGIS XYZ provider; {-y} marks TMS (flipped y) tile sets.
"""

BASE_URL = 'https://openplanetarymap.org/basemaps/'

BODIES = [('mars', 'Mars'), ('mercury', 'Mercury'), ('moon', 'The Moon')]

_CARTO = 'https://cartocdn-gusc.global.ssl.fastly.net/opmbuilder/api/v1/map/named/'
_WOM = 'http://s3-eu-west-1.amazonaws.com/whereonmars.cartodb.net/'
_XYZ = '/%7Bz%7D/%7Bx%7D/%7By%7D.png'
_TMS = '/%7Bz%7D/%7Bx%7D/%7B-y%7D.png'

BASEMAPS = {
    'basemap': {
        'name': 'OPM Mars Basemap v0.2',
        'body': 'mars',
        'slug': 'opm-mars-basemap-v0-2',
        'url': _CARTO + 'opm-mars-basemap-v0-2/all' + _XYZ,
    },
    'colourmola': {
        'name': 'Mars Colour MOLA Elevation',
        'body': 'mars',
        'slug': 'opm-mars-colour-mola-elevation',
        'url': _WOM + 'mola_color-noshade_global' + _TMS,
    },
    'graymola': {
        'name': 'Mars Shaded Grayscale MOLA Elevation',
        'body': 'mars',
        'slug': 'opm-mars-shaded-grayscale-mola-elevation',
        'url': _WOM + 'mola-gray' + _TMS,
    },
    'hillshade': {
        'name': 'Mars Hillshade',
        'body': 'mars',
        'slug': 'opm-mars-hillshade',
        'url': 'https://s3.us-east-2.amazonaws.com/opmmarstiles/hillshade-tiles' + _TMS,
    },
    'shadedmola': {
        'name': 'Mars Shaded Colour MOLA Elevation',
        'body': 'mars',
        'slug': 'opm-mars-shaded-colour-mola-elevation',
        'url': _WOM + 'mola-color' + _TMS,
    },
    'surfacetexture': {
        'name': 'Mars Shaded Surface Texture',
        'body': 'mars',
        'slug': 'opm-mars-colour-celestia',
        'url': _WOM + 'celestia_mars-shaded-16k_global' + _TMS,
    },
    'viking': {
        'name': 'Mars Viking MDIM2.1',
        'body': 'mars',
        'slug': 'opm-mars-viking-mdim21',
        'url': _WOM + 'viking_mdim21_global' + _TMS,
    },
    'mercurybase': {
        'name': 'OPM Mercury Basemap v0.1 (DRAFT)',
        'body': 'mercury',
        'slug': 'opm-mercury-basemap-v0-1-draft',
        # The named map in the tile URL has no "-draft" suffix (checked on the OPM page).
        'url': _CARTO + 'opm-mercury-basemap-v0-1/all' + _XYZ,
        'draft': True,
    },
    'moonbase': {
        'name': 'OPM Moon Basemap v0.1',
        'body': 'moon',
        'slug': 'opm-moon-basemap-v0-1',
        'url': _CARTO + 'opm-moon-basemap-v0-1/all' + _XYZ,
    },
    'moonhillsh': {
        'name': 'Moon Hillshaded Albedo',
        'body': 'moon',
        'slug': 'opm-moon-hillshaded-albedo',
        'url': 'https://s3.amazonaws.com/opmbuilder/301_moon/tiles/w/hillshaded-albedo' + _TMS,
    },
}


def info_url(key):
    """Return the OpenPlanetaryMap page of the basemap."""
    m = BASEMAPS[key]
    return '{}{}/{}/'.format(BASE_URL, m['body'], m['slug'])
