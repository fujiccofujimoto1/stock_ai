import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader.data as web
import datetime
import pickle
from dateutil.relativedelta import relativedelta
from datetime import datetime, date, timedelta


class Get_data():
    start = datetime(2000, 1, 1)
    end = datetime.now()
    
    # 日経平均の取得
    #### https://ntk-lab.com/import_stock_data/
    def nikkei_download(self):
        # 日経平均
        df_nikkei=web.DataReader('^N225', 'yahoo',self.start,self.end)
        #print ("配列長さ:",len(df_nikkei))
        df_nikkei=df_nikkei[['Open','Close']]
        df_nikkei = df_nikkei.reset_index()
        return df_nikkei

    
    def dow_dayplus(self,row):
        y=row['Date']

        if (row['weekday']>=0 and row['weekday']<=3):
            # アメリカが月〜木曜日であれば、アメリカ時間に+1 して、日本時間にマージする
            #　例　6月16日（月）(USA)  => 6月17日（火）（jst）
            y=row['Date']+ timedelta(days=1)

        elif row['weekday']==4:
            # 金曜日であれば、   +3
            #　例　6月19日（金）(USA)  => 6月22日（月）（jst）

            y=row['Date']+ timedelta(days=3)

        return y

    # ダウ平均の取得
    ### https://jp.investing.com/indices/us-30-historical-data
    
    
    def dow_download(self):
        # ダウ平均
        df_dow = web.DataReader('^DJI', 'yahoo',self.start,self.end)

        df_dow['dow_compare']=df_dow['Close']/df_dow['Open']
        df_dow=df_dow[['dow_compare']]
        df_dow = df_dow.reset_index()

        #print ("配列長さ:",len(df_dow))
        # ⭐️⭐️⭐️⭐️⭐️⭐️ここでダウ平均の時間を＋1日する
        df_dow['weekday']=df_dow['Date'].apply(lambda x: x.weekday())
        df_dow['Date']=df_dow.apply(self.dow_dayplus,axis=1)


        return df_dow

    
    def add_today_open(self,df_nikkei,open_value):

        last_day=pd.to_datetime(df_nikkei.tail(1)['Date'].values[0])
        one_weekday_after = last_day + relativedelta(weekday=0)
        one_weekday_after

        df_nikkei=df_nikkei.append(
            { 'Date':one_weekday_after,
                'Open':open_value, 
                'Close':"0"
            },ignore_index=True)
        return df_nikkei

    
    def main(self,today=""):
        #日経平均
        df_nikkei=self.nikkei_download()
        print("日経平均【完了】")
        
        
        if today!="":
            df_nikkei=self.add_today_open(df_nikkei,today)
            
            
            
        # ダウ平均
        df_dow=self.dow_download()
        print("ダウ平均【完了】")
        
        # 結合
        df=pd.merge(df_nikkei,df_dow,on=['Date'],how='inner')
        df['Close']=df['Close'].astype('float')
        df['Open']=df['Open'].astype('float')
        df=df[['Date','Open','Close','dow_compare']]
        print("結合【完了】")
        
        # ファイルの保存 
        df.to_pickle('data/stock.pkl')
        print("保存【完了】")
        #display(df.tail(3))
        
        return df