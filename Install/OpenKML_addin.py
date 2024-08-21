# import relevant packages and modules
import arcpy, os
from arcpy import env, da, mapping, conversion
import pythonaddins

class ButtonClass1(object):
    """Implementation for OpenKML_addin.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        # set environment for map document
        mxd = mapping.MapDocument("current")
        path = r"C:\KML"
        if not os.path.exists(path):
            os.mkdir(path)
        env.workspace = path
        env.overwriteOutput = 1

        # list layers and reference the first layer (local variable for argument in conversion function) in the current map document
        map_layer = mapping.ListLayers(mxd)
        layer = map_layer[0]

        # get objectID attribute of the referenced layer based on "selection" 
        # use the objectID to set a unique name for the kml_name (local variable argument in conversion funtion and startfile method)
        with da.SearchCursor (layer, ("FID")) as cursor:
            for row in cursor:
                kml_name = str(row[0]) + ".kmz"

        # run the conversion tool from layer to KML and save the map document
        conversion.LayerToKML(layer, kml_name)
        mxd.save()

        # open the converted layer in Google Earth
        os.chdir (env.workspace)
        os.startfile(kml_name)
