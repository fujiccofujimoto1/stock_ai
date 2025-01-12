# 変数の定義
import pandas as pd
import pandas_profiling as pdp
import datetime
import pickle

class Make_data():
    
    pram_predict_day=3                   # 1日後の予測をする
    pd.set_option('display.max_columns', 100)
    
    def load(self):
        df = pd.read_pickle('data/stock.pkl')
        #print ("配列長さ:",len(df))
        return df
    
    
    
    # 前処理モジュールの定義（当日の上昇率、過去からの上昇率、下降率）
    # 偏差値
    def Deviation_value(self,df_tmp,x):
        std=df_tmp.std()['Open']
        mean=df_tmp.mean()['Open']
        deviation=(mean-x)*10/std+50
        return deviation
    # 前処理モジュールの定義（当日の上昇率、過去からの上昇率、下降率）

    def persent(self,day0,xday):         #　当日のopen価格と、過去のと比較して上昇率(当日open/過去open)を返す
        rate=0  #上昇率
        if ((i-xday)>=0 and data_len>(i-xday)):        
            rate= ((df_fx.iloc[i,open_index]/df_fx.iloc[i-xday,open_index])-1)*100
        return rate

    def result(self,day0,xday):          #day0 当日の上昇率(close/open)の結果を返す

        rate=0  #上昇率
        if ((i-xday)>=0 and data_len>(i-xday)): 
            rate= ((df_fx.iloc[i,close_index]/df_fx.iloc[i,open_index])-1)*100
        return rate
    
    
    def main(self,start_date):
        if start_date=="":
            start_date='2000-01-01'             #元データを2000年からにする
        else:
            self.start_date=start_date
        
        df=self.load()

        df      =df[(df['Date']>=start_date )]
        df      = df.reset_index(drop=True)
        df_len  =len(df)


        # Index の取得
        index_date    = df.columns.get_loc('Date')
        index_close   = df.columns.get_loc('Close')
        index_open    = df.columns.get_loc('Open')
        index_dow     = df.columns.get_loc('dow_compare')
        
        
        ## 日毎の９０日前からの下落率を９０日間を計算
        columns=["day+"+str(x+1) for x in range(90)]
        #print(columns)
        for i,x in enumerate(columns):
            # ＋は、前日からの比較
            df[x]=df['Open'].pct_change(periods=(i+1))*100

        ## 偏差値を計算
        # 前処理部分　（現在の値と、過去のからの上昇率、下降率を記したDFを作成
        for i in range(df_len) :
            day0_open=df.iloc[i,index_open]
            if i>90:
                df_tail=df.iloc[i-90:i,:]
                Deviation30=self.Deviation_value(df_tail.tail(30),day0_open)
                Deviation60=self.Deviation_value(df_tail.tail(60),day0_open)
                Deviation90=self.Deviation_value(df_tail.tail(90),day0_open)
            if i%100==0:
                print("進捗: {:.1%}".format(i/df_len),end=" ")
                
        #正解      # -は、未来との比較
        # １日先のオープンの値を予想
        df['result']=df['Open'].pct_change(periods=-1*self.pram_predict_day)*100*(-1)
        # 上昇(買い)はマイナス１、下降（売り）は、0
        #df['result']=df['result'].apply(lambda x: 1 if x<0 else 0)
        
        # １日のOpenから Closeの変化だけを見るのであればこの記述にする
        df['result']=df['Close']-df["Open"]#/.apply(lambda x: 1 if x<0 else 0)
        df['result']=df['result'].apply(lambda x: 1 if x>0 else 0)
        
        df=df.dropna()

        # 前処理データの保存
        if start_date<='2000-01-01': 
            df.to_pickle('data/stock_preprocessing_20201017.pkl',)
            print("【完了】データ保存")
        return df