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

# output_file = open("output.txt", "w") # 提供檔案輸出方法

R = 1e-4  # 小球的半徑
charge = sphere(radius=R, opacity=0.8)  # 畫出一顆小球代表一個點電荷

sw = R/5  # 箭頭的寬度
# 畫一個箭頭代表 x 軸，並加上一個文字 X
xaxis = arrow(axis=vector(1, 0, 0)*R*10, color=color.red, shaftwidth=sw)
text(text="X", pos=xaxis.axis, color=xaxis.color, height=R*1.5)
# 畫一個箭頭代表 y 軸，並加上一個文字 Y
yaxis = arrow(axis=vector(0, 1, 0)*R*10, color=color.green, shaftwidth=sw)
text(text="Y", pos=yaxis.axis, color=yaxis.color, height=R*1.5)
# 畫一個箭頭代表 z 軸，並加上一個文字 Z
zaxis = arrow(axis=vector(0, 0, 1)*R*10, color=color.cyan, shaftwidth=sw)
text(text="Z", pos=zaxis.axis, color=zaxis.color, height=R*1.5)


# 點電荷所帶的電荷，假設為 1 個質子的電荷
charge.q = 1.6e-19  # 庫倫
# 真空介電常數（SI 單位制）
epsilon = 8.854187817e-12
# 產生一個空的【曲線圖】，取名為 E_r（因為要畫 E vs r 的曲線圖）
E_r = gcurve(color=color.red)
# 產生一個list，用來儲存每個計算標準差的數值
standard_dev = []

theta = math.pi/2                                        # 計算電場位置的天頂角
phi = math.pi/4                                          # 計算電場位置的方位角


# 因為range只能處理整數，我們需要用arange處理浮點數的遞增
for rf in arange(R*10, R*20, R*10/100):                  # 距離從點電荷數倍半徑到數倍半徑的地方

    r = rf * vector(                    # 算出要計算電場的位置
        math.sin(theta)*math.cos(phi),  # x-分量
        math.sin(theta)*math.sin(phi),  # y-分量
        math.cos(theta)                 # z-分量
    )

    E = 1/(4*math.pi*epsilon)*charge.q/r.mag2*r.norm()   # 套用公式計算電場

    # print("R:", r)  # 印出半徑的向量 --測試
    # print("Mangitude of E:", E.mag)  # 印出電場的大小 --測試
    print(E.mag * rf * rf)
    standard_dev.append(rf*E.mag)  # 放入目前電場乘以半徑平方的值

    arrow_object = arrow(pos=r, axis=E*2e-1, shaftwidth=sw*2)
    E_r.plot(rf, E.mag)								# 在 E_r 曲線圖上畫一個點

    rate(10)    # 以(1.0/frequency)的秒數定義一秒要印多少個
    arrow_object.visible = False  # 可用此行隱藏過去產生的箭頭

print(statistics.stdev(standard_dev))  # 印出標準差
