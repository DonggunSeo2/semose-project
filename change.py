import requests

def get_lat_lng_from_address(address, api_key="AIzaSyAGWaw80N-4bPYXLZjtep8SW6Gs5HxE1pA"):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": api_key,
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        lat = location['lat']
        lng = location['lng']
        return lat, lng
    else:
        return None

if __name__ == "__main__":
  # 본인의 Google Geocoding API 키로 대체

    address = "인계동 374-7"
    latitude, longitude = get_lat_lng_from_address(address)

    if latitude and longitude:
        print(f"주소: {address}")
        print(f"위도: {latitude}")
        print(f"경도: {longitude}")
    else:
        print("위도와 경도를 가져올 수 없습니다.")