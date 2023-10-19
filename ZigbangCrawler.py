import requests
import pandas as pd
import geohash2
from geopy.geocoders import Nominatim
from haversine import haversine

geo_local = Nominatim(user_agent='South Korea')

# 위도, 경도 반환하는 함수
def geocoding(address):
    try:
        geo = geo_local.geocode(address)
        x_y = [geo.latitude, geo.longitude]
        return x_y

    except:
        return [0,0]

def oneroom(addr): # 주소 넣으면 정보 나오게 하기
    # 위 경도 가져오기
    lat, lng = geocoding(addr)
    
    # 지오해시로 영역확보
    geohash = geohash2.encode(lat, lng, precision=5)
    url = f"https://apis.zigbang.com/v2/items?deposit_gteq=0&domain=zigbang&geohash={geohash}&needHasNoFiltered=true&rent_gteq=0&sales_type_in=전세|월세&service_type_eq=원룸"
    response = requests.get(url)
    items = response.json()["items"]
    ids = [item["item_id"] for item in items] # 아이템 아이디 확보
    # https://apis.zigbang.com/v2/items/oneroom?geohash=wyd7&depositMin=0&rentMin=0&salesTypes%5B0%5D=%EC%A0%84%EC%84%B8&salesTypes%5B1%5D=%EC%9B%94%EC%84%B8&domain=zigbang&checkAnyItemWithoutFilter=true
    url = "https://apis.zigbang.com/v2/items/list"
    params = {
        "domain": "zigbang",
        "item_ids": ids[:900]
    }
    response = requests.post(url, params)
    items = response.json()['items']
    extracted_data = []

    # 캐올 칼럼 구성하기
    for item in items:
        extracted_data.append({
            'item_id': item['item_id'],
            'deposit': item.get('deposit', None),
            'rent': item.get('rent', None),
            '공급면적_p': item['공급면적']['p'] if '공급면적' in item and 'p' in item['공급면적'] else None,
            'building_floor': item.get('building_floor', None),
            'floor': item.get('floor', None),
            'lat': item['random_location']['lat'] if 'random_location' in item and 'lat' in item['random_location'] else None,
            'lng': item['random_location']['lng'] if 'random_location' in item and 'lng' in item['random_location'] else None,
            'reg_date': item.get('reg_date', None),
            'sales_type': item.get('sales_type', None),
            'manage_cost' : item.get('manage_cost', None)
        })
    df = pd.DataFrame(extracted_data)

    # 학교와의 거리 기준으로 필터링 계산
    df['distance'] = df.apply(lambda x: haversine((lat, lng), (x['lat'], x['lng']), unit= 'm'), axis=1)    
    df = df[df['distance'] < 2000]
    print(df)
    return df

test = oneroom('아주대학교')

