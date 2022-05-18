# 線性擬和 https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.linregress.html
# 曲線擬和 https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html#scipy.optimize.curve_fit
# maxfev 問題 https://stackoverflow.com/questions/15831763/scipy-curvefit-runtimeerroroptimal-parameters-not-found-number-of-calls-to-fun
# 曲線的r-squared https://stackoverflow.com/questions/19189362/getting-the-r-squared-value-using-curve-fit

from vpython import arrow
from vpython import vector
from vpython import text
from vpython import arange
from vpython import rate
from vpython import cylinder
from vpython import color
from vpython import graph
from vpython import gcurve
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score


def func(x, a, b, c):  # 他算出來的圖形
    return a * x * x + b * x + c


def theory_graph(x):   # 定義理想的 1/r 圖形
    return 1/x


# 定義電線的半徑及長度（可隨意調整）
R = 0.05        									# 電線半徑
L = 2												# 電線長度

# 畫出一條細圓柱代表一條細直電線
wire = cylinder(pos=vector(0, 0, -L/2), radius=R,
                axis=vector(0, 0, L), opacity=0.5)

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

# 產生一個新畫布，用來畫 B_r 圖，取名為 B_r_g
B_r_g = graph(
    title='Magnetic Field Strength vs Distance',			# 畫布標題
    xtitle='<em>r</em> (m)',								# x-軸標題
    ytitle='<em>B</em> (T)'								# y-軸標題
)
# 產生一個空的【曲線圖】，取名為 B_r（因為要畫 B vs r 的曲線圖）
B_r = gcurve(
    graph=B_r_g,											# 指定畫布為 B_r_g
    color=color.blue
)

B_inside_x = np.array([])  # 內部磁場的距離
B_inside_y = np.array([])  # 內部磁場的值
B_outside_x = np.array([])  # 外部磁場的距離
B_outside_y = np.array([])  # 外部磁場的值

# 這邊計算的位置就是在導線中間
for d in arange(0, 2*R, 2*R/200):    					# 距離 d 從 0 到 2R，共計算 200 個位置

    r = vector(d, 0, 0)  # 沿著 x-軸（垂直於導線長軸的方向）
    B = vector(0, 0, 0)	 # 磁場先設定為 0，後面計算中會積分出來

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

                '''if delta_r.mag < drp:				# 計算磁場的位置如果正好在這一
                    continue'''

                dx_1 = (r_dV-vector(0, 0, zp)).norm() * drp  # rho的小塊單位向量
                dx_3 = vector(0, 0, 1) * dzp  # z的小塊單位向量
                dx_2 = dx_3.cross(dx_1) * rp * dphip  # phi的小塊單位向量

                if 0 < delta_r.dot(dx_1) and delta_r.dot(dx_1) < dx_1.mag2:
                    if 0 < delta_r.dot(dx_2) and delta_r.dot(dx_2) < dx_2.mag2:
                        if 0 < delta_r.dot(dx_3) and delta_r.dot(dx_3) < dx_3.mag2:
                            continue

                r_center = r_dV + (dx_1 + dx_2 + dx_3)/2
                delta_r = r - r_center  # 使用小塊的中心點更符合定義

                # 利用比歐-沙伐公式計算這一小塊電線產生的微小磁場
                dB = mu_0/(4*math.pi) * dV * J.cross(delta_r) / delta_r.mag**3

                # 加總到 B
                B += dB

    B_r.plot(d, B.mag)								# 在 B_r 曲線圖上畫一個點

    rate(1000)

    if d < R and d != 0:
        B_inside_x = np.append(B_inside_x, d)
        B_inside_y = np.append(B_inside_y, B.mag)
    elif d > R:
        B_outside_x = np.append(B_outside_x, d)
        B_outside_y = np.append(B_outside_y, B.mag)

res_inside = stats.linregress(B_inside_x, B_inside_y)
popt, pcov = curve_fit(func, B_outside_x, B_outside_y, maxfev=5000)
y_pred = func(B_outside_x, *popt)

# 內部理想圖與r^2
plt.plot(B_inside_x, B_inside_y, 'o', label='original data')
plt.plot(B_inside_x, res_inside.intercept + res_inside.slope
         * B_inside_x, 'r', label='fitted line inside')
plt.text(0.02, 6*10e-6, 'R-squared = %0.6f' % res_inside.rvalue**2)

# 外部理想圖與r^2
plt.plot(B_outside_x, B_outside_y, 'o', label='original data')
plt.plot(B_outside_x, func(B_outside_x, *popt), 'b',
         label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt))
plt.text(0.06, 5*10e-6, 'R-squared = %0.6f' % r2_score(B_outside_y, y_pred))


plt.legend()
plt.show()
