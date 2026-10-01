# -*- coding: utf-8 -*-
"""
/***************************************************************************
 OPTileLoader
                                 A QGIS plugin
 Load Mars, Mercury and The Moon basemaps and datasets
                             -------------------
        begin                : 2026-10-01
        copyright            : (C) 2026 by Robermaps
        email                : robermaps@outlook.es
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load OPTileLoader class from file OPTileLoader.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .optileloader import OPTileLoader
    return OPTileLoader(iface)
