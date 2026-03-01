import pandas as pd
from dotenv import load_dotenv
load_dotenv()
import utils

df=pd.DataFrame([
    {'table':'users','id':1,'error':'missing email'},
    {'table':'orders','id':42,'error':'negative amount'}
])
print(df)
print('report:')
print(utils.analyze_failed_records(df))
