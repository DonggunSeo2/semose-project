# 조건에 해당하는 데이터프레임 반환

# ----------- 예시 조건 ------------ 
# 클라이언트로부터 주소를 받음
# 클라이언트가 스타벅스, 맥도날드, 올리브영, 크린토피아를 선택함
import pandas as pd
import mysql.connector
from dis_min import haversine, change_min
from change import get_lat_lng_from_address

class QuerySemose:
    def __init__(self, host="jkkyui-MacBookPro.local", user="root", password="apdlvmf4@@", database="Semose_DB"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.tabel_name = "places"
    def get_info_condition(self, client_address, client_condition):
        # MySQL 서버에 연결
        connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

        # SQL 쿼리를 사용하여 데이터를 데이터프레임으로 가져옵니다.
        # 동적 쿼리 생성
        query_conditions = " OR ".join([f"place_name LIKE '%{item}%'" for item in client_condition])
        query = f"SELECT * FROM {self.tabel_name} WHERE {query_conditions}"

        # 거리 계산해서 distance에 반영
        df = pd.read_sql(query, connection)

        # 클라이언트로부터 입력받은 주소 위경도로 변환
        lat, lng = get_lat_lng_from_address(client_address)

        # 거리 계산
        df["distance"] = df.apply(lambda x: change_min(lat, lng, x["y"], x["x"]), axis=1)
        df = df.sort_values(by=["distance"])

        # 거리가 가까운 순으로 5개만 반환
        return df

test = QuerySemose()
test_df = test.get_info_condition("팔달구 인계동 374-7", ["스타벅스", "맥도날드", "올리브영", "크린토피아"])
print(test_df[['place_name','distance']])
