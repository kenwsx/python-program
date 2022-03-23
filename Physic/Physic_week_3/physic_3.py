from vpython import sphere
from vpython import arrow
from vpython import vector
from vpython import color
from vpython import text
from vpython import arange
from vpython import rate
from vpython import gcurve
import math
import statistics

# output_file = open("output.txt", "w")  # 提供檔案輸出方法（預設名稱為output.txt）

# 這次我們只模擬出一個空間與球體
R = 1e-4  # 小球的半徑
# 畫出一顆小球代表一個點電荷
charge = sphere(radius=R, opacity=0.8)

sw = R/5  # 箭頭的寬度
# 畫一個箭頭代表 x 軸，並加上一個文字 X
xaxis = arrow(axis=vector(1, 0, 0)*R*10,
              color=color.red, shaftwidth=sw)
text(text="X", pos=xaxis.axis,
     color=xaxis.color, height=R*1.5)
# 畫一個箭頭代表 y 軸，並加上一個文字 Y
yaxis = arrow(axis=vector(0, 1, 0)*R*10,
              color=color.green, shaftwidth=sw)
text(text="Y", pos=yaxis.axis,
     color=yaxis.color, height=R*1.5)
# 畫一個箭頭代表 z 軸，並加上一個文字 Z
zaxis = arrow(axis=vector(0, 0, 1)*R*10,
              color=color.cyan, shaftwidth=sw)
text(text="Z", pos=zaxis.axis,
     color=zaxis.color, height=R*1.5)


# 點電荷所帶的電荷，假設為 1 個質子的電荷
charge.q = 1.6e-19  # 庫倫
# 真空介電常數（SI 單位制）
epsilon = 8.854187817e-12
# 產生一個空的【曲線圖】，取名為 V_r
V_r = gcurve(color=color.blue)
# 產生一個list，用來儲存每個計算標準差的數值
standard_dev = []

theta = math.pi/2    # 計算電場位置的天頂角
phi = math.pi/4      # 計算電場位置的方位角


# 因為range只能處理整數，我們需要用arange處理浮點數的遞增
# 距離從點電荷一倍半徑到數倍半徑的地方
counter = 0
for rf in arange(R, R*10, R*10/100):
    counter += 1

    r = rf * vector(         # 算出要計算電場的位置
        math.sin(theta)*math.cos(phi),  # x-分量
        math.sin(theta)*math.sin(phi),  # y-分量
        math.cos(theta)                 # z-分量
    )

    # 套用公式計算電位
    V = 1/(4*math.pi*epsilon)*charge.q/r.mag
    print("R:", "{:.6f}".format(rf), sep="", end=" ")  # 印出半徑的大小 --測試
    print("V:", "{:.8f}".format(V), sep="")  # 印出電位的大小 --測試
    print("V * rf:", V*rf)  # 印出電位乘以半徑的值 --測試
    standard_dev.append(rf*V)  # 放入目前電位乘以半徑的值

    V_r.plot(rf, V)  # 在V_r 曲線圖上畫一個點

    rate(1000)  # 以(1.0/frequency)的秒數定義一秒要印多少個

# 印出標準差
print("Stdev", statistics.stdev(standard_dev))
