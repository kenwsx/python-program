from vpython import vector
from vpython import color
from vpython import arange
from vpython import rate
from vpython import gdots
import math

output = open("question_output.txt", "w")

# 記錄每個半徑的總電場
E_dic = {}

# 檢測從半徑1到半徑8的數值
for R in range(1, 9):

    # 點電荷所帶的電荷，假設為 1e23 個質子的電荷
    q = 1.6e-19 * 1e23  # 庫倫
    # 計算聚成球狀的電荷密度
    density = q / (4/3)*math.pi*R**3
    # 真空介電常數（SI 單位制）
    epsilon = 8.854187817e-12
    V_r = gdots(color=color.blue, fast=False, size=6)
    # 每個半徑電場的值
    electric_field = 0

    for theta in arange(0, 180, 180/20):   # 天頂角根據輸入步數，決定總步

        theta = theta*math.pi/180  # 換成弧度

        for phi in arange(0, 360, 360/40):  # 方位角根據輸入步數，決定總步

            if theta != 0 or phi != 0:
                continue

            phi = phi*math.pi/180  # 換成弧度

            r = 10 * vector(     # 算出要計算電場的位置（距離球心有多少距離）
                math.sin(theta)*math.cos(phi),  # x-分量
                math.sin(theta)*math.sin(phi),  # y-分量
                math.cos(theta)  # z-分量
            )

            # 把這個球體由小積分到大，並用每個區塊的電荷計算該距離的電場
            # 將球的半徑分成許多小步計算
            drp = R/50
            # 將天頂角 thetap 分成許多小步計算
            dthetap = math.pi/60
            # 將方位角 phip 分成許多小步計算
            dphip = math.pi*2/30
            E = vector(0, 0, 0)    # 電場先設定為 0，後面計算中會積分出來

            for rp in arange(0, R, drp):   # 積分半徑從 0 到 charge.radius
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
                        dq = density * dV  # 計算體積的電荷

                        # 把這一小塊當成一個點電荷，套用點電荷公式計算小塊產生的微小電場
                        dE = 1/(4*math.pi*epsilon) * dq / \
                            delta_r.mag2 * delta_r.norm()

                        # 加總到 E
                        E += dE

            V_r.plot(R, E.mag)  # 在V_r 曲線圖上畫目前半徑的點
            if R > 1:
                V_r.plot(R, E_dic["rad_1"]*R**3)  # 在V_r 曲線圖上畫出理論半徑的點
            # 如果是第一個方位，就存入總電場的值
            if theta == 0 and phi == 0:
                electric_field = E.mag

            # 以(1.0/frequency)的秒數定義一秒要執行幾個
            rate(1000)

    # 把總電場的值放入字典
    E_dic["rad_"+str(R)] = electric_field

# 印出全部半徑電場的值（在theta = 0, phi = 0 的方位）
for i in range(1, 9):
    result = E_dic["rad_"+str(i)]
    print(f"Radius {i}:{result}", file=output)

# 印出全部比較半徑電場的值
for i in range(2, 9):
    elect_bigger = E_dic["rad_"+str(i)]
    elect_smaller = E_dic["rad_"+str(1)]
    result = elect_bigger / elect_smaller
    print(f"Radius {i}/1:{result:.6e}", file=output, sep='')

print("Done.")
