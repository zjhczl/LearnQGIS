
from qgis.core import QgsApplication
import sys

sys.path.append('/usr/share/qgis/python')

QgsApplication.setPrefixPath("/usr/share/qgis", True)

QgsApplication.initQgis()
import processing
