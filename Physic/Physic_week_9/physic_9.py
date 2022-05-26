from vpython import vector
from vpython import arange
from vpython import rate
from vpython import cylinder
from vpython import color
from vpython import graph
from vpython import gcurve
from vpython import arrow
import math
import numpy as np


# 定義電線的半徑及長度（可隨意調整）
R = 0.1        									# 電線半徑
L = 2												# 電線長度

# 畫出一條粗圓柱代表一條粗直電線
wire = cylinder(pos=vector(0, 0, -L/2), radius=R,
                axis=vector(0, 0, L), opacity=0.5)
sw = R / 100
# 電流大小
I = 5   # 安培
# 電流密度（單位面積的電流）
J = wire.axis.norm() * I / (math.pi * R**2)
# 真空磁導率（或導磁率，SI 單位制）
mu_0 = 4 * math.pi * 1e-7			# N / A^2

# 產生一個新畫布，用來畫 B_r 圖，取名為 B_r_g
BL_vs_R = graph(
    title='Ampere\'s Law with Distance',			# 畫布標題
    xtitle='<em>r</em> (m)',								# x-軸標題
    ytitle='<em>B dot dl total</em> (T)'								# y-軸標題
)
# 產生一個空的【曲線圖】，取名為 B_r（因為要畫 B vs r 的曲線圖）
BL_R = gcurve(
    graph=BL_vs_R,											# 指定畫布為 B_r_g
    color=color.blue
)

Bl_inside_x = np.array([])  # 內部積分的距離
Bl_inside_y = np.array([])  # 內部積分的值
Bl_outside_x = np.array([])  # 外部積分的距離
Bl_outside_y = np.array([])  # 外部積分的值

dr = R / 100  # 把半徑切100份
dphi = 2*math.pi / 20  # 把角度切20份
for dr_total in arange(0, 0.20, dr):
    BL = 0												# 路徑積分的結果，先設為 0

    for dphi_total in arange(0, 2*math.pi, dphi):

        r = vector(dr_total * math.cos(dphi_total),  # 此為計算磁場的位置
                   dr_total * math.sin(dphi_total), 0)
        phi_norm = vector(0, 0, 1).cross(r.norm())
        dl_mang = dr_total * dphi
        dl = phi_norm * dl_mang

        B = vector(0, 0, 0)								# 磁場先設定為 0，後面計算中會積分出來

        # 切割電線（做積分）
        drp = R / 50									# 沿著圓柱半徑切成多個小段
        dphip = 2*math.pi / 150								# 沿著角度切成多個小角度
        dzp = L / 200									# 沿著圓柱軸長切成多個小段

        for rp in arange(0, R, drp):						# 積分開始 rp 從 0 到 R
            for phip in arange(0, 2*math.pi, dphip):			# phip 從 0 到 2pi（繞一圈）
                for zp in arange(-L/2, L/2, dzp):			# zp 從 -L/2 到 L/2
                    # 每一小塊電線體積為 dV，面有電流 JdV 流過

                    # 計算這一小塊電線的體積（微小但不是無限小體積公式，從上面公式積分得來）
                    dV = ((rp+drp)**2 - rp**2)/2 * dphip * dzp

                    r_dV = vector(						# 算出這一小塊電線的位置
                        rp * math.cos(phip),
                        rp * math.sin(phip),
                        zp
                        )

                    delta_r = r - r_dV					# 計算從這一小塊電線開始到計算電場位置的向量

                    dx_1 = (r_dV-vector(0, 0, zp)).norm() * \
                        drp  # rho的小塊單位向量
                    dx_3 = vector(0, 0, 1) * dzp  # z的小塊單位向量
                    dx_2 = dx_3.cross(dx_1) * dphip  # phi的小塊單位向量

                    if 0 < delta_r.dot(dx_1) and delta_r.dot(dx_1) < dx_1.mag2:
                        if 0 < delta_r.dot(dx_2) and delta_r.dot(dx_2) < dx_2.mag2:
                            if 0 < delta_r.dot(dx_3) and delta_r.dot(dx_3) < dx_3.mag2:
                                continue

                    r_center = r_dV + (dx_1 + dx_2 + dx_3)/2
                    delta_r = r - r_center  # 使用小塊的中心點更符合定義

                    # 利用比歐-沙伐公式計算這一小塊電線產生的微小磁場
                    dB = mu_0/(4*math.pi) * dV * \
                        J.cross(delta_r) / delta_r.mag**3

                    # 加總到 B
                    B += dB
        arrow(pos=r, axis=B*1e4, shaftwidth=sw/3)			# 畫一個箭頭代表磁場
        BL += B.dot(dl)

    BL_R.plot(dr_total, BL)								# 在 B_r 曲線圖上畫一個點
    rate(1000)

    if dr_total < R:
        Bl_inside_x = np.append(Bl_inside_x, dr_total)
        Bl_inside_y = np.append(Bl_inside_y, BL)
    elif dr_total > R:
        Bl_outside_x = np.append(Bl_outside_x, dr_total)
        Bl_outside_y = np.append(Bl_outside_y, BL)

avg = sum(Bl_outside_y)/len(Bl_outside_y)
ideal = mu_0 * I
error = abs(ideal-avg)/ideal
print("Avg:", avg)
print("Ideal:", ideal)
print("Error:", error)
