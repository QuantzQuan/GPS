##########################################
# 1.please see the test site whether cite
# 2.please choose which site to show
# 3.please give the route of the html document
##########################################

import serial
import time
import folium
from selenium import webdriver

page = []
PAGE_RECEIVE = False
FIRST = 1  # temp value see result

# ##initialize serial
# under windows system
ser = serial.Serial("com3", 115200, timeout=0.5)
# # under raspy
# ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=0.5)
if ser.isOpen():
    ser.close()
ser.open()

# ##start driver
driver = webdriver.Chrome()

while True:
    # catch page
    while not PAGE_RECEIVE:
        ch = ser.read(1).decode(encoding="UTF-8", errors="ignore")
        if ch != '$':
            continue
        # else:
        #     ch = ser.read(1)
        line = ser.readline().decode(encoding="UTF-8", errors="ignore").strip()
        if line[0:5] == "GNGGA":
            page = []
        page.append(line)
        if line[0:5] == "GNTXT":
            # check data whether valid
            for line in enumerate(page):
                if (line[1][0] != "G") and (line[1][0] != "B"):
                    print("Format ERROR!")
                    page = []
                    break
                else:
                    PAGE_RECEIVE = True
            print("Page Success Receive!")

    # analysis data
    for line in page:
        if line[0:5] == "GNGGA":
            cur = line[5:].split(",")
            LATITUDE, HALF_LA, LONGITUDE, HALF_LO, PRECISION = cur[2], cur[3], cur[4], cur[5], cur[8]
            # print("GNGGA Location:\n")
            # print("维度：", LATITUDE, "南北半球：", HALF_LA, "经度：", LONGITUDE, "东西半球：", HALF_LO, "HDOP水平精度因子：", PRECISION)
        if line[0:5] == "GNRMC":
            cur = line[5:].split(",")
            STATE_STA, LATITUDE_GM, HALF_LA_GM, LONGITUDE_GM, HALF_LO_GM, NAVI_SPEED, NAVI_DIRECTION = \
                cur[2], cur[3], cur[4], cur[5], cur[6], cur[7], cur[8]
            print("GNRMC Location:\n")
            print("是否定位(A定位成功):", STATE_STA, "维度：", LATITUDE_GM, "南北半球：", HALF_LA_GM, "经度：", LONGITUDE_GM, "东西半球：",
                  HALF_LO_GM, "航速:", NAVI_SPEED, "航向角:", NAVI_DIRECTION)

    #######################################
    # ######### testing site############# #
    # LONGITUDE = "12029.27488"
    # LATITUDE = "3609.53500"
    # the site is in the OUC Information Department in Laoshan
    #######################################

    # Output in map to visualize
    if LATITUDE != '' and LONGITUDE != '' and LATITUDE_GM != '' and LONGITUDE_GM != '':
        print("Success Navi")
        # # use first site information
        # cur_LATITUDE = float(LATITUDE[0:2]) + float(LATITUDE[2:]) / 60
        # cur_LONGITUDE = float(LONGITUDE[0:3]) + float(LONGITUDE[3:]) / 60
        # use navigation recommend site information
        cur_LATITUDE = float(LATITUDE_GM[0:2]) + float(LATITUDE_GM[2:]) / 60
        cur_LONGITUDE = float(LONGITUDE_GM[0:3]) + float(LONGITUDE_GM[3:]) / 60
        print(cur_LATITUDE, cur_LONGITUDE)
        # map it
        map_info = folium.Map(location=[cur_LATITUDE, cur_LONGITUDE], zoom_start=20, control_scale=True)
        folium.Circle((cur_LATITUDE, cur_LONGITUDE), radius=7, color='yellow', fill=True, fill_color='red',
                      fill_opacity=0.7).add_to(map_info)
        folium.Marker(location=[cur_LATITUDE, cur_LONGITUDE], popup='点', icon=folium.Icon(icon='cloud')).add_to(
            map_info)
        map_info.add_child(folium.LatLngPopup())
        map_info.save('gps.html')
        if FIRST == 1:
            # please correct the route in your own computer
            driver.get('file://C:/Users/95414/Desktop/GPS/gps.html')
            FIRST = 0
        else:
            driver.refresh()

    # set time to refresh site
    time.sleep(5)
    PAGE_RECEIVE = False

