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
qgis_prefix = "C:\\PROGRA~2\\QGISWI~1\\apps\\qgis"

class ShapeViewer(QMainWindow, Ui_MainWindow):sys.path.extend(['D:\\Learning\\workspace\\MapCanvas'])

def __init__(self):
    QMainWindow.__init__(self)

    # Required by Qt4 to initialize the UI
    self.setupUi(self)

    # Set the title for the app
    self.setWindowTitle("ShapeViewer")

    # Create the map canvas
    self.canvas = QgsMapCanvas()
    self.canvas.useImageToRender(False)
    self.canvas.show()

    # Lay our widgets out in the main window using a
    # vertical box layout
    self.layout = QVBoxLayout(self.frame)
    self.layout.addWidget(self.canvas)
    # layout is set - open a layer
    # Add an OGR layer to the map
    file = QFileDialog.getOpenFileName(self,"Open Shapefile", ".", "Shapefiles (*.shp)")
    fileInfo = QFileInfo(file)

    # Add the layer
    layer = QgsVectorLayer(file, fileInfo.fileName(), "ogr")

    if not layer.isValid():
      return

    # Change the color of the layer to gray
    #symbols = layer.renderer().symbols()
    #ymbol = symbols[0]
    #ymbol.setFillColor(QColor.fromRgb(192,192,192))

    # Add layer to the registry
    QgsMapLayerRegistry.instance().addMapLayer(layer);

    # Set extent to the extent of our layer
    self.canvas.setExtent(layer.extent())

    # Set up the map canvas layer set
    cl = QgsMapCanvasLayer(layer)
    layers = [cl]
    self.canvas.setLayerSet(layers)

def main(argv):
  # create Qt application
  app = QApplication(argv)

  qgis_prefix = "C:\\PROGRA~2\\QGIS Lyon\\apps\\qgis"
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

