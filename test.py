from qgis.core import QgsApplication
import time
# Supply path to qgis install location
QgsApplication.setPrefixPath("/usr", True)

# Create a reference to the QgsApplication.  Setting the
# second argument to False disables the GUI.
qgs = QgsApplication([], True)

# Load providers
qgs.initQgis()

# Write your code here to load some layers, use processing
# algorithms, etc.
time.sleep(5)
# Finally, exitQgis() is called to remove the
# provider and layer registries from memory
qgs.exitQgis()
