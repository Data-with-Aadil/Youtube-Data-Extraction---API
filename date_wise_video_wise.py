# we only want the data from links from smartsheet aadil/
import os
from venv import create
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

from tabulate import tabulate
import pandas as pd
from datetime import datetime

SCOPES = ['https://www.googleapis.com/auth/yt-analytics.readonly']

API_SERVICE_NAME = 'youtubeAnalytics'
API_VERSION = 'v2'
CLIENT_SECRETS_FILE = 'secrets.json'

# service ko lene ke liye:-
def get_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server()
    return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

# client create krenge
def execute_api_request(client_library_function, **kwargs):
    response = client_library_function(
        **kwargs
    ).execute()
    return response

# table crations
def create_table(table, headers=None):
    if headers:
        headerstring = "\t{}\t" * len(headers)
        print(headerstring.format(*headers))

    rowstring = "\t{}\t" * len(table[0])

    for row in table:
        print(rowstring.format(*row))

if __name__ == '__main__':
    youtubeAnalytics = get_service()

    # Read video links from a text file, with one link per line
    with open('links.txt', 'r') as f:
        video_links = [line.strip() for line in f]

    # Initialize empty DataFrame to store results
    results_df = pd.DataFrame(columns=['video_id', 'Date', 'views', 'likes', 'dislikes', 'shares', 'estimatedMinutesWatched', 'subscribersGained'])

    # Loop through each video link and execute the API request separately
    for video_link in video_links:
        video_id = video_link.split('=')[1]  # Extract the video ID from the link
        result = execute_api_request(
            youtubeAnalytics.reports().query,
            ids='channel==MINE',
            startDate='2020-02-14',
            endDate=datetime.now().strftime('%Y-%m-%d'),  # Use current date as end date
            dimensions='video,day',
            metrics='views,likes,dislikes,shares,estimatedMinutesWatched,subscribersGained',
            filters=f'video=={video_id}',
            sort='day'
        )

        # Append result to DataFrame
        df = pd.DataFrame(result['rows'], columns=['video_id', 'Date', 'views', 'likes', 'dislikes', 'shares', 'estimatedMinutesWatched', 'subscribersGained'])
        results_df = pd.concat([results_df, df], ignore_index=True)

        # Print tabulated result for this video
        head = ['video_id','Date','views','likes','dislikes','shares','estimatedMinutesWatched','subscribersGained'] 
        print(tabulate(result['rows'], headers=head, tablefmt="pretty"))

    # Write results to CSV file
    results_df.to_csv('all_results.csv', index=False)
