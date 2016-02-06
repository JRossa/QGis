__author__ = 'Pedro'

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import QgsApplication, QgsVectorLayer, QgsMapLayerRegistry, QgsProviderRegistry
from qgis.gui import QgsMapCanvas, QgsMapCanvasLayer
import sys
import os
import qgis.utils


def init():
  a = QgsApplication(sys.argv, True)
  a.setApplicationName("Teste PyCharm")
  QgsApplication.setPrefixPath("C:\\PROGRA~2\\QGISWI~1\\apps\\qgis", True)
  print QgsApplication.showSettings()


  QgsApplication.initQgis()
#  providers = QgsProviderRegistry.instance().providerList()
#  for provider in providers:
#    print provider
  return a


#def open_File(self):
#  file = QFileDialog.getOpenFileName(self, "Open File", ".", "Shapefiles (*.shp)")
#  fileInfo = QFileInfo( file )


def show_canvas(app):
  canvas = QgsMapCanvas()

  layer = QgsVectorLayer("D:\\Software\\QGis\\StatPlanet_France\\map\\map.shp", "teste" , "ogr")

  if not layer.isValid():
    raise IOError, "Failed to open the layer"
  else:
   # add layer to the registry
    QgsMapLayerRegistry.instance().addMapLayer(layer)

# set extent to the extent of our layer
    canvas.setExtent(layer.extent())

# set the map canvas layer set
    canvas.setLayerSet([QgsMapCanvasLayer(layer)])

    canvas.show()
    app.exec_()

    #print qgis.utils.iface.activeLayer()

app = init()
show_canvas(app)

