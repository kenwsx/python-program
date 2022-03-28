from vpython import vector
from vpython import color
from vpython import arange
from vpython import rate
from vpython import gcurve
import math

output = open("output.txt", "w")

# 記錄每個半徑的總電場
E_dic = {}

# 檢測從半徑5到半徑15的數值
for R in range(5, 16):

    # 點電荷所帶的電荷，假設為 1e23 個質子的電荷
    q = 1.6e-19 * 1e23  # 庫倫
    # 計算聚成球狀的電荷密度
    density = q / (4/3)*math.pi*R**3
    # 真空介電常數（SI 單位制）
    epsilon = 8.854187817e-12
    V_r = gcurve(color=color.blue)
    E_integral_list = []

    theta_step, phi_step = 20, 40
    inte_radius_step, inte_theta_step, inte_phi_step = 5, 6, 3
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
            drp = R/inte_radius_step
            # 將天頂角 thetap 分成許多小步計算
            dthetap = math.pi/inte_theta_step
            # 將方位角 phip 分成許多小步計算
            dphip = math.pi*2/inte_phi_step
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

            # 每個箭頭的電場大小
            E_integral_list.append(E.mag)
            V_r.plot(R, E.mag)  # 在V_r 曲線圖上畫一個點

            # 以(1.0/frequency)的秒數定義一秒要執行幾個
            rate(1000)

    E_dic["rad_"+str(R)+"_max"] = max(E_integral_list)
    E_dic["rad_"+str(R)+"_min"] = min(E_integral_list)
for i in range(5, 16):

    max = E_dic["rad_"+str(i)+"_max"]
    min = E_dic["rad_"+str(i)+"_min"]
    print(f"Radius {i} min:{min:.6e}", file=output, sep='')
    print(f"Radius {i} max:{max:.6e}", file=output, sep='')
