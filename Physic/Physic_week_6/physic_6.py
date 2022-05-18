from vpython import sphere
from vpython import arrow
from vpython import vector
from vpython import color
from vpython import text
from vpython import arange
from vpython import rate
from vpython import graph
from vpython import gcurve
import math
import statistics

output_field = open("elect_field.txt", "w")  # 印出距離與電場
output_potent = open("elect_flux.txt", "w")  # 印出距離與電通量

# 定義球的半徑
R = 5
# 畫出一顆不太小的球代表一群聚成球狀的電荷分布
charge = sphere(radius=R, opacity=0.8)

# 箭頭的寬度
sw = R/10
# 畫一個箭頭代表 x,y,z 軸，並加上一個文字 X,Y,Z
xaxis = arrow(axis=vector(1, 0, 0)*R*5, color=color.red, shaftwidth=sw)
text(text="X", pos=xaxis.axis, color=xaxis.color, height=R)
yaxis = arrow(axis=vector(0, 1, 0)*R*5, color=color.green, shaftwidth=sw)
text(text="Y", pos=yaxis.axis, color=yaxis.color, height=R)
zaxis = arrow(axis=vector(0, 0, 1)*R*5, color=color.cyan, shaftwidth=sw)
text(text="Z", pos=zaxis.axis, color=zaxis.color, height=R)

# 點電荷所帶的電荷，假設為 1e23 個質子的電荷
charge.q = 1.6e-19 * 1e23  # 庫倫
# 計算聚成球狀的電荷密度
charge.density = charge.q / (4/3*math.pi*charge.radius**3)
# 真空介電常數（SI 單位制）
epsilon = 8.854187817e-12

F_r_g = graph(
    title='Electric Flux vs Distance',
    xtitle='<em>r</em> (m)',
    ytitle='<em>&Phi;</em> (volt m)'
)
F_r = gcurve(graph=F_r_g, color=color.blue)

E_r_g = graph(
    title='Electric Field Strength vs Distance',
    xtitle='<em>r</em> (m)',
    ytitle='<em>E</em> (volt / m)'
)
E_r = gcurve(graph=E_r_g, color=color.red)

# 以下的設定為電場的位置
theta = math.pi/2  # 位置的天頂角（這個是固定的）
phi = 0  # 位置的方位角（每次半徑加一點，方位角加一點）
dphi = math.pi/30  # 每次方位角要加多少

flux_inside = []  # 半徑內的電通量
flux_outside = []  # 半徑外的電通量

# 距離從 3*R/100 到 3 倍半徑，以半徑的 1/100 為步                # 距離從 0 到 2 倍半徑，以半徑的 1/50 為布幅
for rf in arange(3*R/100, R*3, R/100):
    r = rf * vector(                                # 算出要計算電位勢／電場的位置
        math.sin(theta)*math.cos(phi),
        math.sin(theta)*math.sin(phi),
        math.cos(theta)
    )
    phi += dphi  # 下次計算位置的方位角                                    # 下次計算位置的方位角

    # 對聚成球狀的一群電荷積分來計算電場
    drp = R/30                                     # 將球的半徑分成許多小步計算，計算每一步的大小
    # 將天頂角 thetap 分成許多小步計算，計算每一步的大小
    dthetap = math.pi/30
    # 將方位角 phip 分成許多小步計算，計算每一步的大小
    dphip = math.pi/30
    F = 0  # 初始設定電通量                                         # 電通量先設定為 0，後面計算中會【積分】出來
    # 初始設定電場                             # 電場先設定為 0，後面計算中會積分出來
    E = vector(0, 0, 0)

    for rp in arange(0, charge.radius, drp):          # 積分開始，半徑從 0 到 charge.radius
        for thetap in arange(0, math.pi, dthetap):         # 天頂角從 0 到 pi（北極到南極）
            for phip in arange(0, 2*math.pi, dphip):       # 方位角從 0 到 2*pi（繞一整圈）
                # 每一小步對應一小塊的體積，裡面有電荷
                r_dV = rp * vector(                 # 算出這一個小塊的位置
                    math.sin(thetap)*math.cos(phip),
                    math.sin(thetap)*math.sin(phip),
                    math.cos(thetap)
                )

                dx_1 = r_dV.norm()*drp  # r的小向量
                dx_3 = vector(0, 0, 1).cross(r_dV.norm())*rp * \
                    math.sin(thetap)*dphip  # phi的小向量
                calc_phi = vector(0, 0, 1).cross(r_dV.norm())
                dx_2 = calc_phi.norm().cross(r_dV.norm())*rp*dthetap  # theta的小向量
                delta_r = r - r_dV      # 計算從這一小塊開始到計算電場位置的向量

                # 我們需要這個向量，因為底下要把這一小塊
                # 當作點電荷，然後使用點電荷公式來計算電
                # 場，而點電荷公式裡面的 r 是要從電荷所
                # 在位置開始（不見得是原點開始）的向量。

                if delta_r.dot(dx_1) > 0 and delta_r.dot(dx_1) < dx_1.mag2:
                    if delta_r.dot(dx_2) > 0 and delta_r.dot(dx_2) < dx_2.mag2:
                        if delta_r.dot(dx_3) > 0 and delta_r.dot(dx_3) < dx_3.mag2:
                            continue
                r_center = r_dV + (dx_1+dx_2+dx_3)/2
                delta_r = r - r_center

                # 算出這一小塊的體積（微小但不是無限小體積公式，從上面公式積分得來）
                dV = ((rp+drp)**3-rp**3)/3 * \
                    (math.cos(thetap)-math.cos(thetap+dthetap)) * dphip
                # 算出這一小塊裡面所含的電荷
                dq = charge.density * dV

                # 把這一小塊當成一個點電荷，套用點電荷公式計算小塊產生的微小電場
                dE = 1/(4*math.pi*epsilon)*dq/delta_r.mag2*delta_r.norm()
                # 加總到 E
                E += dE

    # 電場計算完畢，計算電通量
    #       原則上電通量的計算也應該要做積分，只是我們這個練習是球狀電荷，
    #       直接把電場強度乘以球面積便是結果。如果不是球狀的，可能就得實際
    #       做積分才行。
    F = E.mag * 4*math.pi*rf**2
    F_r.plot(rf, F)                                  # 在 F-r 圖上畫一個點
    E_r.plot(rf, E.mag)                              # 在 E-r 圖上畫一個點

    rate(1000)                                       # 更新畫面，裡面的數字是【希望】電腦可以每秒更新
    # 這麼多次，電腦夠快就做得到，不夠快也不會出錯
    # 調整這個數字可以調整動畫的速度

    print(f"{rf}:{F}", file=output_potent)  # 印出距離與電通量
    print(f"{rf}:{E.mag}", file=output_field)  # 印出距離與電場

    if rf < R:  # 距離內的電通量
        flux_inside.append(F*1/(rf*rf*rf))
    elif rf > R:  # 距離外的電通量
        flux_outside.append(F)


print("stdev_inside:", statistics.stdev(flux_inside))
print("stdev_outside:", statistics.stdev(flux_outside))
print("Done.")
