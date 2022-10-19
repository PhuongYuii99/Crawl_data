from airflow import models
import requests
import csv
from datetime import date, timedelta

yesterday = date.today() - timedelta(1)
page_name = ['Thetan Arena','Thetan Rivals']
page_id= [models.Variable.get('facebook_thetanarena_page_id'),models.Variable.get('facebook_thetanrival_page_id')]
access_token = [models.Variable.get('facebook_thetanarena_long_lived_page_access_token'),models.Variable.get('facebook_thetarival_long_lived_page_access_token')]

# Page User Demographics: page_fans,page_fans_country,page_fans_gender_age,page_fan_adds_unique,page_fans_by_like_source,page_fan_removes_unique,page_fans_by_unlike_source_unique
# Page Impressions: page_impressions_unique,page_impressions_paid_unique,page_impressions_organic_unique,page_impressions_by_country_unique,page_impressions_by_age_gender_unique

# get some page insights
def get_page_insight():
    csv_rows = []
    hearder = ['event_date','page_id','page_name','metrics','period','value','title','description']
    with open('fb_page_insight.csv', 'w', encoding='UTF-8', newline='') as f:
        writer = csv.writer(f)
        #writer.writerow(hearder)
        for i in range(len(page_id)):
            page_domain = 'https://graph.facebook.com/{0}/insights'.format(page_id[i])
            url_access_token = '?access_token={0}'.format(access_token[i])
            page_metrics = '&metric=page_fans,page_fan_adds_unique,page_fan_removes_unique,page_impressions_unique,page_impressions_paid_unique,page_impressions_organic_unique'
            page_url = '{0}{1}{2}'.format(page_domain, url_access_token, page_metrics)
            # Handle facebook pagination case
            while True:
                page_r = requests.get(page_url).json()
                if "error" in page_r:
                    print(page_r)
                    break

                rows = page_r["data"]

                for row in rows:
                    # 1 values has 2 value so use for loop to decide which value is suitable
                    for x in range(2):
                        # just get data of yesterday and do not get data of other days
                        if row['values'][x]['end_time'].replace('T07:00:00+0000','') == str(yesterday):
                            csv_rows.append(row['values'][x]['end_time'].replace('T07:00:00+0000','')) #event_date
                            csv_rows.append(page_id[i]) 
                            csv_rows.append(page_name[i])
                            csv_rows.append(row['name']) # metrics
                            csv_rows.append(row['period']) # day, week, days_28
                            csv_rows.append(row['values'][x]['value']) #values
                            csv_rows.append(row['title']) # title
                            csv_rows.append(row['description']) # description
                            writer.writerow(csv_rows)
                            csv_rows.clear() 
                            break
                        else:
                            continue
                # Handle facebook pagination case
                if "paging" not in page_r or "next" not in page_r["paging"]:
                    break
                else:
                    page_url = page_r["paging"]["next"]
    
get_page_insight()
