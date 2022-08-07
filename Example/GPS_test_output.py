from ..GPS_Package import get_gps_data, init_serial
import time

if __name__ == '__main__':
    SER = init_serial("com7")
    while True:
        try:
            cur_LATITUDE, cur_LONGITUDE, cur_LATITUDE_GM, cur_LONGITUDE_GM, NAVI_SPEED, NAVI_DIRECTION = get_gps_data(
                SER)
            print(cur_LATITUDE, cur_LONGITUDE, cur_LATITUDE_GM, cur_LONGITUDE_GM, NAVI_SPEED, NAVI_DIRECTION)
            # set time to refresh site
            time.sleep(0.5)
        except:
            continue
