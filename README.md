# carta-tripid

## Purpose
This script replaces trip_ids with 6-digit numeric ids starting from the second numerical value of exported trip_id.  

## Usage
Tested with Python 3.9.<br>
```python carta-tripid.py feed.zip```<br>
Adjusted files are exported to the current directory for human review, after which they can be manually added to the feed's .zip file.<br>
Alters trip_ids in trips.txt, runcut.txt, stop_times.txt, and frequencies.txt.<br>
If a trip_id is seen multiple times, the script will stop execution to avoid duplicates. When used with feeds exported from Trillium's GTFS Manager, this could be a sign that the feed contains multiple service periods of the same calendar. 
