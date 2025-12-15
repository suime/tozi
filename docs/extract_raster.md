# 래스터 이미지 추출하는 방법

## 0. 준비사항

1. 래스터 레이어(항공사진)과 벡터 레이어(필지)를 Qgis 프로젝트에 넣는다.

## 1. 그리드 레이어 만들기

1. 공간 처리 툴박스 패널을 연다. `보기 - 패널 - 공간 처리 툴박스` 체크
   ![1](../images/r01.png)
1. 공간 처리 툴박스에서 그리드 생성을 한다. ``
   ![2](../images/r02.png)
1. 옵션
   ![3](../images/r03.png)
   - 그리드 유형 : `사각형(폴리곤)`
   - 그리드 범위 : 레이어에로부터 계산 (벡터 레이어: 필지)
   - 수평 간격 및 수직 간격 : `20` 미터 (분할할 이미지 사이즈에 맞춰 적당히 조절한다.)
   - 그리드 : `그리드20` (저장할 레이어명)

## 2. 그리드 레이어 추출

1. 그럼 필지가 있는 전체 범위로 그리드가 생성되기 때문에 필지가 있는 부분만 잘라내야 한다.
1. 공간 처리 툴 박스에서 `벡터 선택 - 위치로 추출` 선택
   ![4](../images/r04.png)
1. 옵션
   - 다음에서 피처 추출 : `그리드20` (추출할 그리드 레이어)
   - 피처 위치 : 교차, 중첩 선택
   - 다음과 같은 피처를 비교 : 필지 레이어
   - Extracted : 그리드20_extracted.shp (저장할 레이어 및 파일명)

## 3. 추출한 그리드에서 이미지 분할하기

1. 이제 항공사진(래스터 레이어)에서 이미지를 추출해야 한다.
1. `crtl + alt + p` 또는 `플러그인 - 파이썬 콘솔`을 눌러 qgis에서 파이썬 콘솔 창을 연다.
1. 아래와 같은 코드를 입력하고 실행한다. (레이어명 정확하게 들어가게 유의)

```python
from qgis.core import *


# 그리드 레이어명
grid = QgsProject.instance().mapLayersByName("그리드20_extracted")[0]


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

```

1. 실행하면 `./output/` 폴더에 20m 범위의 이미지가 생성된다.
