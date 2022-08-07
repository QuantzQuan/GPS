##########################################
# 1.please see the test site whether cite
# 2.please choose which site to show
# 3.please give the route of the html document
##########################################

import serial
import time

LATITUDE, LONGITUDE, LATITUDE_GM, LONGITUDE_GM = "", "", "", ""
cur_LATITUDE, cur_LONGITUDE, cur_LATITUDE_GM, cur_LONGITUDE_GM, NAVI_SPEED, NAVI_DIRECTION = 0, 0, 0, 0, 0, 0


def init_serial(com="com7"):
    # ##initialize serial
    # under windows system
    ser = serial.Serial(com, 115200, timeout=0.5)
    # # under raspy
    # ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=0.5)
    return ser


def get_gps_data(ser=None):
    global LATITUDE, LONGITUDE, LATITUDE_GM, LONGITUDE_GM
    global cur_LATITUDE, cur_LONGITUDE, cur_LATITUDE_GM, cur_LONGITUDE_GM, NAVI_SPEED, NAVI_DIRECTION
    page = []
    PAGE_RECEIVE = False

    if ser.isOpen():
        ser.close()
    ser.open()

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
                    # print("Format ERROR!")
                    page = []
                    break
                else:
                    PAGE_RECEIVE = True
            # print("Page Success Receive!")

    # clear all input wait next time
    ser.flushInput()

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
            # print("GNRMC Location:\n")
            # print("是否定位(A定位成功):", STATE_STA, "维度：", LATITUDE_GM, "南北半球：", HALF_LA_GM, "经度：", LONGITUDE_GM, "东西半球：",
            #       HALF_LO_GM, "航速:", NAVI_SPEED, "航向角:", NAVI_DIRECTION)
    #######################################
    # ######### testing site############# #
    # LONGITUDE = "12029.27488"
    # LATITUDE = "3609.53500"
    # the site is in the OUC Information Department in Laoshan
    #######################################
    if LATITUDE != '' and LONGITUDE != '' and LATITUDE_GM != '' and LONGITUDE_GM != '':
        # print("Success Navi")
        # use first site information
        cur_LATITUDE = float(LATITUDE[0:2]) + float(LATITUDE[2:]) / 60
        cur_LONGITUDE = float(LONGITUDE[0:3]) + float(LONGITUDE[3:]) / 60
        # use navigation recommend site information
        cur_LATITUDE_GM = float(LATITUDE_GM[0:2]) + float(LATITUDE_GM[2:]) / 60
        cur_LONGITUDE_GM = float(LONGITUDE_GM[0:3]) + float(LONGITUDE_GM[3:]) / 60
    else:
        LATITUDE = LONGITUDE = LATITUDE_GM = LONGITUDE_GM = 0
    if NAVI_SPEED != "" and NAVI_DIRECTION != "":
        NAVI_SPEED = float(NAVI_SPEED)
        NAVI_DIRECTION = float(NAVI_DIRECTION)
    else:
        NAVI_SPEED = NAVI_DIRECTION = 0
    # close serial
    if ser.isOpen():
        ser.close()
    return cur_LATITUDE, cur_LONGITUDE, cur_LATITUDE_GM, cur_LONGITUDE_GM, NAVI_SPEED, NAVI_DIRECTION


if __name__ == '__main__':
    SER = init_serial("com7")
    while True:
        cur_LATITUDE, cur_LONGITUDE, cur_LATITUDE_GM, cur_LONGITUDE_GM, NAVI_SPEED, NAVI_DIRECTION = get_gps_data(
            SER)
        print(cur_LATITUDE, cur_LONGITUDE, cur_LATITUDE_GM, cur_LONGITUDE_GM, NAVI_SPEED, NAVI_DIRECTION)
        if cur_LATITUDE == '' and cur_LONGITUDE == '' and cur_LATITUDE_GM == '' and cur_LONGITUDE_GM == '':
            continue
        # set time to refresh site
        time.sleep(1)
