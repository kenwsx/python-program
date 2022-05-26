from vpython import arrow
from vpython import vector
from vpython import arange
from vpython import rate
from vpython import cylinder
from vpython import gcurve
from vpython import color
import math

# 定義電線的半徑及長度（可隨意調整）
R = 0.05        									# 電線半徑
L = 2												# 電線長度

# 畫出一條細圓柱代表一條細直電線
wire = cylinder(pos=vector(0, 0, -4*L), radius=R,
                axis=vector(0, 0, 8*L), opacity=0.5)

BL_vs_R = gcurve(color=color.blue, fast=False, size=6)

# 電流大小
I = 5    # 安培
# 電流密度（單位面積的電流）
J = wire.axis.norm() * I / (math.pi * R**2)
# 真空磁導率（或導磁率，SI 單位制）
mu_0 = 4 * math.pi * 1e-7			# N / A^2


dr = R / 100  # 把半徑切100份
dphi = 2*math.pi / 50  # 把角度切50份
for dr_total in arange(0, 0.35, dr):
    BL = 0												# 路徑積分的結果，先設為 0

    for dphi_total in arange(0, 2*math.pi, dphi):

        r = vector(dr_total * math.cos(dphi_total),
                   dr_total * math.sin(dphi_total), 0)
        phi_norm = vector(0, 0, 1).cross(r.norm())
        dl_mang = dr_total * dphi
        dl = phi_norm * dl_mang

        B = vector(0, 0, 0)    # 磁場先設定為 0，後面計算中會積分出來

        # 切割電線（做積分）
        drp = R / 20    # 沿著圓柱半徑（rho軸）切成多個小段
        dphip = 2*math.pi / 80    # 沿著角度（phi軸）切成多個小角度
        dzp = L / 80   # 沿著圓柱軸長（z軸）切成多個小段

        for rp in arange(0, R, drp):						# 積分開始 rp 從 0 到 R
            for phip in arange(0, 2*math.pi, dphip):			# phip 從 0 到 2pi（繞一圈）
                for zp in arange(-4*L, 4*L, dzp):			# zp 從 -L/2 到 L/2

                    # 計算這一小塊電線的體積（微小但不是無限小體積公式，從上面公式積分得來）
                    dV = ((rp+drp)**2 - rp**2)/2 * dphip * dzp

                    r_dV = vector(						# 算出這一小塊電線的位置
                        rp * math.cos(phip),
                        rp * math.sin(phip),
                        zp
                    )

                    # 藉由把小塊位置改成在小塊中間，可使計算更準確
                    dx_1 = (r_dV-vector(0, 0, zp)).norm() * drp  # rho的小塊單位向量
                    dx_3 = vector(0, 0, 1) * dzp  # z的小塊單位向量
                    dx_2 = dx_3.cross(dx_1) * dphip  # phi的小塊單位向量
                    r_center = r_dV + (dx_1 + dx_2 + dx_3)/2
                    delta_r = r - r_center

                    # 利用比歐-沙伐公式計算這一小塊電線產生的微小磁場
                    dB = mu_0/(4*math.pi) * dV * \
                        J.cross(delta_r) / delta_r.mag**3

                    # 加總到 B
                    B += dB

        rate(1000)										# 更新畫面，裡面的數字是【希望】電腦可以每秒更新
