import numpy as np
import pandas as pd
from urllib.request import urlopen
from urllib import parse
from urllib.request import Request
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import json

# naver api
my_id = "id"
pw = "password"

api_url = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query="

# 주소 목록 파일
data = pd.read_excel("C:/Users/Administrator/Desktop/기획/naver api/sample주소.xlsx", usecols="B", names=["도로명주소"])

# api 호출해서 위도 경도 get

geo_coord = [] 

for add in data["도로명주소"]:
    add_url = parse.quote(add)
    url = api_url+add_url
    request = Request(url)
    request.add_header("X-NCP-APIGW-API-KEY-ID", my_id)
    request.add_header("X-NCP-APIGW-API-KEY", pw)
    try:
        response = urlopen(request)
    except HTTPError as e:
        print("HTTP Error")
        lat = None
        longi = None
    else:
        rescode = response.getcode()
        if rescode==200:
            # 정상 200
            response_body = response.read().decode("utf-8")
            response_body = json.loads(response_body)
            if "addresses" in response_body:
                lat = response_body["addresses"][0]['y']
                longi = response_body["addresses"][0]['x']
                print("성공")
            else:
                print("결과없음.")
                lat = None
                longi = None
        else:
            print("response error code : %d" %rescode)
            lat = None
            longi = None
            
    geo_coord.append([lat, longi])
    
np_geo_coordi = np.array(geo_coord)
pd_geo_coordi = pd.DataFrame({"도로명": data["도로명주소"].values, "위도": np_geo_coordi[:, 0], "경도": np_geo_coordi[:, 1]})

# 저장
writer = pd.ExcelWriter("output2.xlsx")
pd_geo_coordi.to_excel(writer, sheet_name = "Sheet1")
writer.save()



