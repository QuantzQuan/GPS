import folium
from selenium import webdriver

FIRST = 1  # temp value see result


def draw_map(html_route='file://C:/Users/95414/OneDrive/BDS_Code/GPS/Example/gps.html', is_first=FIRST,
             cur_LATITUDE=None, cur_LONGITUDE=None):
    # start driver
    driver = webdriver.Chrome()
    # Output in map to visualize
    # map it
    map_info = folium.Map(location=[cur_LATITUDE, cur_LONGITUDE], zoom_start=20, control_scale=True)
    folium.Circle((cur_LATITUDE, cur_LONGITUDE), radius=7, color='yellow', fill=True, fill_color='red',
                  fill_opacity=0.7).add_to(map_info)
    folium.Marker(location=[cur_LATITUDE, cur_LONGITUDE], popup='点', icon=folium.Icon(icon='cloud')).add_to(
        map_info)
    map_info.add_child(folium.LatLngPopup())
    map_info.save('gps.html')
    if is_first == 1:
        # please correct the route in your own computer
        driver.get(html_route)
        is_first = 0
    else:
        driver.refresh()
    return is_first
