from vpython import sphere
from vpython import arrow
from vpython import vector
from vpython import color
from vpython import text
from vpython import arange
from vpython import rate
import math


# 小球的半徑（可隨意調整）
R = 9
# 畫出一顆不太小的球代表一群聚成球狀的電荷分布
charge = sphere(radius=R, opacity=0.8)

# 箭頭的寬度
sw = R/5

# 畫一個箭頭代表 x 軸，並加上一個文字 X
xaxis = arrow(axis=vector(1, 0, 0)*R*12, color=color.red, shaftwidth=sw)
text(text="X", pos=xaxis.axis, color=xaxis.color, height=R*1.5)
# 畫一個箭頭代表 y 軸，並加上一個文字 Y
yaxis = arrow(axis=vector(0, 1, 0)*R*12, color=color.green, shaftwidth=sw)
text(text="Y", pos=yaxis.axis, color=yaxis.color, height=R*1.5)
# 畫一個箭頭代表 z 軸，並加上一個文字 Z
zaxis = arrow(axis=vector(0, 0, 1)*R*12, color=color.cyan, shaftwidth=sw)
text(text="Z", pos=zaxis.axis, color=zaxis.color, height=R*1.5)


# 點電荷所帶的電荷，假設為 1e23 個質子的電荷
charge.q = 1.6e-19 * 1e23  # 庫倫
# 計算聚成球狀的電荷密度
charge.density = charge.q / (4/3)*math.pi*charge.radius**3
# 真空介電常數（SI 單位制）
epsilon = 8.854187817e-12


theta_step, phi_step = input("Please input the steps of theta \
and phi.").split()
inte_radius_step, inte_theta_step, inte_phi_step = input("Please \
input the steps of theta and phi.").split()
theta_step, phi_step = int(theta_step), int(phi_step)
inte_radius_step, inte_theta_step, inte_phi_step = int(
    inte_radius_step), int(inte_theta_step), int(inte_phi_step)


for theta in arange(0, 180, 180/theta_step):   # 天頂角根據輸入步數，決定總步

    theta = theta*math.pi/180  # 換成弧度

    for phi in arange(0, 360, 360/phi_step):  # 方位角根據輸入步數，決定總步

        phi = phi*math.pi/180  # 換成弧度

        r = R * 3 * vector(     # 算出要計算電場的位置（距離球心有多少距離）
            math.sin(theta)*math.cos(phi),  # x-分量
            math.sin(theta)*math.sin(phi),  # y-分量
            math.cos(theta)  # z-分量
        )

        # 把這個球體由小積分到大，並用每個區塊的電荷計算該距離的電場
        # 將球的半徑分成許多小步計算
        drp = charge.radius/inte_radius_step
        # 將天頂角 thetap 分成許多小步計算
        dthetap = math.pi/inte_theta_step
        # 將方位角 phip 分成許多小步計算
        dphip = math.pi*2/inte_phi_step
        E = vector(0, 0, 0)    # 電場先設定為 0，後面計算中會積分出來

        for rp in arange(0, charge.radius, drp):   # 積分半徑從 0 到 charge.radius
            for thetap in arange(0, math.pi, dthetap):  # 積分天頂角從 0 到 pi（北極到南極）
                for phip in arange(0, 2*math.pi, dphip):  # 積分方位角從 0 到 2*pi（繞一整圈）
                    # 每一小步對應一小塊的體積，裡面有電荷
                    r_dV = rp * vector(                 # 算出這一個小塊的位置
                        math.sin(thetap)*math.cos(phip),
                        math.sin(thetap)*math.sin(phip),
                        math.cos(thetap)
                    )

                    delta_r = r - r_dV  # 得出從積分半徑到計算電場位置的距離
                    # 計算積分半徑的體積
                    dV = drp * (rp*dthetap) * (rp*math.sin(thetap) * dphip)
                    dq = charge.density * dV  # 計算體積的電荷

                    # 把這一小塊當成一個點電荷，套用點電荷公式計算小塊產生的微小電場
                    dE = 1/(4*math.pi*epsilon) * dq / \
                        delta_r.mag2 * delta_r.norm()

                    # 加總到 E
                    E += dE

        # 每個箭頭的電場大小
        print("mangitude of E:", E.mag, sep='')
        # 畫一個箭頭代表電場，乘上一個比例讓箭頭看起來大小合適
        arrow(pos=r, axis=E*3e-15/10, shaftwidth=sw/3)

        # 以(1.0/frequency)的秒數定義一秒要執行幾個
        rate(1000)

# 總共的積分步數
print("Integration total step:", inte_phi_step
      * inte_theta_step * inte_radius_step, sep='')
# 全部總共的步數
print("All total step:", theta_step * phi_step * inte_phi_step
      * inte_theta_step * inte_radius_step, sep='')
