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
        
        return self._data

    def save_result_df(self, path):
        print("> 전체 csv 파일 생성중...")
        self._data.to_csv(path,index_label = False)