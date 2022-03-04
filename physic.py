from vpython import sphere
from vpython import arrow
from vpython import vector
from vpython import color
from vpython import text
from vpython import arange
from vpython import rate
import math

R = 1e-4  # 小球的半徑(由於x,y,z向量的大小是以半徑衡量，因此改動這個值對結果沒影響)
charge = sphere(radius=R, opacity=0.8)  # 畫出一顆小球代表一個點電荷

sw = R/5  # 箭頭的寬度
xaxis = arrow(axis=vector(1, 0, 0)*R*20, color=color.red, shaftwidth=sw)
text(text="X", pos=xaxis.axis, color=xaxis.color, height=R*3)
# 畫一個箭頭代表 y 軸，並加上一個文字 Y
yaxis = arrow(axis=vector(0, 1, 0)*R*20, color=color.green, shaftwidth=sw)
text(text="Y", pos=yaxis.axis, color=yaxis.color, height=R*3)
# 畫一個箭頭代表 z 軸，並加上一個文字 Z
zaxis = arrow(axis=vector(0, 0, 1)*R*20, color=color.cyan, shaftwidth=sw)
text(text="Z", pos=zaxis.axis, color=zaxis.color, height=R*3)


# 點電荷所帶的電荷，假設為 1 個質子的電荷
charge.q = 1.6e-19  # 庫倫
# 真空介電常數（SI 單位制）
epsilon = 8.854187817e-12

# 因為range只能處理整數，我們需要用arange處理浮點數(180/20)
for theta in arange(0, 180, 180/20):                      # 天頂角從北極到南極，分成 20 步完成

    theta = theta * math.pi/180                                # 換成弧度

    for phi in arange(0, 360, 360/40):                    # 方位角繞一整圈，分成 40 步完成

        phi = phi * math.pi/180                                # 換成弧度

        r = R * 15 * vector(							# 算出要計算電場的位置（以距離球體的15倍觀察結果）
            math.sin(theta)*math.cos(phi),  # x-分量
            math.sin(theta)*math.sin(phi),  # y-分量
            math.cos(theta)  # z-分量
        )

        E = 1/(4*math.pi*epsilon)*charge.q/r.mag2*r.norm()   # 套用公式計算電場

        print("Vector E:", E)  # 觀察電場的向量
        print("Mangitude of E:", E.mag)  # 測試電場的大小

        arrow(pos=r, axis=E*2e2, shaftwidth=sw/3)        # 畫一個箭頭代表電場

        rate(60)    # 更新畫面，裡面的數字是【希望】電腦可以每秒更新
        # 這麼多次，電腦夠快就做得到，不夠快也不會出錯
        # 調整這個數字可以調整動畫的速度
