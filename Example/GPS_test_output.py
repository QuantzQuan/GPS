from GPS_Package import get_gps_data, draw_map
import time

if __name__ == '__main__':
    while True:
        cur_LATITUDE, cur_LONGITUDE, cur_LATITUDE_GM, cur_LONGITUDE_GM, NAVI_SPEED, NAVI_DIRECTION = get_gps_data(
            "com3")
        if cur_LATITUDE == '' and cur_LONGITUDE == '' and cur_LATITUDE_GM == '' and cur_LONGITUDE_GM == '':
            continue
        print(cur_LATITUDE, cur_LONGITUDE, cur_LATITUDE_GM, cur_LONGITUDE_GM, NAVI_SPEED, NAVI_DIRECTION)
        # set time to refresh site
        time.sleep(0.5)
