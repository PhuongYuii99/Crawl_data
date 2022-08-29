from datetime import date, timedelta
import requests
import pandas as pd 
import csv

# define general keys:
start_date = date.today()- timedelta(7)
end_date = date.today() - timedelta(1)


# create list app 
r_app = requests.get('https://api.sensortower.com:443/v1/ios/ajax/user_apps?auth_token=your_auth_token').json()
list_app = pd.json_normalize(r_app['user_apps'])[['appName','id','os', 'appId','validCountries','publisherId']].values.tolist()


# crawl keyword download by game, os, country, start_date, end_date from list app
# function retrieve keyword download and write csv file
def retrieve_keyword(): 
    rows_1 = []
    hearder_1 = ["start_date","end_date","game_name","os","country","keyword_download","percent_download","number_download"]
    with open('sensor_keyword.csv', mode='w', encoding='UTF-8', newline='') as f1:
        writer = csv.writer(f1)
        writer.writerow(hearder_1)
        for app in range(len(list_app)): # loop to get apps
            for country in range(len(list_app[app][4])): # loop to get countries
                r_kw = requests.get('https://api.sensortower.com/v1/{0}/keywords/downloads/history?user_app_id={1}&country={2}&start_date={3}&end_date={4}&device=phone&date_granularity=weekly&display_untracked_keywords=false&auth_token=your_auth_token'.format(list_app[app][2],list_app[app][1],list_app[app][4][country],start_date,end_date)).json()
                # loại trường hợp data bị rỗng
                if len(r_kw['data']) == 0: 
                    continue
                list_kw = pd.json_normalize(r_kw['data'])[['name','data']].values.tolist()
                for row_1 in list_kw:
                    # solve the case that percent download and number download are empty, if empty then set percent download = 0.0, number download = 0
                    if len(row_1[1]) == 0:
                        row_1[1] = [[0,0.0,0]]
                    rows_1.append(start_date) #start_date
                    rows_1.append(end_date) #end_date
                    rows_1.append(list_app[app][0]) #game_name
                    rows_1.append(list_app[app][2]) #os
                    rows_1.append(list_app[app][4][country]) #country
                    rows_1.append(row_1[0]) #keyword_download
                    rows_1.append(row_1[1][0][1]) #percent_download
                    rows_1.append(row_1[1][0][2]) #number_download
                    writer.writerow(rows_1)
                    rows_1.clear() 


# Retrieve download and revenue estimates of apps by country, date, os from list app
# function retrieve download and revenue and write csv file
def retrieve_number_download_and_revenue():
    rows_2 = []
    hearder_2 = ["event_date","game_name","publisher_id","os","country","number_download","revenue","start_date","end_date"]
    with open('sensor_download_revenue.csv', mode='w', encoding='UTF-8', newline='') as f2:
        writer = csv.writer(f2)
        writer.writerow(hearder_2)
        for app in range(len(list_app)): # loop to get apps
            for country in range(len(list_app[app][4])): # loop to get countries
                r_dr = requests.get('https://api.sensortower.com/v1/{0}/sales_report_estimates?app_ids={1}&publisher_ids={2}&countries={3}&date_granularity=daily&start_date={4}&end_date={5}&auth_token=your_auth_token'.format(list_app[app][2],list_app[app][1],list_app[app][5],list_app[app][4][country],start_date,end_date)).json()
                for row_2 in r_dr:
                    rows_2.append(row_2['d'].replace('T00:00:00Z','')) #event_date
                    rows_2.append(list_app[app][0]) #game_name
                    rows_2.append(list_app[app][5]) #publisher_id
                    rows_2.append(list_app[app][2]) #os
                    rows_2.append(list_app[app][4][country]) #country
                    # solve the case of different key due to different os
                    if list_app[app][2] == 'ios':
                        # number_download
                        # solve the case data do not have key 'iu', 'au'
                        try:
                            iu = row_2['iu']
                        except:
                            iu = 0
                        try:
                            au = row_2['au'] 
                        except:
                            au = 0
                        rows_2.append(iu+au)
                        # revenue
                        # solve the case data do not have key 'ir', 'ar'
                        try: 
                            ir = row_2['ir'] 
                        except: 
                            ir = 0
                        try: 
                            ar = row_2['ar'] 
                        except: 
                            ar = 0
                        rows_2.append(ir+ar)
                    # solve the case of different key due to different os
                    elif list_app[app][2] == 'android':
                        # number_download
                        # solve the case data do not have key 'u'
                        try:
                            rows_2.append(row_2['u'])
                        except: 
                            rows_2.append(0)
                        # revenue
                        # solve the case data do not have key 'r'
                        try:
                            rows_2.append(row_2['r'])
                        except: 
                            rows_2.append(0)
                    else:
                        raise Exception("neither_android_and_ios")
                    rows_2.append(start_date) #start_date
                    rows_2.append(end_date) #end_date
                    writer.writerow(rows_2)
                    rows_2.clear()

retrieve_keyword() 
retrieve_number_download_and_revenue()

# {
#   "sales_report_estimates_key": {
#     "ios": {
#       "aid": "App ID",
#       "cc": "Country Code",
#       "d": "Date",
#       "iu": "iPhone Downloads",
#       "ir": "iPhone Revenue",
#       "au": "iPad Downloads",
#       "ar": "iPad Revenue"
#     },
#     "android": {
#       "aid": "App ID",
#       "c": "Country Code",
#       "d": "Date",
#       "u": "Android Downloads",
#       "r": "Android Revenue"
#     },
#     "unified": {
#       "app_id": "App ID",
#       "country": "Country Code",
#       "date": "Date",
#       "android_units": "Android Downloads",
#       "android_revenue": "Android Revenue",
#       "ipad_units": "iPad Downloads",
#       "ipad_revenue": "iPad Revenue",
#       "iphone_units": "iPhone Downloads",
#       "iphone_revenue": "iPhone Revenue"
#     }
#   }
# }
