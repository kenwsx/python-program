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
output_potent = open("elect_potential.txt", "w")  # 印出距離與電位勢

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

# 產生一個新畫布，用來畫 V_r 圖，取名為 V_r_g
V_r_g = graph(title='Electric Potential vs Distance',
              xtitle='<em>r</em> (m)', ytitle='<em>V</em> (volt)')
# 產生一個空的【曲線圖】，取名為 V_r（因為要畫 V vs r 的曲線圖）
V_r = gcurve(graph=V_r_g, color=color.blue)

# 產生一個新畫布，用來畫 E_r 圖，取名為 E_r_g
E_r_g = graph(title='Electric Field Strength vs Distance',
              xtitle='<em>r</em> (m)', ytitle='<em>E</em> (volt / m)')
# 產生一個空的【曲線圖】，取名為 E_r（因為要畫 E vs r 的曲線圖）
E_r = gcurve(graph=E_r_g, color=color.red)

# 以下的設定皆為電位勢 與 電場的位置
theta = math.pi/2    # 位置的天頂角（這個是固定的）
phi = 0     # 位置的方位角（每次半徑加一點，方位角加一點）
dphi = math.pi/30   # 每次方位角要加多少

stdev_v_out = []  # 在半徑外的電位勢
stdev_v_in = []  # 在半徑內的電位勢
stdev_e_out = []  # 在半徑外的電場
stdev_e_in = []  # 在半徑內的電場

for rf in arange(1e-10, R*3, R/100):  # 距離從 0 到 3 倍半徑，以半徑的 1/100 為步幅
    r = rf * vector(     # 算出要計算電位勢／電場的位置
        math.sin(theta)*math.cos(phi),
        math.sin(theta)*math.sin(phi),
        math.cos(theta)
    )
    phi += dphi     # 下次計算位置的方位角

    # 對聚成球狀的一群電荷積分來計算電場
    drp = R/100                         # 將球的半徑分成許多小步計算，計算每一步的大小
    # 將天頂角 thetap 分成許多小步計算，計算每一步的大小
    dthetap = math.pi/30
    # 將方位角 phip 分成許多小步計算，計算每一步的大小
    dphip = math.pi/30
    V = 0                # 初始設定電位勢
    E = vector(0, 0, 0)   # 初始設定電場

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

                # 以下為兩種判斷方法

                # 1.最簡單的判斷方法
                # drp 是小塊在 r 方向的邊長
                '''if delta_r.mag < drp:
                    continue'''

                # 2.目前的判斷方法
                # 運用內積與delta_r，判斷是否在小塊內
                if delta_r.dot(dx_1) > 0 and \
                        delta_r.dot(dx_1) < dx_1.mag2:
                    if delta_r.dot(dx_2) > 0 and \
                            delta_r.dot(dx_2) < dx_2.mag2:
                        if delta_r.dot(dx_3) > 0 and \
                                delta_r.dot(dx_3) < dx_3.mag2:
                            continue

                # 算出這一小塊的體積（微小但不是無限小體積公式，從上面公式積分得來）
                dV = ((rp+drp)**3-rp**3)/3 * \
                    (math.cos(thetap)-math.cos(thetap+dthetap)) * dphip
                # 算出這一小塊裡面所含的電荷
                dq = charge.density * dV

                # 把這一小塊當成一個點電荷，套用點電荷公式計算小塊產生的微小電位勢
                dV = 1/(4*math.pi*epsilon)*dq/delta_r.mag
                # 加總到 V
                V += dV

                # 把這一小塊當成一個點電荷，套用點電荷公式計算小塊產生的微小電場
                dE = 1/(4*math.pi*epsilon)*dq/delta_r.mag2*delta_r.norm()
                # 加總到 E
                E += dE

    V_r.plot(rf, V)    # 在 V-r 圖上畫一個點
    E_r.plot(rf, E.mag)   # 在 E-r 圖上畫一個點

    rate(1000)   # 更新畫面，裡面的數字是【希望】電腦可以每秒更新

    print(f"{rf}:{V}", file=output_potent)  # 印出距離與電位勢
    print(f"{rf}:{E.mag}", file=output_field)  # 印出距離與電場

    # 當距離剛好在球體的半徑上，需要納入考慮嗎？
    if rf > R:  # 距離外
        stdev_v_out.append(V*rf)
        stdev_e_out.append(E.mag*rf*rf)
    elif rf < R and rf != 1e-10:  # 距離內與不是在距離超小的時候
        # 如果把 rf == 1e-10 ，值會非常大
        stdev_v_in.append(V*1/-(rf*rf))
        stdev_e_in.append(E.mag*1/rf)

# 印出球體外與球體內電場與電位勢的標準差
print("stdev_v_out:", statistics.stdev(stdev_v_out), sep="")
print("stdev_v_in:", statistics.stdev(stdev_v_in), sep="")
print("stdev_e_out:", statistics.stdev(stdev_e_out), sep="")
print("stdev_e_in:", statistics.stdev(stdev_e_in), sep="")

print("Done.")
