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
