# Import required libraries
import os
from venv import create
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from tabulate import tabulate
import pandas as pd
from datetime import datetime

# Set scopes, API service name, version, and client secrets file name
SCOPES = ['https://www.googleapis.com/auth/yt-analytics.readonly']
API_SERVICE_NAME = 'youtubeAnalytics'
API_VERSION = 'v2'
CLIENT_SECRETS_FILE = 'secrets.json'

# Create a function to get the service object by authenticating with the user's credentials
def get_service():
    # Check if credentials file already exists and load them
    creds = None
    creds_file = 'creds.json'
    if os.path.exists(creds_file):
        creds = Credentials.from_authorized_user_file(creds_file, SCOPES)
    # If credentials do not exist or are invalid, run authentication flow and save credentials
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
        creds = flow.run_local_server()
        with open(creds_file, 'w') as f:
            f.write(creds.to_json())
    # Return authenticated service object
    return build(API_SERVICE_NAME, API_VERSION, credentials=creds)

# Create a function to execute any API request using the provided client library function and kwargs
def execute_api_request(client_library_function, **kwargs):
    # Execute the API request and return the response
    response = client_library_function(**kwargs).execute()
    return response

# Create a function to print a tabulated version of a given table
def create_table(table, headers=None):
    # If headers are provided, print them as a tabulated row
    if headers:
        headerstring = "\t{}\t" * len(headers)
        print(headerstring.format(*headers))
    # Print each row of the table as a tabulated row
    rowstring = "\t{}\t" * len(table[0])
    for row in table:
        print(rowstring.format(*row))

if __name__ == '__main__':
    # Authenticate and get the service object
    youtubeAnalytics = get_service()

    # Read video links from a text file, with one link per line
    with open('links.txt', 'r') as f:
        video_links = [line.strip() for line in f]

    # Initialize empty DataFrame to store results
    results_df = pd.DataFrame(columns=['video_id', 'Date', 'views', 'likes', 'dislikes', 'shares', 'estimatedMinutesWatched', 'subscribersGained'])

    # Loop through each video link and execute the API request separately
    for video_link in video_links:
        # Extract the video ID from the link
        video_id = video_link.split('=')[1]
        # Execute the API request for the current video
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
        # Create a new DataFrame with the data returned by the API request, with column names specified
        df = pd.DataFrame(result['rows'], columns=['video_id', 'Date', 'views', 'likes', 'dislikes', 'shares', 'estimatedMinutesWatched', 'subscribersGained'])
        # Concatenate the newly created DataFrame with the existing results DataFrame
        results_df = pd.concat([results_df, df], ignore_index=True)

        # Print tabulated result for this video
        # Create a list of headers for the tabulated data
        head = ['video_id','Date','views','likes','dislikes','shares','estimatedMinutesWatched','subscribersGained'] 
        # Print the tabulated data using the 'tabulate' module
        print(tabulate(result['rows'], headers=head, tablefmt="pretty"))

    # Write results to CSV file
    # Write the results DataFrame to a CSV file with column names, and exclude the index column
    results_df.to_csv('all_results.csv', index=False)

