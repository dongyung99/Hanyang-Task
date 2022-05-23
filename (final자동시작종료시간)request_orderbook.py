import time
import requests
import pandas as pd
from datetime import datetime
import os

# current_starting_time = datetime.now().strftime('%Y-%m-%d-bithumb-btc-orderbook.csv')
current_starting_time = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
filename_start_time = f'./{current_starting_time}'

filename = 'a'
old_name = 'a'

while True:
    #response = requests.get ('https://api.bithumb.com/public/orderbook/BTC_KRW/?count=10')
    #print (response.text)

    old_name = filename
    timestamp = datetime.now()
    req_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')
    filename_req_timestamp = timestamp.strftime('%Y-%m-%d %H.%M.%S')
    filename_last_time = f'{filename_req_timestamp}'

    filename = filename_start_time + '~' + filename_last_time +'-bithumb-btc-orderbook.csv'
    
    book = {}
    response = requests.get ('https://api.bithumb.com/public/orderbook/BTC_KRW/?count=5')
    book = response.json()

    data = book['data']

    #print (data)

    bids = (pd.DataFrame(data['bids'])).apply(pd.to_numeric,errors='ignore')
    bids.sort_values('price', ascending=False, inplace=True)
    bids = bids.reset_index()
    del bids['index']
    bids['type'] = 0

    asks = (pd.DataFrame(data['asks'])).apply(pd.to_numeric,errors='ignore')
    asks.sort_values('price', ascending=True, inplace=True)
    asks['type'] = 1

    '''
    tmstamp = int(data['timestamp'])
    tm = datetime.fromtimestamp(tmstamp/1000)
    '''
    

    df = pd.concat([bids, asks])
    df['timestamp']= req_timestamp

    #print (df)
    
    if not os.path.exists(old_name):
        df.to_csv(filename, mode = 'w', index = False)
    else:
        os.rename(old_name, filename)
        df.to_csv(filename, mode = 'a', index = False, header = False)

    time.sleep(1)



#print (response.status_code)
