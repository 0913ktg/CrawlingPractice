import os
import glob
import smtplib
import time
import pandas as pd
from datetime import datetime
import pytz

from email.utils import formataddr
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders


def run_crawler():
    today = datetime.today()

    from_addr = formataddr(('Google mail', "your mail address"))
    to_addr = formataddr(('Naver mail', "customer's mail address"))

    #csv 파일이 존재하면 삭제시키기
    [os.remove(f) for f in glob.glob("./asset/*csv")]

    #크롤러 실행 시키고 csv파일 저장
    path = os.getcwd()
    os.chdir(path)
    os.system("scrapy crawl task1 -o asset/task1.csv -t csv")
    time.sleep(40)

    #저장된 csv파일을 가공
    source = pd.read_csv('asset/task1.csv', encoding = 'utf-8')
    korea = source[source['country'] == 'korea'].iloc[:50]
    china = source[source['country'] == 'china'].iloc[:50]
    korea = korea.reset_index(drop=True)
    china = china.reset_index(drop=True)
    korea.index += 1
    china.index += 1
    korea.to_csv("asset/korea.csv", encoding='utf-8')
    china.to_csv("asset/china.csv", encoding='utf-8')

    session = None
    try:
        # SMTP 세션 생성
        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.set_debuglevel(True)

        # SMTP 계정 인증 설정
        session.ehlo()
        session.starttls()
        session.login("your mail address", "your google Authentication key")

        # 메일 콘텐츠 설정
        message = MIMEMultipart("alternative")

        # 메일 송/수신 옵션 설정
        message.set_charset('utf-8')
        message['From'] = from_addr
        message['To'] = to_addr
        message['Subject'] = f'{today.year}년{today.month}월{today.day}일 게임 매출 순위 보고서'

        # 메일 콘텐츠 - 내용
        body = '''
        <h4>안녕하세요 [your name]입니다.</h4>
        <p>Google play KR 과 App Store CN의 매출 순위 Top 50을 csv파일로 전송합니다.</p>
        <h4>파일 보는 순서</h4>
        <p>1. 엑셀 실행 후 상단바에서 데이타 -> 텍스트/CSV 선택</p>
        <p>2. 가져올 파일 선택 후 확인 클릭</p>
        <p>3. 파일 원본 라벨 밑 한국어 클릭 -> 유니코드 (UTF-8) 선택</p>
        <p>4. 우측 하단에 로드 버튼 클릭</p>
        '''
        bodyPart = MIMEText(body, 'html', 'utf-8')
        message.attach( bodyPart )

        #메일 콘텐츠 - 첨부파일
        filenames = ['asset/korea.csv', 'asset/china.csv']

        for filename in filenames:
            attachment = open(filename, 'rb')

            part = MIMEBase('application','octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',"attachment", filename= os.path.basename(filename))
            message.attach(part)

        # 메일 발송
        session.sendmail(from_addr, to_addr, message.as_string())   
        print( 'Successfully sent the mail!!!' )
    except Exception as e:
        print( e )
    finally:
        if session is not None:
            session.quit()
            
            
if __name__ == "__main__":
    
    KTZ = pytz.timezone('Asia/Seoul')         
    
    while(True):
        curr_time = datetime.now(KTZ)
        print(f'시각 : {curr_time.year}-{curr_time.month}-{curr_time.day}  {curr_time.hour} 시 {curr_time.minute} 분 {curr_time.second} 초')
        
        if curr_time.hour == 16 and curr_time.minute == 12:
            print('크롤링 시작')
            run_crawler()
            print('크롤링 끝')
            time.sleep(50)
        
        time.sleep(10)