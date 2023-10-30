import math

def haversine(lat1, lon1, lat2, lon2):
    # 지구의 반지름 (킬로미터)
    radius = 6371

    # 위도 및 경도를 라디안으로 변환
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Haversine 공식을 사용하여 두 지점 간의 거리 계산
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = radius * c

    return distance

def change_min(lat1, lon1, lat2, lon2): # 도보 걸음걸이 속도 = 67m/min
    distance = haversine(lat1, lon1, lat2, lon2)
    min_ = distance * 1000 / 67
    return min_