##qgis环境配置
### python导入
```python
from qgis.core import QgsApplication

#初始化qgis
QgsApplication.setPrefixPath("/usr/share/qgis", True)
qgs = QgsApplication([], True)
# Load providers
qgs.initQgis()

import sys
sys.path.append('/usr/share/qgis/python/plugins')
# 导入processing
import processing
# 注册算法
from processing.core.Processing import Processing
Processing.initialize()
from processing.tools import *

#其他代码
pass

qgs.exitQgis()
```
### import processing
```
sys.path.append('/usr/share/qgis/python/plugins')
import processing
# 注册算法
from processing.core.Processing import Processing
Processing.initialize()
from processing.tools import *

```
## qgis路径分析
### 数据处理
#### 最短路径
求解点点之间的最短路径
#### 线相交
求线线的交接
#### 用线分割
线线相互分割
#### 平滑
折线转圆滑曲线
