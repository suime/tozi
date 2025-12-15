from qgis.core import *


# 그리드 레이어명
grid = QgsProject.instance().mapLayersByName("그리드")[0]


# 래스터 레이어명
raster = QgsProject.instance().mapLayersByName("항공사진")[0]


crs = grid.crs().authid()

for i, f in enumerate(grid.getFeatures()):
    # print(f.geometry())
    output = f"./image/{i}.png"

    mask_layer = QgsVectorLayer(f"Polygon?crs={crs}", "mask", "memory")

    prov = mask_layer.dataProvider()
    prov.addFeatures([f])
    mask_layer.updateExtents()

    processing.run(
        "gdal:cliprasterbymasklayer",
        {
            "INPUT": raster,
            "MASK": mask_layer,
            "SOURCE_CRS": None,
            "TARGET_CRS": None,
            "TARGET_EXTENT": None,
            "NODATA": None,
            "ALPHA_BAND": False,
            "CROP_TO_CUTLINE": True,
            "KEEP_RESOLUTION": True,
            "SET_RESOLUTION": False,
            "X_RESOLUTION": None,
            "Y_RESOLUTION": None,
            "MULTITHREADING": False,
            "OPTIONS": None,
            "DATA_TYPE": 0,
            "EXTRA": "",
            "OUTPUT": output,
        },
    )
