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

        return self._data

    def save_result_df(self, path):
        print("> 전체 csv 파일 생성중...")
        self._data.to_csv(path,index_label = False)