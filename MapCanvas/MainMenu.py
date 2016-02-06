__author__ = 'Pedro'
# Original sources Copyright (c) 2006 by Tim Sutton
#
# ported to Python by Martin Dobias
#
# licensed under the terms of GNU GPL 2
import sys
import os


qgis_prefix = "C:\\PROGRA~2\\QGISWI~1\\apps\\qgis"
os.environ["QGIS_DEBUG"] = "-1"
sys.path.insert(0, qgis_prefix + "/share/qgis/python")
sys.path.insert(0, 'ui')

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from shapeviewer_gui import Ui_MainWindow
from qgis.core import *
from qgis.gui import *


qgis_prefix = "C:\\PROGRA~2\\QGISWI~1\\apps\\qgis"

class MainWindow(QMainWindow, Ui_MainWindow):

  def __init__(self):
    QMainWindow.__init__(self)

    # required by Qt4 to initialize the UI
    self.setupUi(self)

    # create map canvas
    self.canvas = QgsMapCanvas()
    self.canvas.setCanvasColor(QColor(255,255,255))
    self.canvas.enableAntiAliasing(True)
    self.canvas.useImageToRender(False)
    self.canvas.show()

    # lay our widgets out in the main window
    self.layout = QVBoxLayout(self.frame)
    self.layout.addWidget(self.canvas)

    # create the actions behaviours
    self.connect(self.mpActionAddLayer, SIGNAL("triggered()"), self.addLayer)
    self.connect(self.mpActionZoomIn, SIGNAL("triggered()"), self.zoomIn)
    self.connect(self.mpActionZoomOut, SIGNAL("triggered()"), self.zoomOut)
    self.connect(self.mpActionPan, SIGNAL("triggered()"), self.pan)

    # create a little toolbar
    self.toolbar = self.addToolBar("File");
    self.toolbar.addAction(self.mpActionAddLayer);
    self.toolbar.addAction(self.mpActionZoomIn);
    self.toolbar.addAction(self.mpActionZoomOut);
    self.toolbar.addAction(self.mpActionPan);

    # create the map tools
    self.toolPan = QgsMapToolPan(self.canvas)
    self.toolPan.setAction(self.mpActionPan)
    self.toolZoomIn = QgsMapToolZoom(self.canvas, False) # false = in
    self.toolZoomIn.setAction(self.mpActionZoomIn)
    self.toolZoomOut = QgsMapToolZoom(self.canvas, True) # true = out
    self.toolZoomOut.setAction(self.mpActionZoomOut)

    self.polygon = True
    self.rubberband = QgsRubberBand(self.canvas, self.polygon)


  def zoomIn(self):
    self.canvas.setMapTool(self.toolZoomIn)

  def zoomOut(self):
    self.canvas.setMapTool(self.toolZoomOut)

  def pan(self):
    self.canvas.setMapTool(self.toolPan)

  def addLayer(self):
    """add a (hardcoded) layer and zoom to its extent"""

    info = QtCore.QFileInfo("data/Abarema_jupunba_projection.tif")

    # create layer
    layer = QgsRasterLayer(info.filePath(), info.completeBaseName())

    if not layer.isValid():
      return

    layer.setColorRampingType(QgsRasterLayer.BLUE_GREEN_RED)
    layer.setDrawingStyle(QgsRasterLayer.SINGLE_BAND_PSEUDO_COLOR)

    # add layer to the registry
    QgsMapLayerRegistry.instance().addMapLayer(layer);

    # set extent to the extent of our layer
    self.canvas.setExtent(layer.extent())

    # set the map canvas layer set
    cl = QgsMapCanvasLayer(layer)
    layers = [cl]
    self.canvas.setLayerSet(layers)

  def transform(self, x, y):
    return QgsPoint(self.canvas.getCoordinateTransform().toMapCoordinates(x,y))

  def on_mpToolShowRubberBand_clicked(self):
    self.rubberband.reset(self.polygon)
    self.rubberband.addPoint( self.transform(10,10) )
    self.rubberband.addPoint( self.transform(20,10) )
    self.rubberband.addPoint( self.transform(20,20) )
    self.rubberband.addPoint( self.transform(10,20) )

  def on_mpToolHideRubberBand_clicked(self):
    self.rubberband.reset(self.polygon)


def main(argv):
  # create Qt application
  app = QApplication(sys.argv)

  # initialize qgis libraries
  QgsApplication.setPrefixPath(qgis_prefix, True)
  QgsApplication.initQgis()

  # create main window
  wnd = MainWindow()
  wnd.show()

  # run!
  retval = app.exec_()

  # exit
  QgsApplication.exitQgis()
  sys.exit(retval)


if __name__ == "__main__":
  main(sys.argv)
