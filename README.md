## YouTube Analytics Data Retrieval

This Python script is designed to retrieve YouTube Analytics data for a list of videos. It uses the YouTube Analytics API v2 to retrieve data such as views, likes, dislikes, shares, estimated minutes watched, and subscribers gained for a specific date range.
This Code will save the creds of the channel in the creds.json file, so that we don't have to authenticate the channel permission again and again.

### Prerequisites

To use this script, you will need:
- A Google account
- Access to the YouTube Analytics API v2
- A `client_secrets.json` file containing your API credentials
- Python 3.x installed
- Libraries: google-auth, google-auth-oauthlib, google-auth-httplib2, google-api-python-client, pandas, tabulate

To obtain access to the YouTube Analytics API v2 and obtain your API credentials, follow these steps:

1. Go to the [Google Developers Console](https://console.developers.google.com/)
2. Create a new project or select an existing project
3. Enable the YouTube Analytics API v2 for your project
4. Create API credentials for a desktop application
5. Download the `client_secrets.json` file containing your API credentials

For more information on obtaining API credentials, see the [YouTube Analytics API documentation](https://developers.google.com/youtube/reporting/v1/reports).
- More liks to check-out:-
1. [Obtain authorization credentials](https://developers.google.com/youtube/reporting/guides/registering_an_application)
2. [Analytics and Reporting](https://developers.google.com/youtube/analytics)
3. [Code Samples](https://developers.google.com/youtube/reporting/v1/reports#python).

### How to Use

1. Clone or download this repository to your local machine
2. Install the required packages by running `pip install -r requirements.txt` in your terminal
3. Edit the `secrets.json` file to contain your own API credentials
4. Create a text file named `links.txt` in the same directory as the script, with one YouTube video link per line
5. Run the script by running `python youtube_analytics.py` in your terminal

The script will retrieve YouTube Analytics data for each video in the `links.txt` file and save the results to a CSV file named `all_results.csv`. The script will also print the results to the console in a tabulated format.

**Note: This script retrieves private YouTube Analytics data. Use it at your own risk and make sure to follow all relevant terms of service and privacy policies.**

### Further Customization

You can customize the script by changing the date range, metrics, and dimensions used in the API request. See the [YouTube Analytics API documentation](https://developers.google.com/youtube/analytics/getting_started/metrics) for more information on available metrics and dimensions.

### Example Output

Here's an example of what the output might look like:

```
+-----------+------------+-------+-------+----------+--------+----------------------+-------------------+
|  video_id |    Date    | views | likes | dislikes | shares | estimatedMinutesWatched | subscribersGained |
+-----------+------------+-------+-------+----------+--------+----------------------+-------------------+
| xxxxxxxxx | 2023-04-30 |  1234 |   12  |    2     |   1    |          123          |         0         |
| xxxxxxxxx | 2023-05-01 |  2345 |   20  |    3     |   0    |          234          |         1         |
+-----------+------------+-------+-------+----------+--------+----------------------+-------------------+
```
