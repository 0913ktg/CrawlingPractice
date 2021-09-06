import os
import smtplib

from email.utils import formataddr
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders

from datetime import datetime

today = datetime.today()

from_addr = formataddr(('Google mail', '0913ktg@google.com'))
to_addr = formataddr(('Naver mail', '0913ktg@naver.com'))

#csv 파일이 존재하면 삭제시키기

#크롤러 실행 시키고 csv파일 저장

#저장된 csv파일을 가공

session = None
try:
    # SMTP 세션 생성
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.set_debuglevel(True)
    
    # SMTP 계정 인증 설정
    session.ehlo()
    session.starttls()
    session.login('0913ktg@gmail.com', 'wpcpcigkoevzktfk')
 
    # 메일 콘텐츠 설정
    message = MIMEMultipart("alternative")
    
    # 메일 송/수신 옵션 설정
    message.set_charset('utf-8')
    message['From'] = from_addr
    message['To'] = to_addr
    message['Subject'] = f'{today.year}년{today.month}월{today.day}일 게임 매출 순위 보고서'
 
    # 메일 콘텐츠 - 내용
    body = '''
    <h4>안녕하세요 김대겸입니다.</h4>
    <p>Google play KR 과 App Store CN의 매출 순위 Top 50을 csv파일로 전송합니다.</p>
    '''
    bodyPart = MIMEText(body, 'html', 'utf-8')
    message.attach( bodyPart )

    #메일 콘텐츠 - 첨부파일
    
    filename = 'task1.csv'
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