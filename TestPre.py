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

        return self.user_df