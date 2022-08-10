from GPS_Package import get_gps_data, init_serial
import time
import socket

RECEIVE_NUM = "192.168.50.103"

if __name__ == '__main__':
    SER = init_serial("com8")
    while True:
        try:
            raw_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            receive_code = (RECEIVE_NUM, 2000)
            cur_LATITUDE, cur_LONGITUDE, cur_LATITUDE_GM, cur_LONGITUDE_GM, NAVI_SPEED, NAVI_DIRECTION = get_gps_data(
                SER)
            cur_LATITUDE = round(cur_LATITUDE, 6)
            cur_LONGITUDE = round(cur_LONGITUDE, 6)
            cur_LATITUDE_GM = round(cur_LATITUDE_GM, 6)
            cur_LONGITUDE_GM = round(cur_LONGITUDE_GM, 6)
            NAVI_SPEED = round(NAVI_SPEED, 6)
            NAVI_DIRECTION = round(NAVI_DIRECTION, 6)
            print(cur_LATITUDE, cur_LONGITUDE, cur_LATITUDE_GM, cur_LONGITUDE_GM, NAVI_SPEED, NAVI_DIRECTION)
            raw_socket.sendto(str(cur_LATITUDE).encode() + b','
                              + str(cur_LONGITUDE).encode() + b','
                              + str(cur_LATITUDE_GM).encode() + b','
                              + str(cur_LONGITUDE_GM).encode() + b','
                              + str(NAVI_SPEED).encode() + b','
                              + str(NAVI_DIRECTION).encode()
                              , receive_code)
            # set time to refresh site
            time.sleep(0.5)
        except KeyboardInterrupt:
            SER.close()
        else:
            continue
