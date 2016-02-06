__author__ = 'Pedro'

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
import sys
import os

# Import our GUI
from shapeviewer_gui import Ui_MainWindow

# Environment variable QGISHOME must be set to the install directory
# before running the application
qgis_prefix = os.getenv("QGISHOME")


class ShapeViewer(QMainWindow, Ui_MainWindow):
  def __init__(self):
    QMainWindow.__init__(self)

    # Required by Qt4 to initialize the UI.
    self.setupUi(self)
    self.layers = []

    # Set the title for the app.
    self.setWindowTitle("ShapeViewer")

    # Create the map canvas.
    self.canvas = QgsMapCanvas()
    self.canvas.useImageToRender(False)

    # Set the background color to white.
    self.canvas.setCanvasColor(Qt.white)
    self.canvas.enableAntiAliasing(True)
    self.canvas.show()

    # Lay our widgets out in the main window using a vertical box layout.
    self.layout = QVBoxLayout(self.frame)
    self.layout.addWidget(self.canvas)

    actionZoomIn = QAction(QString("Zoom in"), self)
    actionZoomOut = QAction(QString("Zoom out"), self)
    actionPan = QAction(QString("Pan"), self)

    actionZoomIn.setCheckable(True)
    actionZoomOut.setCheckable(True)
    actionPan.setCheckable(True)

    self.toolbar = self.addToolBar("Canvas actions")
    self.toolbar.addAction(actionZoomIn)
    self.toolbar.addAction(actionZoomOut)
    self.toolbar.addAction(actionPan)

    # Create the map tools.
    self.toolPan = QgsMapToolPan(self.canvas)
    self.toolPan.setAction(actionPan)
    self.toolZoomIn = QgsMapToolZoom(self.canvas, False) # false = in
    self.toolZoomIn.setAction(actionZoomIn)
    self.toolZoomOut = QgsMapToolZoom(self.canvas, True) # true = out
    self.toolZoomOut.setAction(actionZoomOut)

    self.pan()


    # Layout is set - open a layer.
    # Add an OGR layer to the map.
    self.Add_Map_Layer("")

    self.connect(actionZoomIn, SIGNAL("triggered()"), self.zoomIn)
    self.connect(actionZoomOut, SIGNAL("triggered()"), self.zoomOut)
    self.connect(actionPan, SIGNAL("triggered()"), self.pan)

  def zoomIn(self):
    self.canvas.setMapTool(self.toolZoomIn)

  def zoomOut(self):
    self.canvas.setMapTool(self.toolZoomOut)

  def pan(self):
    self.canvas.setMapTool(self.toolPan)

  def Add_Map_Layer(self, mapFileName):
    # Add the layer

    # layout is set - open a layer
    # Add an OGR layer to the map
    file = QFileDialog.getOpenFileName(self,"Open Shapefile", ".", "Shapefiles (*.shp)")
    fileInfo = QFileInfo(file)

    # Add the layer
    layer = QgsVectorLayer(file, fileInfo.fileName(), "ogr")

    if not layer.isValid():
      print "Layer failed to load! :("
      return

    # Add layer to the registry
    QgsMapLayerRegistry.instance().addMapLayer(layer);

    # Set extent to the extent of our layer
    self.canvas.setExtent(layer.extent())

    # Set up the map canvas layer set
    self.layers.append( QgsMapCanvasLayer(layer) )
    self.canvas.setLayerSet(self.layers)

def main(argv):
  # create Qt application
  app = QApplication(argv)

  # Environment variable QGISHOME must be set to the install directory
  # before running the application
  qgis_prefix = os.getenv("QGISHOME")
  if qgis_prefix == None:
    qgis_prefix =  "C:\\PROGRA~2\\QGISWI~1\\apps\\qgis"

  # Initialize qgis libraries
  QgsApplication.setPrefixPath(qgis_prefix, True)
  QgsApplication.initQgis()

  # create main window
  wnd = ShapeViewer()

  # Move the app window to upper left
  wnd.move(200,200)
  wnd.show()

  # run!
  retval = app.exec_()

  # exit
  QgsApplication.exitQgis()
  sys.exit(retval)


if __name__ == "__main__":
  main(sys.argv)

