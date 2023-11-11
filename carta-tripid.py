import sys
import os
import csv
import io
import zipfile

COLOR_RED   = "\033[1;31m"
COLOR_GREEN = "\033[0;32m"
COLOR_RESET = "\033[0;0m"

def convert_file():
    if len(sys.argv) < 2:
        print(COLOR_RED + "No file provided!" + COLOR_RESET)
        exit()
    filepath = sys.argv[1]
    file_type = os.path.splitext(filepath)[1]
    gtfs_zipped = zipfile.ZipFile(filepath)
    if not ".zip" in file_type:
        print(COLOR_RED + "Invalid input. Ensure input is a zip file." + COLOR_RESET)
        exit()
    check_duplicates(gtfs_zipped)
    files_with_tripid = ["trips.txt", "stop_times.txt", "frequencies.txt"]
    files_with_other_field = ["runcut.txt"]
    for file in files_with_tripid: 
        make_new_file(file, gtfs_zipped)
    for file in files_with_other_field:
        make_new_file(file, gtfs_zipped) 


def check_duplicates(gtfs_zipped):
    with gtfs_zipped.open("trips.txt", "r") as file_raw:
        txt = io.TextIOWrapper(file_raw)
        csv_file = csv.DictReader(txt)
        csv_list = list(csv_file)
        seen_trip_ids = set()
        for row in csv_list:
            trip_id = row["trip_id"][3:9]
            row["trip_id"] = trip_id
            if trip_id in seen_trip_ids:
                print(COLOR_RED + "trip_id " + row["trip_id"] + " has already been seen! Will not create duplicates. Ensure the feed does not include multiple service periods of the same calendar." + COLOR_RESET)
                exit()
            seen_trip_ids.add(trip_id)
            

def make_new_file(file, gtfs_zipped):
    with gtfs_zipped.open(file, "r") as file_raw:
        txt = io.TextIOWrapper(file_raw)
        csv_file = csv.DictReader(txt)
        csv_list = list(csv_file)
        file_name = file
        if os.path.exists(file_name):
            print(COLOR_RED + "File with name " + file_name + " already exists in directory; cannot create a new one. Move this file and try again." + COLOR_RESET)
            return
        new_file = open(file_name, "w")
        new_csv_writer = csv.DictWriter(new_file, fieldnames=csv_file.fieldnames)
        new_csv_writer.writeheader()
        for row in csv_list:
            if "trip_id" in csv_file.fieldnames:
                trip_id = row["trip_id"][3:9]
                row["trip_id"] = trip_id
                new_csv_writer.writerow(row)      
            if "start_trip_id" in csv_file.fieldnames:
                    start_trip_id = row["start_trip_id"][3:9]
                    end_trip_id = row["end_trip_id"][3:9]
                    row["start_trip_id"] = start_trip_id
                    row["end_trip_id"] = end_trip_id
                    new_csv_writer.writerow(row)
        new_file.close()
        print(COLOR_GREEN + "Exported " + file_name + " with updated trip_id values." + COLOR_RESET)

if __name__ == "__main__":
    convert_file()
