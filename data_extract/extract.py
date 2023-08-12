from steam.webapi import webapi_request
import pandas as pd
import math
import datetime as dt

# Setup Save Data Path
title = 'battlebit-remastered'
save_path = f'data/{title}-reviews.csv'

# Dataframe To Store Retrieved Reviews
results = pd.DataFrame(columns=['id', 'review', 'create_ts'])

# Reviews From Process Date - day_range to Process Date
day_range = 30
cursor = '*'

# Initial Request To Get Total Reviews
# TODO Obtain Game Title ID From Game Title Using http://api.steampowered.com/ISteamApps/GetAppList/v0002/
req = webapi_request(url='https://store.steampowered.com/appreviews/671860?json=1',
                     params={'language': 'english', 'day_range': day_range, 'cursor': cursor})

# API Gets Batches of 20 Reviews, Calculate Num Query Requests
total_reviews = req['query_summary']['total_reviews']
num_queries = math.ceil(total_reviews / 20)

# Count How Many Reviews Processed
count = 0

print(f'There Are {total_reviews} Total Reviews')
print(f'API Will Be Called {num_queries} Times')

# Call API Until All Reviews Retrieved
for i in range(num_queries):
    print(f'API Call: {i+1}')
    req = webapi_request(url='https://store.steampowered.com/appreviews/671860?json=1',
                         params={'language': 'english', 'day_range': day_range, 'cursor': cursor})

    reviews = req['reviews']
    cursor = req['cursor']

    # Store Batch Of Reviews, Rename Columns
    curr_reviews = pd.DataFrame.from_dict(reviews)[['recommendationid', 'review', 'timestamp_created']] \
        .rename({'recommendationid': 'id', 'timestamp_created': 'create_ts'}, axis=1)

    # Convert TS to UTC TS
    curr_reviews['create_ts'] = curr_reviews['create_ts'].map(dt.datetime.utcfromtimestamp)

    # Append Batch Of Reviews
    results = pd.concat([results, curr_reviews])
    count += 20
    print(f'Processed {count} Reviews')

# Save Reviews To CSV
results.to_csv(save_path, index=False)