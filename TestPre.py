import pandas as pd
import numpy as np
import datetime
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans

class initPreObj(object):
    def __init__(self, path):
        self._path = path
        self._data = pd.read_csv(path,parse_dates=['partition_dt'])

    def get_path(self):
        return self._path

    def __del__(self):
        pass

    def get_result_df(self): 

        print("> 필요 없는 컬럼 제거중...")

        del self._data['prod_nm']
        del self._data['parent_prod_id']
        del self._data['parent_prod_nm']
        del self._data['nonsett_target_cpn_amt']
        del self._data['prod_grd_cd']
        del self._data['pkg_nm']
        del self._data['payment_mtd_nm']

        print("> null값 제거중...")
        self._data = self._data.dropna()
        print('> Check null status :'+str(self._data.isnull().sum()))

        print("> 구매 취소 건 제거중...")
        self._data = self._data[self._data.prchs_cancel_yn != 'Y']

        print("> new_id 생성중 (user id + device id)...")
        self._data['new_id'] = self._data['insd_usermbr_no'].astype('str')+self._data['insd_device_id'].astype('str')


        del self._data['insd_usermbr_no'] 
        del self._data['insd_device_id']

        print("> 가입날짜 가공중...")
        # 가입날짜 가공
        self._data['mbr_entry_yymm'] = self._data['mbr_entry_yymm']*100+1
        self._data['mbr_entry_yymm'] = round(self._data['mbr_entry_yymm'])
        self._data['mbr_entry_yymm'].astype('int')
        self._data['mbr_entry_yymm'].astype('str')
        self._data['mbr_entry_yymm'] = pd.to_datetime(self._data['mbr_entry_yymm'], format='%Y%m%d')
<<<<<<< HEAD

        print("> Day of week (요일) 변수 생성중...")

        # Day of week (요일) 변수 생성
        self._data['dayofweek'] = self._data['partition_dt'].dt.weekday.astype('int8')

        print("> New category 생성중...")
        # New category 생성
        self._data['new_cat'] = self._data.loc[:, 'dtl_category_no'].apply(lambda x: x[0:4])

        # Label Encoding
        print("> label encoding 처리중...")

        # encode class values as integers

        encoder1 = LabelEncoder()

        self._data.loc[:, 'payment_mtd_cd'] = encoder1.fit_transform(self._data.loc[:, 'payment_mtd_cd'])
        label_payment_mtd_cd = pd.Series(list(encoder1.classes_))
        # name = str(label_payment_mtd_cd.name)
        # label_payment_mtd_cd.to_csv('%s.csv'%(name),index_label=False)
        print(label_payment_mtd_cd)

        encoder2 = LabelEncoder()
        self._data.loc[:, 'prchs_tm_clsf_nm'] = encoder2.fit_transform(self._data.loc[:, 'prchs_tm_clsf_nm'])
        label_prchs_tm_clsf_nm = pd.Series(list(encoder2.classes_))
        print(label_prchs_tm_clsf_nm)

        encoder3 = LabelEncoder()
        self._data.loc[:, 'chrg_apply_clsf_nm'] = encoder3.fit_transform(self._data.loc[:, 'chrg_apply_clsf_nm'])
        label_chrg_apply_clsf_nm = pd.Series(list(encoder3.classes_))
        print(label_chrg_apply_clsf_nm)

        encoder4 = LabelEncoder()
        self._data.loc[:, 'mno_nm'] = encoder4.fit_transform(self._data.loc[:, 'mno_nm'])
        label_mno_nm = pd.Series(list(encoder4.classes_))
        print(label_mno_nm )

        encoder5 = LabelEncoder()
        self._data.loc[:, 'dtl_category_no'] = encoder5.fit_transform(self._data.loc[:, 'dtl_category_no'])
        label_dtl_category_no = pd.Series(list(encoder5.classes_))
        print(label_dtl_category_no)

        encoder6 = LabelEncoder()
        self._data.loc[:, 'new_cat'] = encoder6.fit_transform(self._data.loc[:, 'new_cat'])
        label_new_cat = pd.Series(list(encoder6.classes_))
        print(label_new_cat)

        encoder7 = LabelEncoder()
        self._data.loc[:, 'sex_clsf_cd'] = encoder7.fit_transform(self._data.loc[:, 'sex_clsf_cd'])
        label_sex_clsf_cd = pd.Series(list(encoder7.classes_))
        print(label_sex_clsf_cd)

        print(" # 유저의 나이 - age_cd")

        # 널값에 대해서는 평균나이 40으로 일괄 적용
        self._data.loc[self._data['age_cd'] == 'ZZZ','age_cd'] = '40'
        self._data.age_cd = self._data.age_cd.astype(int)

        #나이 분류
        self._data.loc[self._data['age_cd']<=9,'age_cd']=1
        self._data.loc[(self._data['age_cd'] <=19) & (self._data['age_cd']>9) ,'age_cd'] =10
        self._data.loc[(self._data['age_cd'] <=29) & (self._data['age_cd']>19) ,'age_cd']=20
        self._data.loc[(self._data['age_cd'] <=39) & (self._data['age_cd']>29) ,'age_cd']=30
        self._data.loc[(self._data['age_cd'] <=49) & (self._data['age_cd']>39) ,'age_cd']=40
        self._data.loc[(self._data['age_cd'] <=59) & (self._data['age_cd']>49) ,'age_cd']=50
        self._data.loc[(self._data['age_cd'] <=69) & (self._data['age_cd']>59) ,'age_cd']=60
        self._data.loc[(self._data['age_cd'] <=79) & (self._data['age_cd']>69) ,'age_cd']=70
        self._data.loc[(self._data['age_cd'] <=89) & (self._data['age_cd']>79) ,'age_cd']=80
        self._data.loc[(self._data['age_cd'] <=99) & (self._data['age_cd']>89) ,'age_cd']=90
        self._data.loc[self._data['age_cd']>99,'age_cd']=100

        # Label Encoding
        encoder8 = LabelEncoder()
        self._data.loc[:, 'age_cd'] = encoder8.fit_transform(self._data.loc[:, 'age_cd'])
        label_age_cd = pd.Series(list(encoder8.classes_))
        print(label_age_cd)

        print("# prod_id - Word2Vec")

        self.wv = pd.read_csv('/notebooks/data/onechu/Preprocessing/Suhyeon/w2v_prod_cl.csv')
        self.wv.reset_index(inplace=True)
        self.wv.rename(columns={'index':'prod_id'},inplace=True)
        self.wv.columns = ['prod_id', 'w2v_prod_clr']
        self._data = pd.merge(self._data,self.wv,how='left')

=======
        
>>>>>>> 78d1c13... 가입 일자 datetime 형으로 변환
        return self._data

    def save_result_df(self, path):
        print("> 전체 csv 파일 생성중...")
        self._data.to_csv(path,index_label = False)


class FeatureObj(object):
    def __init__(self, path, split_day, mode):
        if mode == 0:
            # mode가 0인 경우 DataFrame을 바로 가져오는 경우
            self._data = path
            self._data['partition_dt'] = pd.to_datetime(self._data['partition_dt'])
            self._data['mbr_entry_yymm'] = pd.to_datetime(self._data['mbr_entry_yymm'])
            self._split_date = self._data['partition_dt'].max() - pd.Timedelta(days=split_day)
            self._post_data = self._data.loc[self._data['partition_dt'] > self._split_date]
            self._data = self._data.loc[self._data['partition_dt'] <= self._split_date]
            self.user_df = pd.DataFrame({'new_id' : self._data['new_id'].unique()})
        else:
            # mode가 1인 경우 경로를 읽어오는 경우
            self._data = pd.read_csv(path)
            self._data['partition_dt'] = pd.to_datetime(self._data['partition_dt'])
            self._data['mbr_entry_yymm'] = pd.to_datetime(self._data['mbr_entry_yymm'])
            self._split_date = self._data['partition_dt'].max() - pd.Timedelta(days=split_day)
            self._post_data = self._data.loc[self._data['partition_dt'] > self._split_date]
            self._data = self._data.loc[self._data['partition_dt'] <= self._split_date]
            self.user_df = pd.DataFrame({'new_id' : self._data['new_id'].unique()})
            print(self.user_df.shape)

    def __del__(self):
        pass

    def save_result_df(self, path):
        print("> 전체 csv 파일 생성중...")
        self.user_df.to_csv(path,index_label = False)
        print(self.user_df.shape)

    def get_result_df(self): 

        print("# 데이터가 가진 최신 날짜")
        # 데이터가 가진 최신 날짜
        self.our_last_date = self._data['partition_dt'].max()
        print(self.user_df.shape)

        print("# 유저별 마지막으로 구매일 - 'last_prchs_date'")

        self.last_date = pd.pivot_table(self._data,index=["new_id"],values=["partition_dt"],aggfunc=max)
        self.last_date.rename(columns={'partition_dt':'last_prchs_date'}, inplace=True)
        self.last_date.reset_index(level=0, inplace=True)
        print(self.user_df.shape)

        print("# Recency (데이터가 가진 최신 날짜 - 유저별 마지막 구매일)")

        self.last_date['Recency'] =  (self.our_last_date - self.last_date['last_prchs_date']).dt.days
        self.user_df = pd.merge(self.user_df, self.last_date, how='left')
        print(self.user_df.shape)
        del self.last_date

        print(" # 가입경과일 ")

        self.temp_df = self._data.loc[:,['mbr_entry_yymm','new_id']].drop_duplicates()
        self.temp_df['days_from_register'] = (self.our_last_date - self.temp_df['mbr_entry_yymm']).dt.days
        self.temp_df = self.temp_df.loc[:,['new_id', 'days_from_register']]
        self.user_df = pd.merge(self.user_df, self.temp_df, how='left')
        print(self.user_df.shape)
        del self.our_last_date

        print("# 유저별 처음으로 구매일 - 'init_prchs_date'")

        self.init_date = pd.pivot_table(self._data,index=["new_id"],values=["partition_dt"],aggfunc=min)
        self.init_date.rename(columns={'partition_dt':'init_prchs_date'}, inplace=True)
        self.init_date.reset_index(level=0, inplace=True)
        self.user_df = pd.merge(self.user_df, self.init_date, how='left')
        print(self.user_df.shape)
        del self.init_date

        print("# 유저별 Frequency (유저의 총 구매횟수)")

        self.temp_df = self._data[['new_id', 'prchs_id']].drop_duplicates()
        self.Frequency = self.temp_df.groupby(self.temp_df['new_id'], as_index=False).count()
        self.Frequency.columns = ['new_id', 'Frequency']
        self.user_df = pd.merge(self.user_df, self.Frequency, how='left')
        print(self.user_df.shape)
        del self.Frequency

        print(" # 일 기준 총 구매 횟수 - day_freq")

        self.temp_df = self._data.loc[:,['new_id', 'partition_dt']].drop_duplicates()
        self.day_freq = self.temp_df.groupby(self.temp_df['new_id'], as_index=False).count()
        self.day_freq.columns = ['new_id', 'day_freq']
        self.user_df = pd.merge(self.user_df, self.day_freq, how='left')
        print(self.user_df.shape)
        del self.day_freq

        print("#유저별 구매한 상품 종류 수")

        self.temp_df = self._data.groupby(["new_id"])["prod_id"].nunique()
        self.clsf_prod_n = pd.DataFrame({'new_id':self.temp_df.index, 'clsf_prod_n':self.temp_df.values})
        self.user_df = pd.merge(self.user_df, self.clsf_prod_n, how='left')
        print(self.user_df.shape)
        del self.clsf_prod_n


        print("#유저별 구매한 카테고리 종류 수")

        self.temp_df = self._data.groupby(["new_id"])["dtl_category_no"].nunique()
        self.clsf_dtl_cat_n = pd.DataFrame({'new_id':self.temp_df.index, 'clsf_dtl_cat_n':self.temp_df.values})
        self.user_df = pd.merge(self.user_df, self.clsf_dtl_cat_n, how='left')
        print(self.user_df.shape)
        del self.clsf_dtl_cat_n

        print("# 유저별 구매한 new_cat 종류 수 ")
        #유저별 구매한 new_cat 종류 수 
        self.temp_df = self._data.groupby(["new_id"])["new_cat"].nunique()
        self.clsf_new_cat_n = pd.DataFrame({'new_id':self.temp_df.index, 'clsf_new_cat_n':self.temp_df.values})
        self.user_df = pd.merge(self.user_df, self.clsf_new_cat_n, how='left')
        print(self.user_df.shape)
        del self.clsf_new_cat_n

        print("# cpn freq cpn_pref")
        ## 1-2. 이전 단계와 마찬가지로 유저별로 쿠폰을 사용하여 구매한 총 횟수를 구한다.
        self.coupon_filtered_unique_df = self._data.loc[self._data['payment_mtd_cd']==4, ['new_id', 'prchs_id']].drop_duplicates()
        ### 유저별로 Group by 하여 Coupon Frequency('cpn_freq')를 구한다.
        self.coupon_grouped_df = self.coupon_filtered_unique_df.groupby(self.coupon_filtered_unique_df['new_id'], as_index=False).count()
        ### user_df와 Merge하기위해 컬럼명을 미리 변경해준다.
        self.coupon_grouped_df.columns = ['new_id', 'cpn_freq']
        ### user_df 을 기준으로 Merge를 진행한다.
        self.user_df = pd.merge(self.user_df, self.coupon_grouped_df, how='left')
        del self.coupon_filtered_unique_df
        del self.coupon_grouped_df
        self.user_df = self.user_df.fillna(0)
        self.user_df['cpn_pref'] = self.user_df['cpn_freq'] / self.user_df['Frequency'] * 100
        print(self.user_df.shape)

        print(" # free_freq ")

        self.free_freq_df = self._data.loc[self._data['chrg_apply_clsf_nm'] == 0, ['new_id','prchs_id']].drop_duplicates()
        self.free_df = self.free_freq_df.groupby(self.free_freq_df['new_id'], as_index=False).count()
        self.free_df.columns = ['new_id','free_freq']
        self.user_df = pd.merge(self.user_df, self.free_df, how='left')
        print(self.user_df.shape)
        del self.free_freq_df
        del self.free_df

        print(" # free_pref ")

        self.user_df = self.user_df.fillna(0)
        self.user_df['free_pref'] = self.user_df['free_freq'] / self.user_df['Frequency'] * 100
        del self.user_df['cpn_freq']
        print(self.user_df.shape)

        print("# 유저별 북스캐쉬 - 'bcash_purchs_cnt'")

        self.temp_df = self._data.loc[(self._data['payment_mtd_cd'] == 12) | (self._data['payment_mtd_cd'] == 11), ['new_id', 'prchs_id']].drop_duplicates()
        self.temp_df = self.temp_df.groupby(self.temp_df['new_id'], as_index=False).count()
        self.temp_df.columns = ['new_id', 'bcash_purchs_cnt']
        self.user_df = pd.merge(self.user_df, self.temp_df, how='left')
        print(self.user_df.shape)

        print("# 유저별 총 쿠폰 결제금액 - 기초통계량 변수")

        self.temp_df = self._data.loc[:,['sett_target_cpn_amt','new_id']]
        # SUM
        self.temp_df_agg = pd.pivot_table(self.temp_df,index=["new_id"],aggfunc=np.sum)
        self.temp_df_agg.rename(columns={'sett_target_cpn_amt':'sett_target_cpn_amt_sum'},inplace=True)
        # MEAN, MAX, MIN, STD, VAR  
        self.temp_df_agg['sett_target_cpn_amt_mean']=pd.pivot_table(self.temp_df,index=["new_id"],aggfunc=np.mean)
        self.temp_df_agg['sett_target_cpn_amt_max']=pd.pivot_table(self.temp_df,index=["new_id"],aggfunc=np.max)
        self.temp_df_agg['sett_target_cpn_amt_min']=pd.pivot_table(self.temp_df,index=["new_id"],aggfunc=np.min)
        self.temp_df_agg['sett_target_cpn_amt_std']=pd.pivot_table(self.temp_df,index=["new_id"],aggfunc=np.std)
        self.temp_df_agg['sett_target_cpn_amt_var']=pd.pivot_table(self.temp_df,index=["new_id"],aggfunc=np.var)
        self.temp_df_agg.reset_index(level=0, inplace=True)
        self.user_df = pd.merge(self.user_df, self.temp_df_agg, how='left')
        print(self.user_df.shape)

        print(" # 유저별 구매 시각 - 기초통계량 변수")

        self.temp_df = self._data.loc[:,['prchs_tm_clsf_nm','new_id']]
        # SUM
        self.temp_df_agg = pd.pivot_table(self.temp_df,index=["new_id"],aggfunc=np.sum)
        self.temp_df_agg.rename(columns={'prchs_tm_clsf_nm':'prchs_tm_clsf_nm_sum'},inplace=True)
        # MEAN, MAX, MIN, STD, VAR  
        self.temp_df_agg['prchs_tm_clsf_nm_mean']=pd.pivot_table(self.temp_df,index=["new_id"],aggfunc=np.mean)
        self.temp_df_agg['prchs_tm_clsf_nm_max']=pd.pivot_table(self.temp_df,index=["new_id"],aggfunc=np.max)
        self.temp_df_agg['prchs_tm_clsf_nm_min']=pd.pivot_table(self.temp_df,index=["new_id"],aggfunc=np.min)
        self.temp_df_agg['prchs_tm_clsf_nm_std']=pd.pivot_table(self.temp_df,index=["new_id"],aggfunc=np.std)
        self.temp_df_agg['prchs_tm_clsf_nm_var']=pd.pivot_table(self.temp_df,index=["new_id"],aggfunc=np.var)
        self.temp_df_agg['prchs_tm_clsf_nm_nuniq']=pd.pivot_table(self.temp_df,index=["new_id"],aggfunc=pd.Series.nunique)
        self.temp_df_agg.reset_index(level=0, inplace=True)
        self.user_df = pd.merge(self.user_df, self.temp_df_agg, how='left')
        print(self.user_df.shape)

        print("# 유저별 총 상품 결제금액 - 기초통계량 변수")

        self.temp_df = self._data.loc[:,['prod_amt','new_id']]
        # SUM
        self.temp_df_agg = pd.pivot_table(self.temp_df,index=["new_id"],aggfunc=np.sum)
        self.temp_df_agg.rename(columns={'prod_amt':'prod_amt_sum'},inplace=True)
        # MEAN, MAX, MIN, STD, VAR  
        self.temp_df_agg['prod_amt_mean']=pd.pivot_table(self.temp_df,index=["new_id"],aggfunc=np.mean)
        self.temp_df_agg['prod_amt_max']=pd.pivot_table(self.temp_df,index=["new_id"],aggfunc=np.max)
        self.temp_df_agg['prod_amt_min']=pd.pivot_table(self.temp_df,index=["new_id"],aggfunc=np.min)
        self.temp_df_agg['prod_amt_std']=pd.pivot_table(self.temp_df,index=["new_id"],aggfunc=np.std)
        self.temp_df_agg['prod_amt_var']=pd.pivot_table(self.temp_df,index=["new_id"],aggfunc=np.var)
        self.temp_df_agg.reset_index(level=0, inplace=True)
        self.user_df = pd.merge(self.user_df, self.temp_df_agg, how='left')
        print(self.user_df.shape)

        print(" # 유저별 총 실결제 금액 - 기초통계량 변수")

        self.temp_df = self._data.loc[:,['cust_payment_amt','new_id']]
        # SUM
        self.temp_df_agg = pd.pivot_table(self.temp_df,index=["new_id"],aggfunc=np.sum)
        self.temp_df_agg.rename(columns={'cust_payment_amt':'Monetary'},inplace=True)
        # MEAN, MAX, MIN, STD, VAR  
        self.temp_df_agg['avg_prchs_amt']=pd.pivot_table(self.temp_df,index=["new_id"],aggfunc=np.mean)
        self.temp_df_agg['cust_payment_amt_max']=pd.pivot_table(self.temp_df,index=["new_id"],aggfunc=np.max)
        self.temp_df_agg['cust_payment_amt_min']=pd.pivot_table(self.temp_df,index=["new_id"],aggfunc=np.min)
        self.temp_df_agg['cust_payment_amt_std']=pd.pivot_table(self.temp_df,index=["new_id"],aggfunc=np.std)
        self.temp_df_agg['cust_payment_amt_var']=pd.pivot_table(self.temp_df,index=["new_id"],aggfunc=np.var)
        self.temp_df_agg.reset_index(level=0, inplace=True)
        self.user_df = pd.merge(self.user_df, self.temp_df_agg, how='left')
        print(self.user_df.shape)

        print(" # 유저의 성별 - sex_clsf_cd")
        # 중도에 성별이 바뀌는 경우 유저가 중복되어 들어가므로 가장 최근 구매건에 명시되어 있는 성별값으로 설정
        self.temp_df = self._data.loc[:,['sex_clsf_cd','new_id']].drop_duplicates().groupby(['new_id']).tail(1)
        self.user_df = pd.merge(self.user_df, self.temp_df, how='left')
        print(self.user_df.shape)

        print(" # 유저의 나이")
        self.temp_df = self._data.loc[:,['age_cd','new_id']].drop_duplicates().groupby(['new_id']).tail(1)
        self.temp_df.rename(columns={'age_cd':'age_cat'}, inplace=True)
        self.user_df = pd.merge(self.user_df, self.temp_df, how='left')
        print(self.user_df.shape)

        print(" # 유저 통신사")
        self.temp_df = self._data.loc[:,['mno_nm','new_id']].drop_duplicates().groupby(['new_id']).tail(1)
        self.user_df = pd.merge(self.user_df, self.temp_df, how='left')
        print(self.user_df.shape)

        print(" # 평균 구매 주기 - avg_prchs_cycle (사용기간/freq)")

        self.user_df['avg_prchs_cycle'] = ((self.user_df['last_prchs_date'] - self.user_df['init_prchs_date']) / self.user_df['Frequency']).dt.days
        print(self.user_df.shape)

        print(" # day freq 기준 평균 구매 주기 - avg_prchs_day_cycle (사용기간/freq)")

        self.user_df['avg_prchs_day_cycle'] = ((self.user_df['last_prchs_date'] - self.user_df['init_prchs_date']) / self.user_df['day_freq']).dt.days
        print(self.user_df.shape)

        print("# pass / pass_yn / pass_nuique / pass_amt (유저별 정액권 피쳐)")

        # init 데이터에 'pass' 컬럼 값 추가
        self._data['pass'] =0
        self._data['pass'].loc[self._data['new_cat']==3] =1

        # new_id별로 pass count 값 추가
        self.p = self._data.groupby(['new_id'])['pass'].sum()
        self.p = pd.DataFrame(self.p)

        # pass count로 pass_yn 변수까지 생성
        self.p['pass_yn'] = 1
        self.p.loc[self.p['pass']==0,['pass_yn']]=0

        # pass 관련 새로운 변수를 groupby - 그전에 new_id를 컬럼으로 쓰기 위해 reset_index()함.
        self.p.reset_index()

        # pass_nunique, pass_amt는 DPFF 카테고리 구매건만 잘라서 DF를 만든 후, outer 조인으로 기존 p 와 병합.
        self.DPFF = self._data.loc[self._data['new_cat']==3]
        # dtl category가 dpff인 것들 구매 종류 수
        self.nunique = self.DPFF.groupby('new_id')['dtl_category_no'].nunique()

        # dtl category가 dpff인 것들의 구매금액
        self.amt = self.DPFF.groupby('new_id')["cust_payment_amt"].sum()

        # DataFrame으로 변환 후, 최종 merge (new_id별 새로운 feature matrix)
        self.nunique = pd.DataFrame(self.nunique)
        self.amt =pd.DataFrame(self.amt)
        self.total = pd.merge(self.p,self.nunique,how='outer',on='new_id')
        self.total = pd.merge(self.total,self.amt,how='outer',on='new_id')
        # outer 조인이므로, 없는 값은 0 으로 채우기
        self.total = self.total.fillna(0)
        self.total.rename(columns={'dtl_category_no':'pass_nuique','cust_payment_amt':'pass_amt'},inplace=True)
        self.total.reset_index(level=0, inplace=True)

        self.user_df = pd.merge(self.user_df, self.total, how='left')
        print(self.user_df.shape)

        print("diff_prchs_date")

        self.user_df['diff_prchs_date'] = (self.user_df['last_prchs_date'] - self.user_df['init_prchs_date']).dt.days
        print(self.user_df.shape)

        print("past churn")

        self.user_df['past_churn'] = 0
        self.user_df.loc[self.user_df.Recency > 7, 'past_churn'] = 1
        print(self.user_df.shape)

        print("max_prchs_cycle / min ~ / median")

        #import the csv
        self.tx_data = self._data.loc[:,['partition_dt','new_id']]

        # 구매는 일단위로 본다
        self.tx_data = self.tx_data.drop_duplicates()
        # date 포맷 변경
        self.tx_data['partition_dt'] = pd.to_datetime(self.tx_data['partition_dt'])
        # new_id, partition_dt 를 기준으로 오름차순 정렬
        self.tx_data = self.tx_data.sort_values(['new_id','partition_dt'], ascending=[True, True])

        # Day Gap 계산
        self.tx_data['PrevInvoiceDate'] = self.tx_data.groupby('new_id')['partition_dt'].shift(1)
        self.tx_data['DayDiff'] = (self.tx_data['partition_dt'] - self.tx_data['PrevInvoiceDate']).dt.days
        self.diff_df = self.tx_data[['new_id', 'DayDiff']]
        del self.tx_data

        # 유저별로 Max_day_gap / Min~ / Median ~ 뽑아내고 nan 행에 대해서는 median값으로 채워주기
        self.diff_max_df =  self.diff_df.groupby(['new_id']).max()
        self.diff_max_df.reset_index(level=0, inplace=True)
        self.diff_max_df = self.diff_max_df.fillna(self.diff_max_df['DayDiff'].median())
        self.diff_max_df.rename(columns={'DayDiff':'max_prchs_cycle'}, inplace=True)

        self.diff_min_df =  self.diff_df.groupby(['new_id']).min()
        self.diff_min_df.reset_index(level=0, inplace=True)
        self.diff_min_df = self.diff_min_df.fillna(self.diff_min_df['DayDiff'].median())
        self.diff_min_df.rename(columns={'DayDiff':'min_prchs_cycle'}, inplace=True)

        self.diff_median_df =  self.diff_df.groupby(['new_id']).median()
        self.diff_median_df.reset_index(level=0, inplace=True)
        self.diff_median_df = self.diff_median_df.fillna(self.diff_median_df['DayDiff'].median())
        self.diff_median_df.rename(columns={'DayDiff':'median_prchs_cycle'}, inplace=True)

        del self.diff_df

        # 마지막으로 user_df에 붙히기
        self.user_df = pd.merge(self.user_df, self.diff_max_df, how='left')
        self.user_df = pd.merge(self.user_df, self.diff_min_df, how='left')
        self.user_df = pd.merge(self.user_df, self.diff_median_df, how='left')

        del self.diff_max_df
        del self.diff_min_df
        del self.diff_median_df
        print(self.user_df.shape)

        print("마지막으로 churn 붙히기")

        self._post_data = self._post_data.loc[:,['new_id']].drop_duplicates()
        self._post_data['churn'] = 0
        self.user_df = pd.merge(self.user_df, self._post_data, how='left')
        self.user_df = self.user_df.fillna(1)
        print(self.user_df.shape)

        return self.user_df