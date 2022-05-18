from vpython import arrow
from vpython import vector
from vpython import text
from vpython import arange
from vpython import rate
from vpython import cylinder
from vpython import gdots
from vpython import color
import math

# 定義電線的半徑及長度（可隨意調整）
R = 0.05        									# 電線半徑
L = 2												# 電線長度

# 畫出一條細圓柱代表一條細直電線
wire = cylinder(pos=vector(0, 0, -4*L), radius=R,
                axis=vector(0, 0, 8*L), opacity=0.5)

B_r = gdots(color=color.blue, fast=False, size=6)

'''sw = R/10
xaxis = arrow(axis=vector(1, 0, 0)*R*5, color=color.red, shaftwidth=sw)
text(text="X", pos=xaxis.axis, color=xaxis.color, height=R)
yaxis = arrow(axis=vector(0, 1, 0)*R*5, color=color.green, shaftwidth=sw)
text(text="Y", pos=yaxis.axis, color=yaxis.color, height=R)
zaxis = arrow(axis=vector(0, 0, 1)*R*5, color=color.cyan, shaftwidth=sw)
text(text="Z", pos=zaxis.axis, color=zaxis.color, height=R)'''

# 畫出一個箭頭代表電流方向
sw = R/10
arrI = arrow(axis=vector(0, 0, L/5), shaftwidth=sw)  # 箭頭長度是電線的 1/5
arrI.pos = arrI.pos - arrI.axis/2					# 把箭頭移到畫面中央
arrI.pos.y += R*1.5									# 箭頭稍微離開電線一些

text(												# 箭頭的中央放一個文字
    text='I',  # 文字內容
    pos=arrI.pos+arrI.axis/2,  # 文字位置
    height=R,  # 文字高度
    font='serif'  # 設定字型
)

# 電流大小
I = 50   # 安培
# 電流密度（單位面積的電流）
J = wire.axis.norm() * I / (math.pi * R**2)
# 真空磁導率（或導磁率，SI 單位制）
mu_0 = 4 * math.pi * 1e-7			# N / A^2

for z in arange(-4*L, 4*L, L/20):  # z 從 -L/4 到 L/4 增加，計算 10 個位置
    print(z)
    if z != -2.842170943040401e-14:
        continue

    B_list = []
    for phi in arange(0, 2*math.pi, 2*math.pi/100):  # 方位角繞一整圈，共計算 20 個位置

        r = vector(						# 算出要計算 磁場 的位置
            R * 1.25 * math.cos(phi),   # 在電線半徑 1.25 倍的地方（電線外面不遠處）
            R * 1.25 * math.sin(phi),
            z
        )

        B = vector(0, 0, 0)    # 磁場先設定為 0，後面計算中會積分出來

        # 切割電線（做積分）
        drp = R / 80    # 沿著圓柱半徑（rho軸）切成多個小段
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

        B_list.append(B.mag)
        arrow(pos=r, axis=B*1e4, shaftwidth=sw/3)			# 畫一個箭頭代表磁場
        rate(1000)										# 更新畫面，裡面的數字是【希望】電腦可以每秒更新

    B_r.plot(z, sum(B_list)/len(B_list))
