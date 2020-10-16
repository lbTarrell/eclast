from __future__ import print_function
from flask import Flask, render_template, request
import pickle
import numpy as np
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
import pandas as pd
import os
import matplotlib
from numpy import random
matplotlib.use('nbAgg')
import matplotlib.pyplot as plt
import sys
import shutil
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from flask import Flask, flash, redirect, render_template, request, session, abort
app=Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == '111' and request.form['username'] == 'ecadmin':
         session['logged_in'] = True
         return render_template("home.html")
    else:
        flash('wrong password!')
        return render_template('login.html')

def ValuePredictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1,8)
    to_predict1 = loaded_model1.transform(to_predict)
    result = loaded_model.predict(to_predict1)
    return result[0]

@app.route('/result',methods = ['POST'])
def result():
    prediction=''
    if request.method == 'POST':
        df=pd.read_csv('c21.csv')
        df=df.fillna('/')
        to_predict_list = request.form.to_dict()
        print(to_predict_list.values())

        print('hi',str(to_predict_list['za']))
        df=df.loc[df.中標公司.str.contains(to_predict_list['z'])]
        df=df.iloc[::-1]
        try:
            type1=df.裝修設計公司.values[0]
        except:
            type1=0
        df=df.drop(columns='裝修設計公司')
        #df.set_index('工程日期')
        df1=pd.read_csv('v100.csv')
        df1=df1.loc[df1.裝修公司名.str.contains(to_predict_list['z'])]
        try:
            price=df1.價錢.values[0]
        except:
            price='沒有記錄'
        try:
            feature=df1.特色.values[0]
        except:
            feature='沒有記錄'
        try:
            contact=df1.聯諾人.values[0]
        except:
            contact='沒有記錄'
        try:
            contactnum=df1.電話.values[0]
        except:
            contactnum='沒有記錄'
        try:
            losing=df1.失效日期.values[0]
        except:
            losing='沒有記錄'
        try:
            typez=df1['設計/裝修/師傅'].values[0]
        except:
            typez='沒有記錄'
        prediction=df.groupby(['中標公司','工程日期','單位']).first().sort_values('進度',ascending=False)
        try:
            nam=df.中標公司.values[0]
        except:
            nam='沒有記錄'
        name='裝修公司：'+str(nam)+' ('+'失效日:'+str(losing)+')'
        address='地址：'+''
        try:
            donenumber=prediction.進度.value_counts()['進行中']
        except:
            donenumber=0
        try:
            donenumber1=prediction.進度.value_counts()['已完成']
        except:
            donenumber1=0
        donenumber='進行中：'+ str(donenumber)+'單'+' ｜ 己完成：'+str(donenumber1)+'單'
      
        type1='裝修｜設計：'+str(typez)+' ('+'價錢:'+str(price)+')'
     
        feature='特色：'+str(feature)
        contact='聯絡人：'+str(contact)+' ('+'電話:'+str(contactnum)+')'
        contactnum='電話：'+str(contactnum)

        
        if str(to_predict_list['za'])=='進行中':
            df['工程日期'] = pd.to_datetime(df['工程日期'], format="%d/%m/%Y")
            prediction=df.loc[df.進度=='進行中']
            prediction=prediction.groupby(['中標公司','工程日期','單位']).first().sort_values(['進度','工程日期'],ascending=[False,False])


        elif str(to_predict_list['za'])=='已完成':
            df['工程日期'] = pd.to_datetime(df['工程日期'], format="%d/%m/%Y")
            prediction=df.loc[df.進度=='已完成']
            prediction=prediction.groupby(['中標公司','工程日期','單位']).first().sort_values(['進度','工程日期'],ascending=[False,False])

        else:
            df['工程日期'] = pd.to_datetime(df['工程日期'], format="%d/%m/%Y")
            prediction=df.groupby(['中標公司','工程日期','單位']).first().sort_values(['進度','工程日期'],ascending=[False,False])

        return render_template("result.html",  tables=[prediction.to_html(classes='data')], titles=prediction.columns.values,address=address,donenumber=donenumber,name=name,feature=feature,contact=contact,contactnum=contactnum,type1=type1)
     

@app.route('/result1',methods = ['POST'])
def result1():
    prediction=''
    if request.method == 'POST':
        df=pd.read_csv('c21.csv')
        df=df.fillna('/')
        to_predict_list = request.form.to_dict()
        print(to_predict_list.values())

        
        df=df.loc[df.單位.str.contains(to_predict_list['z'])]
        df=df.iloc[::-1]
        #df=df.drop(columns='中單人')
        #df.set_index('工程日期')


        df1=pd.read_csv('v100.csv')
        
        for qa in range(len(df)):
            try:
                df2=df1.loc[df1.裝修公司名.str.contains(df['中標公司'][qa])]
                df2=df2.reset_index()
                df['裝修設計公司'][qa]=df2['設計/裝修/師傅'][0]

            except:
                df['裝修設計公司'][qa]='沒有記錄'
        prediction=df.groupby(['裝修設計公司','地區','中標公司']).first().sort_values('進度',ascending=False)
        try:
            decor=df.裝修設計公司.value_counts()['裝修公司']
        except:
            decor=0
        try:
            ren=df.裝修設計公司.value_counts()['設計公司']
        except:
            ren=0
        try:
            nam1=to_predict_list['z']
        except:
            nam1=0
        print(prediction)
        try:
            donenumber=prediction.進度.value_counts()['進行中']
        except:
            donenumber=0
        try:
            donenumber1=prediction.進度.value_counts()['已完成']
        except:
            donenumber1=0
        donenumber='進行中：'+ str(donenumber)+'單'+' ｜ 己完成：'+str(donenumber1)+'單'
    

        nam1='地區：'+ str(nam1)
        decor='裝修公司：'+ str(decor)+' ｜ 設計公司：'+str(ren)
        ren='待定'
        return render_template("result1.html",  tables=[prediction.to_html(classes='data')], titles=prediction.columns.values,decor=decor,ren=ren,nam1=nam1,donenumber=donenumber)
@app.route('/result9',methods = ['POST'])
def result9():
    prediction=''
    if request.method == 'POST':
        df=pd.read_csv('c21.csv')
        df=df.fillna('/')
        to_predict_list = request.form.to_dict()
        print(to_predict_list.values())

        
        df=df.loc[df.單位.str.contains(to_predict_list['parch'])]
        df=df.iloc[::-1]
        #df=df.drop(columns='中單人')
        #df.set_index('工程日期')
 
        prediction=df.groupby(['裝修設計公司','中標公司']).first()
        try:
            decor=df.裝修設計公司.value_counts()['裝修公司']
        except:
            decor=0
        try:
            ren=df.裝修設計公司.value_counts()['設計公司']
        except:
            ren=0
        try:
            nam1=to_predict_list['z']
        except:
            nam1=0
        print(prediction)
        try:
            donenumber=prediction.進度.value_counts()['進行中']
        except:
            donenumber=0
        try:
            donenumber1=prediction.進度.value_counts()['已完成']
        except:
            donenumber1=0
        donenumber='進行中數量：'+ str(donenumber)
        donenumber1='己完成數量：'+str(donenumber1)
        nam1='地區：'+ str(nam1)
        decor='裝修公司數量：'+ str(decor)
        ren='設計公司數量：'+str(ren)
        
        print(prediction)
        return render_template("result1.html",  tables=[prediction.to_html(classes='data')], titles=prediction.columns.values,decor=decor,ren=ren,nam1=nam1,donenumber=donenumber,donenumber1=donenumber1)

@app.route('/result2',methods = ['POST'])
def result2():
    prediction=''
    if request.method == 'POST':
        df=pd.read_csv('c21.csv')
        df=df.fillna('/')
        to_predict_list = request.form.to_dict()
        print(to_predict_list.values())

        
        df=df.loc[df.中單人.str.contains(to_predict_list['z'],case=False)]
        df=df.iloc[::-1]
        df=df.reset_index()
        for e in range(len(df)):
            df['中單人'][e]=df['中單人'][e].replace('Kit','KIT')
            
        df=df.drop(columns=['index','裝修設計公司'])
        df['簽單月份']=pd.to_datetime(df['簽單月份'], format="%m/%Y").dt.to_period('m')

        # df1=pd.read_csv('/Users/lota/Downloads/passwordtest/v100.csv')
        # for qa in range(len(df)):
        #     try:
        #         df2=df1.loc[df1.裝修公司名.str.contains(df['中標公司'][qa])]
        #         df2=df2.reset_index()
        #         df['裝修設計公司'][qa]=df2['設計/裝修/師傅'][0]

        #     except:
        #         df['裝修設計公司'][qa]='沒有記錄'
        

        try:
            totl=df.裝修設計公司.count()
        except:
            totl=0
        try:
            donenumber=df.進度.value_counts()['進行中']
        except:
            donenumber=0
        try:
            donenumber1=df.進度.value_counts()['已完成']
        except:
            donenumber1=0
        finn=donenumber+donenumber1
        donenumber='進行中：'+ str(donenumber)+'單'+' ｜ 己完成：'+str(donenumber1)+'單'
        totl='中單總數量：'+ str(finn)+'單'
        nnnna='同事：'+ str(to_predict_list['z'])
        summm='中單總額：'+str(round(sum(df.價錢)))+'萬'


        if str(to_predict_list['za'])=='進行中':
            prediction=df.loc[df.進度=='進行中']
            prediction=prediction.groupby(['簽單月份','單位']).first().sort_values(['進度','簽單月份'],ascending=[False,False])


        elif str(to_predict_list['za'])=='已完成':
            prediction=df.loc[df.進度=='已完成']
            prediction=prediction.groupby(['簽單月份','單位']).first().sort_values(['進度','簽單月份'],ascending=[False,False])

        else:
            prediction=df
            prediction=prediction.groupby(['簽單月份','單位']).first().sort_values(['進度','簽單月份'],ascending=[False,False])

        return render_template("result2.html",summm=summm,nnnna=nnnna,donenumber=donenumber,  tables=[prediction.to_html(classes='data')], titles=prediction.columns.values,totl=totl)
@app.route('/selelogin',methods = ['POST'])
def selelogin():
    prediction=''
    if request.method == 'POST':

        to_predict_list = request.form.to_dict()
     
        options = webdriver.ChromeOptions();
        options.add_argument('--user-data-dir=./Tem')
        driver = webdriver.Chrome('./templates/chromedriver-2',chrome_options=options)

        driver.get('https://web.whatsapp.com/send?phone=852'+to_predict_list['z']+'&text=你好，非常感謝使用EcHouse裝修配對服務。')
      
        return render_template("sele.html")
@app.route('/sele',methods = ['POST'])
def sele():
    prediction=''
    if request.method == 'POST':

        to_predict_list = request.form.to_dict()
     
        options = webdriver.ChromeOptions();
        options.add_argument('--user-data-dir=./Tem')
        driver = webdriver.Chrome('./templates/chromedriver-2',chrome_options=options)

        driver.get('https://web.whatsapp.com/send?phone=852'+to_predict_list['z']+'&text=你好，非常感謝使用EcHouse裝修配對服務。')
      
        return render_template("sele.html")
@app.route('/result30',methods = ['POST'])
def result30():
    prediction=''
    if request.method == 'POST':
        shutil.rmtree('./static/image', ignore_errors=True)
        os.mkdir('./static/image')
        
        #df=pd.read_excel('ecformnew.xlsx')
        
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

        # The ID and range of a sample spreadsheet.
        SAMPLE_SPREADSHEET_ID = '1U21R5n8dbn6MbzYQj3QjMXFcd4w2hoFYaUtU7S1PnS8'


        SAMPLE_RANGE_NAMEcog = 'cog!A:Q'
        coglis=[]
        coglis1=[]
        cogdi={}
        def cogmain():
                    """Shows basic usage of the Sheets API.
                    Prints values from a sample spreadsheet.
                    """
                    cnt=1
                    
                    
                    creds = None
                    # The file token.pickle stores the user's access and refresh tokens, and is
                    # created automatically when the authorization flow completes for the first
                    # time.
                    if os.path.exists('./token.pickle'):
                        with open('./token.pickle', 'rb') as token:
                            creds = pickle.load(token)
                    # If there are no (valid) credentials available, let the user log in.
                    if not creds or not creds.valid:
                        if creds and creds.expired and creds.refresh_token:
                            creds.refresh(Request())
                        else:
                            flow = InstalledAppFlow.from_client_secrets_file('./credentials.json', SCOPES)
                            creds = flow.run_local_server(port=0)
                        # Save the credentials for the next run
                        with open('./token.pickle', 'wb') as token:
                            pickle.dump(creds, token)

                    service = build('sheets', 'v4', credentials=creds)

                    # Call the Sheets API
                    sheet = service.spreadsheets()
                    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                                range=SAMPLE_RANGE_NAMEcog).execute()
                    values = result.get('values', [])

                    if not values:
                        print('No data found.')
                    else:
                        for row in values:
                            if cnt==1:
                                coglis.extend(row)
                                cnt+=1
                            else:
                                coglis1.append(row)
                    
                    for i in range(len(coglis1)):

                        cogdi.update({str(i):coglis1[i]})

        cogmain()

        df=pd.DataFrame.from_dict(cogdi, orient='index',columns=coglis)

        for e in range(len(df)):
                df['EcHouse免費裝修報價_Id'][e]=df['EcHouse免費裝修報價_Id'][e].replace('1-','')
                df['性別'][e]=df['性別'][e].replace('TRUE','Male')
                df['性別'][e]=df['性別'][e].replace('FALSE','Female')
                
        df['Entry_DateSubmitted']=pd.to_datetime(df['Entry_DateSubmitted'],utc=True)

        nuuu=['EcHouse免費裝修報價_Id',  '房', '廳']

        for bz in range(len(nuuu)):
            df[nuuu[bz]]=pd.to_numeric(df[nuuu[bz]])
            
        
        to_predict_list = request.form.to_dict()
        

        import datetime
        yea=int(to_predict_list['z']) #forinput
        mon=int(to_predict_list['za'])  #forinput
        dat=31
        tt=df.loc[df['Entry_DateSubmitted'].dt.date>=datetime.date(yea, mon, 1)]
        for i in range(7):
            try:
                tt=tt.loc[tt['Entry_DateSubmitted'].dt.date<=datetime.date(yea, mon, dat)]
                break
            except:
                dat-=1

        df1=pd.read_excel('comdecoform1.xlsx')
        dat=31
        df1=df1.loc[df1['Entry_DateSubmitted'].dt.date>=datetime.date(yea, mon, 1)]
        for i in range(7):
            try:
                df1=df1.loc[df1['Entry_DateSubmitted'].dt.date<=datetime.date(yea, mon, dat)]
                break
            except:
                dat-=1
        tt=tt.drop_duplicates('聯絡電話')
        df1=df1.drop_duplicates('電話')
        try:
            gog=tt.如何找到我們.str.count('Google').sum()
        except:
            gog=0
   
        try:
            facebook=tt.如何找到我們.str.count('Facebook').sum()
        except:
            facebook=0

        try:
            yahoo=tt.如何找到我們.str.count('Yahoo').sum()
        except:
            yahoo=0
       
        try:
            instagram=tt.如何找到我們.str.count('Instagram').sum()
        except:
            instagram=0

        try:
            friend=tt.如何找到我們.str.count('朋友介紹').sum()
        except:
            friend=0
    
        try:
            forum=tt.如何找到我們.str.count('論壇').sum()
        except:
            forum=0

        try:
            youtube=tt.如何找到我們.str.count('Youtube').sum()
        except:
            youtube=0
   
        try:
            other=tt.如何找到我們.str.count('其他').sum()
        except:
            other=0
        try:
            news=tt.如何找到我們.str.count('新聞').sum()
        except:
            news=0
        try:
            partial=tt.全部局部.str.count('局部裝修').sum()
        except:
            partial=0

        try:
            alll=tt.全部局部.str.count('全部裝修').sum()
        except:
            alll=0    

        try:
            onehundred=tt.預算.str.count('以上').sum()
        except:
            onehundred=0

        try:
            fifty=tt.預算.str.count('50萬 ').sum()
        except:
            fifty=0
        
        try:
            forty=tt.預算.str.count('40萬 ').sum()
        except:
            forty=0
  
        try:
            thirty=tt.預算.str.count('30萬 ').sum()
        except:
            thirty=0
  
        try:
            twenty=tt.預算.str.count('20萬 ').sum()
        except:
            twenty=0
  
        try:
            ten=tt.預算.str.count('10萬 ').sum()
        except:
            ten=0
 
        try:
            fivetten=tt.預算.str.count(' 10萬').sum()
        except:
            fivetten=0

        try:
            fiveb=tt.預算.str.count('以下').sum()
        except:
            fiveb=0

         #reward
         
        try:
            kit=tt.負責人.str.contains('kit',case=False).sum()-tt.負責人.str.contains('kit cancel',case=False).sum()
            kitreward=tt.負責人.str.contains('kit獎',case=False).sum()+tt.負責人.str.contains('kit 獎',case=False).sum()
        except:
            kit=0

        try:
            king=tt.負責人.str.contains('king',case=False).sum()-tt.負責人.str.contains('king cancel',case=False).sum()
            kingreward=tt.負責人.str.contains('king獎',case=False).sum()+tt.負責人.str.contains('king 獎',case=False).sum()
        except:
            king=0
  
        try:
            wil=tt.負責人.str.contains('wil',case=False).sum()-tt.負責人.str.contains('wil cancel',case=False).sum()
            wilreward=tt.負責人.str.contains('wil獎',case=False).sum()+tt.負責人.str.contains('wil 獎',case=False).sum()
        except:
            wil=0

        try:
            yin=tt.負責人.str.contains('yin',case=False).sum()-tt.負責人.str.contains('yin cancel',case=False).sum()
            yinreward=tt.負責人.str.contains('yin獎',case=False).sum()+tt.負責人.str.contains('yin 獎',case=False).sum()
        except:
            yin=0


        try:
            fiona=tt.負責人.str.contains('fiona',case=False).sum()-tt.負責人.str.contains('fiona cancel',case=False).sum()
            fionareward=tt.負責人.str.contains('fiona獎',case=False).sum()+tt.負責人.str.contains('fiona 獎',case=False).sum()
        except:
            fiona=0
      

        try:
            ecc=tt.負責人.str.contains('ec',case=False).sum()-tt.負責人.str.contains('ec cancel',case=False).sum()
        except:
            ecc=0

        #totalnumberplot
        q2=random.randint(1000000000000000)
        ax1=pd.DataFrame({'Type':['Below 5','5-10','10-20','20-30','30-40','40-50','50-100','100 Up'],'Amount':[fiveb,fivetten,ten,twenty,thirty,forty,fifty,onehundred]}).groupby(['Type'],sort=False).sum().unstack().plot(kind='bar',title=str(yea)+'-'+str(mon)+' Type Order Amounts',color=['red','green','blue','yellow','pink','black','purple','grey'],alpha=0.5)
        ax1.set_xticklabels(['Below 5','5-10','10-20','20-30','30-40','40-50','50-100','100 Up'], rotation=360)
        ax1.get_figure().savefig("./static/image/a"+str(q2)+".png", transparent=True)

        plt.close()


        #inchargeplot

        ax2=pd.DataFrame({'Colleague':['Kit','King','Wilson','Yin','Fiona','EC'],'Amount':[kit,king,wil,yin,fiona,ecc]}).groupby(['Colleague'],sort=False).sum().unstack().plot(kind='bar',title=str(yea)+'-'+str(mon)+' Colleague Order Amounts',color=['red','green','blue','yellow','pink','black'],alpha=0.5)
        ax2.set_xticklabels(['Kit','King','Wilson','Yin','Fiona','EC'], rotation=360)
        ax2.get_figure().savefig("./static/image/b"+str(q2)+".png", transparent=True)

        plt.close()

        #contype
 
        ax3=pd.DataFrame({'Type':['Full Construction','Partial Construction'],'Amount':[alll,partial]}).groupby(['Type'],sort=False).sum().unstack().plot(kind='bar',title=str(yea)+'-'+str(mon)+' Type of Construction Amount',color=['red','green'],alpha=0.5)
        ax3.set_xticklabels(['Full Construction','Partial Construction'], rotation=360)
        ax3.get_figure().savefig("./static/image/d"+str(q2)+".png", transparent=True)

        plt.close()


        #mediatype

        ax4=pd.DataFrame({'Source':['Google','FB','Yahoo','IG','Friend','Youtube','Forum','News','Others'],'Amount':[gog,facebook,yahoo,instagram,friend,youtube,forum,news,other]}).groupby(['Source'],sort=False).sum().unstack().plot(kind='bar',title=str(yea)+'-'+str(mon)+' Type of Marketing Source Amount',color=['red','green','blue','yellow','pink','black','purple','grey','orange'],alpha=0.5)
        ax4.set_xticklabels(['Google','FB','Yahoo','IG','Friend','Youtube','Forum','News','Others'], rotation=360)
        ax4.get_figure().savefig("./static/image/e"+str(q2)+".png", transparent=True)

        plt.close()
        


        totalorder=str(tt.shape[0])
        totalorder0=to_predict_list['z']+'年'+to_predict_list['za']+'月總單量'
        tim='選擇日期：'+to_predict_list['z']+'年'+to_predict_list['za']+'月'

        prediction=pd.DataFrame({' ':['Cog Form'],totalorder0:[totalorder],'全部裝修':[alll],'局部裝修':[partial],'5萬以下':[fiveb],'5萬-10萬':[fivetten],'10萬-20萬':[ten],'20萬-30萬':[twenty],'30萬-40萬':[thirty],'40萬-50萬':[forty],'50萬-100萬':[fifty],'100萬以上':[onehundred]})
        #prediction.index.name='Cog Form'
        prediction=prediction.set_index([' '])

        prediction1=pd.DataFrame({' ':['派單量'],'Kit':[kit],'King':[king],'Wilson':[wil],'Yin':[yin],'Fiona':[fiona],'Ec':[ecc],'總數量':[kit+king+wil+yin+fiona+ecc]})
        prediction1=prediction1.set_index([' '])


        #rewarddataframe
        predictionreward=pd.DataFrame({' ':['獎'],'Kit':[kitreward],'King':[kingreward],'Wilson':[wilreward],'Yin':[yinreward],'Fiona':[fionareward],'總數量':[kitreward+kingreward+wilreward+yinreward+fionareward]})
        predictionreward=predictionreward.set_index([' '])

        #more detail in colleague with money
        namee=['kit','king','wil','yin','fiona','ec']
        moneyy=['以下',' 10萬','10萬 ','20萬 ','30萬 ','40萬 ','50萬 ','以上']
        su=[]
        for ii in range(len(namee)):
            for bb in range(len(moneyy)):
                su.append(tt.loc[tt.負責人.str.contains(namee[ii],case=False,na=False)].預算.str.count(moneyy[bb]).sum())
        sum1=su[0]+su[8]+su[16]+su[24]+su[32]+su[40]
        sum2=su[1]+su[9]+su[17]+su[25]+su[33]+su[41]
        sum3=su[2]+su[10]+su[18]+su[26]+su[34]+su[42]
        sum4=su[3]+su[11]+su[19]+su[27]+su[35]+su[43]
        sum5=su[4]+su[12]+su[20]+su[28]+su[36]+su[44]
        sum6=su[5]+su[13]+su[21]+su[29]+su[37]+su[45]
        sum7=su[6]+su[14]+su[22]+su[30]+su[38]+su[46]
        sum8=su[7]+su[15]+su[23]+su[31]+su[39]+su[47]

        prediction22=pd.DataFrame({' ':['Kit','King','Wilson','Yin','Fiona','EC','總數'],'5萬以下':[su[0],su[8],su[16],su[24],su[32],su[40],sum1],'5萬-10萬':[su[1],su[9],su[17],su[25],su[33],su[41],sum2],'10萬-20萬':[su[2],su[10],su[18],su[26],su[34],su[42],sum3],'20萬-30萬':[su[3],su[11],su[19],su[27],su[35],su[43],sum4],'30萬-40萬':[su[4],su[12],su[20],su[28],su[36],su[44],sum5],'40萬-50萬':[su[5],su[13],su[21],su[29],su[37],su[45],sum6],'50萬-100萬':[su[6],su[14],su[22],su[30],su[38],su[46],sum7],'100萬以上':[su[7],su[15],su[23],su[31],su[39],su[47],sum8],'總單量':[sum(su[0:8]),sum(su[8:16]),sum(su[16:24]),sum(su[24:32]),sum(su[32:40]),sum(su[40:48]),sum(su[0:48])]})
        prediction22=prediction22.set_index([' '])

        #more detail in source with money

        source1=['Facebook','Yahoo','Youtube','Google','新聞','論壇','朋友介紹','Instagram','其他','--請選擇--','郵件','地鐵/小巴廣告']
        sourcecomb=[]
        for ii in range(len(source1)):
            for bb in range(len(moneyy)):
                sourcecomb.append(tt.loc[tt.如何找到我們.str.contains(source1[ii],case=False,na=False)].預算.str.count(moneyy[bb]).sum())

        sumsourcecomb1=sourcecomb[0]+sourcecomb[8]+sourcecomb[16]+sourcecomb[24]+sourcecomb[32]+sourcecomb[40]+sourcecomb[48]+sourcecomb[56]+sourcecomb[64]+sourcecomb[72]+sourcecomb[80]+sourcecomb[88]
        sumsourcecomb2=sourcecomb[1]+sourcecomb[9]+sourcecomb[17]+sourcecomb[25]+sourcecomb[33]+sourcecomb[41]+sourcecomb[49]+sourcecomb[57]+sourcecomb[65]+sourcecomb[73]+sourcecomb[81]+sourcecomb[89]
        sumsourcecomb3=sourcecomb[2]+sourcecomb[10]+sourcecomb[18]+sourcecomb[26]+sourcecomb[34]+sourcecomb[42]+sourcecomb[50]+sourcecomb[58]+sourcecomb[66]+sourcecomb[74]+sourcecomb[82]+sourcecomb[90]
        sumsourcecomb4=sourcecomb[3]+sourcecomb[11]+sourcecomb[19]+sourcecomb[27]+sourcecomb[35]+sourcecomb[43]+sourcecomb[51]+sourcecomb[59]+sourcecomb[67]+sourcecomb[75]+sourcecomb[83]+sourcecomb[91]
        sumsourcecomb5=sourcecomb[4]+sourcecomb[12]+sourcecomb[20]+sourcecomb[28]+sourcecomb[36]+sourcecomb[44]+sourcecomb[52]+sourcecomb[60]+sourcecomb[68]+sourcecomb[76]+sourcecomb[84]+sourcecomb[92]
        sumsourcecomb6=sourcecomb[5]+sourcecomb[13]+sourcecomb[21]+sourcecomb[29]+sourcecomb[37]+sourcecomb[45]+sourcecomb[53]+sourcecomb[61]+sourcecomb[69]+sourcecomb[77]+sourcecomb[85]+sourcecomb[93]
        sumsourcecomb7=sourcecomb[6]+sourcecomb[14]+sourcecomb[22]+sourcecomb[30]+sourcecomb[38]+sourcecomb[46]+sourcecomb[54]+sourcecomb[62]+sourcecomb[70]+sourcecomb[78]+sourcecomb[86]+sourcecomb[94]
        sumsourcecomb8=sourcecomb[7]+sourcecomb[15]+sourcecomb[23]+sourcecomb[31]+sourcecomb[39]+sourcecomb[47]+sourcecomb[55]+sourcecomb[63]+sourcecomb[71]+sourcecomb[79]+sourcecomb[87]+sourcecomb[95]
        

        predictionresource1=pd.DataFrame({' ':['Facebook','Yahoo','Youtube','Google','新聞','論壇','朋友介紹','Instagram','其他','沒選','郵件','地鐵/小巴廣告','總數'],'5萬以下':[sourcecomb[0],sourcecomb[8],sourcecomb[16],sourcecomb[24],sourcecomb[32],sourcecomb[40],sourcecomb[48],sourcecomb[56],sourcecomb[64],sourcecomb[72],sourcecomb[80],sourcecomb[88],sumsourcecomb1],'5萬-10萬':[sourcecomb[1],sourcecomb[9],sourcecomb[17],sourcecomb[25],sourcecomb[33],sourcecomb[41],sourcecomb[49],sourcecomb[57],sourcecomb[65],sourcecomb[73],sourcecomb[81],sourcecomb[89],sumsourcecomb2],'10萬-20萬':[sourcecomb[2],sourcecomb[10],sourcecomb[18],sourcecomb[26],sourcecomb[34],sourcecomb[42],sourcecomb[50],sourcecomb[58],sourcecomb[66],sourcecomb[74],sourcecomb[82],sourcecomb[90],sumsourcecomb3],'20萬-30萬':[sourcecomb[3],sourcecomb[11],sourcecomb[19],sourcecomb[27],sourcecomb[35],sourcecomb[43],sourcecomb[51],sourcecomb[59],sourcecomb[67],sourcecomb[75],sourcecomb[83],sourcecomb[91],sumsourcecomb4],'30萬-40萬':[sourcecomb[4],sourcecomb[12],sourcecomb[20],sourcecomb[28],sourcecomb[36],sourcecomb[44],sourcecomb[52],sourcecomb[60],sourcecomb[68],sourcecomb[76],sourcecomb[84],sourcecomb[92],sumsourcecomb5],'40萬-50萬':[sourcecomb[5],sourcecomb[13],sourcecomb[21],sourcecomb[29],sourcecomb[37],sourcecomb[45],sourcecomb[53],sourcecomb[61],sourcecomb[69],sourcecomb[77],sourcecomb[85],sourcecomb[93],sumsourcecomb6],'50萬-100萬':[sourcecomb[6],sourcecomb[14],sourcecomb[22],sourcecomb[30],sourcecomb[38],sourcecomb[46],sourcecomb[54],sourcecomb[62],sourcecomb[70],sourcecomb[78],sourcecomb[86],sourcecomb[94],sumsourcecomb7],'100萬以上':[sourcecomb[7],sourcecomb[15],sourcecomb[23],sourcecomb[31],sourcecomb[39],sourcecomb[47],sourcecomb[55],sourcecomb[63],sourcecomb[71],sourcecomb[79],sourcecomb[87],sourcecomb[95],sumsourcecomb8],'總單量':[sum(sourcecomb[0:8]),sum(sourcecomb[8:16]),sum(sourcecomb[16:24]),sum(sourcecomb[24:32]),sum(sourcecomb[32:40]),sum(sourcecomb[40:48]),sum(sourcecomb[48:56]),sum(sourcecomb[56:64]),sum(sourcecomb[64:72]),sum(sourcecomb[72:80]),sum(sourcecomb[80:88]),sum(sourcecomb[88:96]),sum(sourcecomb[0:96])]})
        predictionresource1=predictionresource1.set_index([' '])


        #district
        kongto=['堅尼地城',
            '石塘咀',
            '西營盤',
            '上環',
            '中環',
            '金鐘',
            '半山區',
            '山頂',
            '灣仔',
            '銅鑼灣',
            '跑馬地',
            '大坑',
            '掃桿埔',
            '渣甸山',
            '天后',
            '寶馬山',
            '北角',
            '鰂魚涌',
            '西灣河',
            '筲箕灣',
            '柴灣',
            '小西灣',
            '薄扶林',
            '香港仔',
            '鴨脷洲',
            '黃竹坑',
            '壽臣山',
            '淺水灣',
            '舂磡角',
            '赤柱',
            '大潭',
            '石澳']
        kowloon=['尖沙咀',
            '油麻地',
            '西九龍',
            '填海區',
            '京士柏',
            '旺角',
            '大角咀',
            '美孚',
            '荔枝角',
            '長沙灣',
            '深水埗',
            '石硤尾',
            '又一村',
            '大窩坪',
            '昂船洲',
            '紅磡',
            '土瓜灣',
            '馬頭角',
            '馬頭圍',
            '啟德',
            '九龍城',
            '何文田',
            '九龍塘',
            '筆架山',
            '新蒲崗',
            '黃大仙',
            '東頭',
            '橫頭磡',
            '樂富',
            '鑽石山',
            '慈雲山',
            '牛池灣',
            '坪石',
            '九龍灣',
            '牛頭角',
            '佐敦',
            '觀塘',
            '秀茂坪藍田',
            '油塘',
            '鯉魚門']
        newt=['葵涌',
            '青衣',
            '荃灣',
            '荃威花園',
            '梨木樹',
            '汀九',
            '深井',
            '青龍頭',
            '馬灣',
            '欣澳',
            '大欖涌',
            '掃管笏',
            '屯門',
            '藍地',
            '洪水橋',
            '廈村',
            '流浮山',
            '天水圍',
            '元朗',
            '新田',
            '落馬洲',
            '錦田',
            '石崗',
            '八鄉',
            '粉嶺',
            '聯和墟',
            '上水',
            '石湖墟',
            '沙頭角',
            '鹿頸',
            '烏蛟騰',
            '大埔墟',
            '大埔',
            '大埔滘',
            '大尾篤',
            '船灣',
            '樟木頭',
            '企嶺下',
            '大圍',
            '沙田',
            '火炭',
            '馬料水',
            '烏溪沙',
            '馬鞍山',
            '清水灣',
            '西貢',
            '大網仔',
            '將軍澳',
            '坑口',
            '調景嶺',
            '馬游塘',
            '長洲',
            '坪洲',
            '大嶼山',
            '東涌',
            '南丫島']

        kongtocnt=0
        kowlooncnt=0
        newtcnt=0

        df.地址=df.地址.astype(str)
        for g in range(tt.shape[0]):
            for i in range(len(kongto)):
                    if kongto[i]  in df.地址.iloc[g]:
                        kongtocnt+=1
                        break
                    else:
                        continue
            for i in range(len(kowloon)):
                    if kowloon[i]  in df.地址.iloc[g]:
                        kowlooncnt+=1
                        break
                    else:
                        continue
            for i in range(len(newt)):
                    if newt[i]  in df.地址.iloc[g]:
                        newtcnt+=1
                        break
                    else:
                        continue

        prediction33=pd.DataFrame({' ':['地區'],'港島':[kongtocnt],'九龍':[kowlooncnt],'新界':[newtcnt],'總數':[kongtocnt+kowlooncnt+newtcnt]})
        prediction33=prediction33.set_index([' '])

        


        #type 
        try:
            homet=tt.裝修類型.str.count('住宅').sum()
        except:
            homet=0
        try:
            towert=tt.裝修類型.str.count('工廈/辦公室').sum()
        except:
            towert=0
        try:
            shopt=tt.裝修類型.str.count('商鋪').sum()
        except:
            shopt=0
        #typeagaincomdeco
        try:
            shoo=df1.裝修類型.str.count('商舖').sum()
        except:
            shoo=0
        try:
            food=df1.裝修類型.str.count('食肆').sum()
        except:
            food=0
        try:
            office=df1.裝修類型.str.count('辦公室').sum()
        except:
            office=0

        
        predictiontype=pd.DataFrame({' ':['裝修類型'],'Ec住宅':[homet],'Ec商鋪':[shopt],'Ec工廈/辦公室':[towert],'Com商舖':[shoo],'Com食肆':[food],'Com辦公室':[office],'總數':[homet+shopt+towert+shoo+food+office]})
        predictiontype=predictiontype.set_index([' '])



        #df1 = pd.DataFrame({'A':['A0','A1','A2'],'B':['B0','B1','B2'],'C':['C0','C1','C2'],},index=pd.date_range('2017-01-01',periods=4, freq='M'))
        #df2 = pd.DataFrame({'A':['A3','A4','A5'],'B':['B3','B4','B5'],'C':['C3','C4','C5']},index=pd.date_range('2017-01-01',periods=4, freq='M'))

        #predictiontype=pd.concat([df1,df2],axis=1,keys=['df1','df2']).swaplevel(0,1,axis=1).sort_index(axis=1)

        


        #type2
        try:
            both=tt.配對公司類別.str.count('2者皆可').sum()
        except:
            both=0
        try:
            cons=tt.配對公司類別.str.count('裝修公司').sum()
        except:
            cons=0
        try:
            des=tt.配對公司類別.str.count('室內設計').sum()
        except:
            des=0
        predictiontype1=pd.DataFrame({' ':['配對公司類別'],'裝修公司':[cons],'室內設計':[des],'2者皆可':[both],'總數':[both+cons+des]})
        predictiontype1=predictiontype1.set_index([' '])


        #origin
        prediction2=pd.DataFrame({' ':['來源'],'Google':[gog],'Facebook':[facebook],'Yahoo':[yahoo],'Instagram':[instagram],'朋友介紹':[friend],'Youtube':[youtube],'論壇':[forum],'新聞':[news],'其他':[other]})
        prediction2=prediction2.set_index([' '])


        #api getting echouse vip form
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

        SAMPLE_SPREADSHEET_ID = '1U21R5n8dbn6MbzYQj3QjMXFcd4w2hoFYaUtU7S1PnS8'
        SAMPLE_RANGE_NAME = 'ecvip!A:O'
        lis=[]
        lis1=[]
        di={}
        def main():
            """Shows basic usage of the Sheets API.
            Prints values from a sample spreadsheet.
            """
            cnt=1
            
            
            creds = None
            # The file token.pickle stores the user's access and refresh tokens, and is
            # created automatically when the authorization flow completes for the first
            # time.
            if os.path.exists('./token.pickle'):
                with open('./token.pickle', 'rb') as token:
                    creds = pickle.load(token)
            # If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        './credentials.json', SCOPES)
                    creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open('./token.pickle', 'wb') as token:
                    pickle.dump(creds, token)

            service = build('sheets', 'v4', credentials=creds)

            # Call the Sheets API
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                        range=SAMPLE_RANGE_NAME).execute()
            values = result.get('values', [])

            if not values:
                print('No data found.')
            else:
                for row in values:
                    if cnt==1:
                        lis.extend(row)
                        cnt+=1
                    else:
                        lis1.append(row)
            
            for i in range(len(lis1)):

                di.update({str(i):lis1[i]})

        main()

        vipcomp=pd.DataFrame.from_dict(di, orient='index',columns=lis)
        vipcomp['Entry_DateSubmitted']=pd.to_datetime(vipcomp['Entry_DateSubmitted'])
        vipcomp=vipcomp.loc[vipcomp['Entry_DateSubmitted'].dt.date>=datetime.date(yea, mon, 1)]
        dat=31
        for i in range(7):
            try:
                vipcomp=vipcomp.loc[vipcomp['Entry_DateSubmitted'].dt.date<=datetime.date(yea, mon, dat)]
                break
            except:
                dat-=1


        vipcomp=vipcomp.rename(columns={"EcHouse裝修加盟_Id": "EC單號"})

        vipcompkit=vipcomp.loc[vipcomp.負責人.str.contains('KIT',case=False,na=False)]
        vipcompkit = vipcompkit.drop(vipcompkit.columns[[1,2,3,5,6,7,8,9,10,11,12,14]], axis=1)
        vipcompkit['EC單號'] = 'EC' + vipcompkit['EC單號'].astype(str)
        

        vipcompwil=vipcomp.loc[vipcomp.負責人.str.contains('WIL',case=False,na=False)]
        vipcompwil = vipcompwil.drop(vipcompwil.columns[[1,2,3,5,6,7,8,9,10,11,12,14]], axis=1)
        vipcompwil['EC單號'] = 'EC' + vipcompwil['EC單號'].astype(str)

        vipcompyin=vipcomp.loc[vipcomp.負責人.str.contains('YIN',case=False,na=False)]
        vipcompyin=vipcompyin.drop(vipcompyin.columns[[1,2,3,5,6,7,8,9,10,11,12,14]], axis=1)
        vipcompyin['EC單號'] = 'EC' + vipcompyin['EC單號'].astype(str)

        vipcompking=vipcomp.loc[vipcomp.負責人.str.contains('KING',case=False,na=False)]
        vipcompking = vipcompking.drop(vipcompking.columns[[1,2,3,5,6,7,8,9,10,11,12,14]], axis=1)
        vipcompking['EC單號'] = 'EC' + vipcompking['EC單號'].astype(str)

        #comdeco vip google sheet api

        SAMPLE_RANGE_NAME = 'comvip!A:N'
        comviplis=[]
        comviplis1=[]
        comvipdi={}
        def comvipmain():
            """Shows basic usage of the Sheets API.
            Prints values from a sample spreadsheet.
            """
            cnt=1
            
            
            creds = None
            # The file token.pickle stores the user's access and refresh tokens, and is
            # created automatically when the authorization flow completes for the first
            # time.
            if os.path.exists('./token.pickle'):
                with open('./token.pickle', 'rb') as token:
                    creds = pickle.load(token)
            # If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        './credentials.json', SCOPES)
                    creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open('./token.pickle', 'wb') as token:
                    pickle.dump(creds, token)

            service = build('sheets', 'v4', credentials=creds)

            # Call the Sheets API
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                        range=SAMPLE_RANGE_NAME).execute()
            values = result.get('values', [])

            if not values:
                print('No data found.')
            else:
                for row in values:
                    if cnt==1:
                        comviplis.extend(row)
                        cnt+=1
                    else:
                        comviplis1.append(row)
            
            for i in range(len(comviplis1)):

                comvipdi.update({str(i):comviplis1[i]})

        comvipmain()

        comvipcomp=pd.DataFrame.from_dict(comvipdi, orient='index',columns=comviplis)
        comvipcomp['Entry_DateSubmitted']=pd.to_datetime(comvipcomp['Entry_DateSubmitted'])
        comvipcomp=comvipcomp.loc[comvipcomp['Entry_DateSubmitted'].dt.date>=datetime.date(yea, mon, 1)]
        dat=31
        for i in range(7):
            try:
                comvipcomp=comvipcomp.loc[comvipcomp['Entry_DateSubmitted'].dt.date<=datetime.date(yea, mon, dat)]
                break
            except:
                dat-=1


        comvipcomp=comvipcomp.rename(columns={"Comdeco加盟_Id": "COM單號"})

        comvipcompkit=comvipcomp.loc[comvipcomp.負責人.str.contains('KIT',case=False,na=False)]
        comvipcompkit = comvipcompkit.drop(comvipcompkit.columns[[1,2,3,5,6,7,8,9,10,11,13]], axis=1)
        comvipcompkit['COM單號'] = 'COM' + comvipcompkit['COM單號'].astype(str)
        comvipcompkit=comvipcompkit.reset_index().drop(columns='index')
        vipcompkit=vipcompkit.reset_index().drop(columns='index')
        comvipcompkit=pd.concat([vipcompkit,comvipcompkit], axis=1)





        comvipcompwil=comvipcomp.loc[comvipcomp.負責人.str.contains('WIL',case=False,na=False)]
        comvipcompwil = comvipcompwil.drop(comvipcompwil.columns[[1,2,3,5,6,7,8,9,10,11,13]], axis=1)
        comvipcompwil['COM單號'] = 'COM' + comvipcompwil['COM單號'].astype(str)
        comvipcompwil=comvipcompwil.reset_index().drop(columns='index')
        vipcompwil=vipcompwil.reset_index().drop(columns='index')
        comvipcompwil=pd.concat([vipcompwil,comvipcompwil], axis=1)




        comvipcompking=comvipcomp.loc[comvipcomp.負責人.str.contains('KING',case=False,na=False)]
        comvipcompking = comvipcompking.drop(comvipcompking.columns[[1,2,3,5,6,7,8,9,10,11,13]], axis=1)
        comvipcompking['COM單號'] = 'COM' + comvipcompking['COM單號'].astype(str)
        comvipcompking=comvipcompking.reset_index().drop(columns='index')
        vipcompking=vipcompking.reset_index().drop(columns='index')
        comvipcompking=pd.concat([vipcompking,comvipcompking], axis=1)



        comvipcompyin=comvipcomp.loc[comvipcomp.負責人.str.contains('YIN',case=False,na=False)]
        comvipcompyin = comvipcompyin.drop(comvipcompyin.columns[[1,2,3,5,6,7,8,9,10,11,13]], axis=1)
        comvipcompyin['COM單號'] = 'COM' + comvipcompyin['COM單號'].astype(str)
        comvipcompyin=comvipcompyin.reset_index().drop(columns='index')
        vipcompyin=vipcompyin.reset_index().drop(columns='index')
        comvipcompyin=pd.concat([vipcompyin,comvipcompyin], axis=1)

        # aaa=pd.DataFrame({'123':['KIT',2],'23':['ASD',42]})
        # def highlight_max(s):
        #     '''
        #     highlight the maximum in a Series yellow.
        #     '''
        #     is_max = s == 'KIT'
        #     return ['background-color: yellow' if v else '' for v in is_max]
        # comvipcompyin1=aaa.style.apply(highlight_max).render()
    
   


        
        newmonth=int(to_predict_list['za'])+1
        

        plt.close()
        tt['Entry_DateSubmitted']=pd.to_datetime(tt['Entry_DateSubmitted']).dt.date
        tt['Entry_DateSubmitted']=pd.to_datetime(tt['Entry_DateSubmitted'])
        q=tt.set_index('Entry_DateSubmitted').groupby(pd.Grouper(freq='D')).size()
        g=pd.Series(q.tolist(),q.index)
        g=g.groupby([g.index.day]).sum()
        ax=g.plot(figsize=(15,10),title=str(yea)+'-'+str(mon)+' EcHouse Daily Form Submission',ylim=(0,20),color='purple')
        ax.set_xticks(range(1,len(g)+1))
        ax.set_xticklabels(["%02d" % item for item in g.index.tolist()], rotation=360)
        ax.get_figure().savefig("./static/image/c"+str(q2)+".png", transparent=True)


        plt.close()

        #table of sumbission
        da=[]
        quan=[]
        qq=pd.Series(q.tolist(),q.index)
        for i in qq.index:
            da.append(i.date())
        for i in qq.tolist():
            quan.append(i)
        sumb=pd.DataFrame([(quan)],columns=da,index=['提交'])

        SAMPLE_RANGE_NAME1 = 'ordernumreal!A:J'
        orderlis=[]
        orderlis1=[]
        orderdi={}
        def ordermain():
       
                    cnt=1
                    
                    
                    creds = None
           
                    if os.path.exists('./token.pickle'):
                        with open('./token.pickle', 'rb') as token:
                            creds = pickle.load(token)
                    if not creds or not creds.valid:
                        if creds and creds.expired and creds.refresh_token:
                            creds.refresh(Request())
                        else:
                            flow = InstalledAppFlow.from_client_secrets_file(
                                './credentials.json', SCOPES)
                            creds = flow.run_local_server(port=0)
                        with open('./token.pickle', 'wb') as token:
                            pickle.dump(creds, token)

                    service = build('sheets', 'v4', credentials=creds)

                    sheet = service.spreadsheets()
                    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                                range=SAMPLE_RANGE_NAME1).execute()
                    values = result.get('values', [])

                    if not values:
                        print('No data found.')
                    else:
                        for row in values:
                            if cnt==1:
                                orderlis.extend(row)
                                cnt+=1
                            else:
                                orderlis1.append(row)
                    
                    for i in range(len(orderlis1)):

                        orderdi.update({str(i):orderlis1[i]})

        ordermain()

        ordernum=pd.DataFrame.from_dict(orderdi, orient='index',columns=orderlis)

        ordernum['月份']=pd.to_datetime(ordernum['月份'])
        import datetime

        dat=31
        ordernum=ordernum.loc[ordernum['月份'].dt.date>=datetime.date(yea, mon, 1)]
        for i in range(7):
            try:
                ordernum=ordernum.loc[ordernum['月份'].dt.date<=datetime.date(yea, mon, dat)]
                break
            except:
                dat-=1
                
        ordernum=ordernum.fillna(0)    

        ordernum['已收樓已派VIP']=pd.to_numeric(ordernum['已收樓已派VIP'])
        ordernum['已收樓可派單數']=pd.to_numeric(ordernum['已收樓可派單數'])
        ordernum['已收樓上門']=pd.to_numeric(ordernum['已收樓上門'])
        ordernum['未收樓']=pd.to_numeric(ordernum['未收樓'])
        ordernum['未收樓已派VIP']=pd.to_numeric(ordernum['未收樓已派VIP'])

        ordernum['已收樓派單率']=(ordernum['已收樓已派VIP']/ordernum['已收樓可派單數'])*100
        ordernum['已收樓上門率']=(ordernum['已收樓上門']/ordernum['已收樓可派單數'])*100

        ordernum['未收樓派單率']=(ordernum['未收樓已派VIP']/ordernum['未收樓'])*100

        ordernum=ordernum.round(2)
        ordernum=ordernum.fillna(0)
        ordernum['已收樓派單率']=ordernum['已收樓派單率'].astype(str) + '%'
        ordernum['已收樓上門率']=ordernum['已收樓上門率'].astype(str) + '%'
        ordernum['未收樓派單率']=ordernum['未收樓派單率'].astype(str) + '%'
        ordernum=ordernum.reset_index()
        try:
            vipgetting=ordernum['月份VIP接單總數'][0]
        except:
            vipgetting='No Record'
        seventypercent=pd.DataFrame({' ':[totalorder0],'查詢量':[totalorder],'VIP接單量':[vipgetting],'合格':[round(int(totalorder)*3*0.7)]})
        #prediction.index.name='Cog Form'
        seventypercent=seventypercent.set_index([' '])

        ordernum=ordernum.reindex(columns=['負責人','派單數','已收樓可派單數','已收樓已派VIP','已收樓上門','已收樓派單率','已收樓上門率','未收樓','未收樓已派VIP','未收樓派單率','中單'])

        googleall=[]
        facebookall=[]
        yahooall=[]
        instagramall=[]
        youtubeall=[]
        friendall=[]
        fiveall=[]
        fivetotwnetyall=[]
        twetytofiftyall=[]
        fiftytohundredall=[]
        hundredall=[]
        kitall=[]
        kingall=[]
        yinall=[]
        wilall=[]
        fionaall=[]
        ecall=[]
        for e in range(1,13):
            mon=e  #forinput
            dat=31
            storeall=df.loc[df['Entry_DateSubmitted'].dt.date>=datetime.date(yea, mon, 1)]
            for i in range(7):
                try:
                    storeall=storeall.loc[storeall['Entry_DateSubmitted'].dt.date<=datetime.date(yea, mon, dat)]
                    break
                except:
                    dat-=1

            googleall.append(storeall.如何找到我們.str.count('Google').sum())
            facebookall.append(storeall.如何找到我們.str.count('Facebook').sum())
            yahooall.append(storeall.如何找到我們.str.count('Yahoo').sum())
            instagramall.append(storeall.如何找到我們.str.count('Instagram').sum())
            youtubeall.append(storeall.如何找到我們.str.count('Youtube').sum())
            friendall.append(storeall.如何找到我們.str.count('朋友介紹').sum())

            fiveall.append(storeall.預算.str.count('以下').sum())
            money1=storeall.預算.str.count(' 10萬').sum()+storeall.預算.str.count('10萬 ').sum()
            money2=storeall.預算.str.count('20萬 ').sum()+storeall.預算.str.count('30萬 ').sum()+storeall.預算.str.count('40萬 ').sum()

            
            fivetotwnetyall.append(money1)
            twetytofiftyall.append(money2)
            fiftytohundredall.append(storeall.預算.str.count('50萬 ').sum())
            hundredall.append(storeall.預算.str.count('以上').sum())


            try:        
                kitall.append(storeall.負責人.str.contains('kit',case=False).sum()-storeall.負責人.str.contains('kit cancel',case=False).sum())
            except:
                kitall.append(0)
            try:        
                kingall.append(storeall.負責人.str.contains('king',case=False).sum()-storeall.負責人.str.contains('kit cancel',case=False).sum())
            except:
                kingall.append(0)
            try:        
                yinall.append(storeall.負責人.str.contains('yin',case=False).sum()-storeall.負責人.str.contains('kit cancel',case=False).sum())
            except:
                yinall.append(0)
            try:        
                wilall.append(storeall.負責人.str.contains('wil',case=False).sum()-storeall.負責人.str.contains('kit cancel',case=False).sum())
            except:
                wilall.append(0)
            try:        
                fionaall.append(storeall.負責人.str.contains('fiona',case=False).sum()-storeall.負責人.str.contains('kit cancel',case=False).sum())
            except:
                fionaall.append(0)

    

        sourcedistribution=pd.DataFrame({'Google':googleall,'Facebook':facebookall,'Yahoo':yahooall,'Instagram':instagramall,'Youtube':youtubeall,'Friend':friendall})
        sourcedistribution.index+=1
        axxx=sourcedistribution.plot(title=str(yea)+' Year EcHouse Source Distribution',ylim=(0,100))
        axxx.set_xticks(range(1,13))
        axxx.get_figure().savefig("./static/image/q"+str(q2)+".png", transparent=True)

        plt.close()


        orderdistribution=pd.DataFrame({'5':fiveall,'5-20':fivetotwnetyall,'20-50':twetytofiftyall,'50-100':fiftytohundredall,'100':hundredall})
        orderdistribution.index+=1
        axx1=orderdistribution.plot(title=str(yea)+' Year EcHouse Order Distribution')
        axx1.set_xticks(range(1,13))
        axx1.get_figure().savefig("./static/image/qg"+str(q2)+".png", transparent=True)



        plt.close()
        colleaguedistribution=pd.DataFrame({'Kit':kitall,'King':kingall,'Yin':yinall,'Wil':wilall,'Fiona':fionaall})
        colleaguedistribution.index+=1
        axx2=colleaguedistribution.plot(title=str(yea)+' Year EcHouse Colleague Order Distribution')
        axx2.set_xticks(range(1,13))
        axx2.get_figure().savefig("./static/image/qu"+str(q2)+".png", transparent=True)


        plt.close()

        monthname=to_predict_list['z']+'年'+to_predict_list['za']+'月'
        yearname=to_predict_list['z']+'年'

        return render_template("result30.html",yearname=yearname,monthname=monthname,ordernum=[ordernum.to_html(classes='data')],seventypercent1=[seventypercent.to_html(classes='data')], tablessumb=[sumb.to_html(classes='data')],tables=[prediction.to_html(classes='data')],comvipcompkit=[comvipcompkit.to_html(classes='kit')],comvipcompwil=[comvipcompwil.to_html(classes='data')],comvipcompyin=[comvipcompyin.to_html(classes='data')],comvipcompking=[comvipcompking.to_html(classes='data')],tablesreward=[predictionreward.to_html(classes='data')],tables1=[prediction1.to_html(classes='data')],tables22=[prediction22.to_html(classes='third')],tablesorucecomb=[predictionresource1.to_html(classes='forth')],tables33=[prediction33.to_html(classes='data')],tablestype=[predictiontype.to_html(classes='data')],tablestype1=[predictiontype1.to_html(classes='data')],tables2=[prediction2.to_html(classes='data')],url1='/static/image/a'+str(q2)+'.png',url2='/static/image/b'+str(q2)+'.png',url3='/static/image/c'+str(q2)+'.png',url4='/static/image/d'+str(q2)+'.png',url5='/static/image/e'+str(q2)+'.png',url6='/static/image/q'+str(q2)+'.png',url7='/static/image/qg'+str(q2)+'.png',url8='/static/image/qu'+str(q2)+'.png')

@app.route('/',methods = ['POST'])
def home1():
    if request.method == 'POST':
        return render_template("home.html")
    
@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(200)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig
@app.route('/resultz',methods = ['POST'])
def qqq():
    prediction=''
    if request.method == 'POST':
        print('1')
        return render_template("resultz.html")


if __name__ == "__main__":
    app.debug = True
    app.secret_key = os.urandom(12)
    app.run()
