# 웹페이지 크롤링하여 책이미지 url csv파일로 저장하는 파일

import requests
import csv
from bs4 import BeautifulSoup

base_url = "https://www.aladin.co.kr/shop/common/wbest.aspx?BestType=YearlyBest&BranchType=1&CID=0&Year=2024&cnt=300&SortOrder=1&page={}"

headers = {"User-Agent": "Mozilla/5.0"}  # User-Agent 추가 (차단 방지)
csv_file = "book_image_urls.csv"

# CSV 파일 생성 및 헤더 작성
with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["book_img"])  # 헤더 작성

    for page in range(1, 7):  # page=1부터 page=6까지 반복
        url = base_url.format(page)
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # "frontcover" 클래스를 가진 이미지 태그 찾기
        book_images = [img["src"] for img in soup.select("img[class*='_cover']")]

        # CSV 파일에 이미지 URL 저장
        for img_url in book_images:
            writer.writerow([img_url])
            print(f"저장 완료: Page {page}, URL: {img_url}")

print(f"모든 이미지 URL이 {csv_file}에 저장되었습니다.")