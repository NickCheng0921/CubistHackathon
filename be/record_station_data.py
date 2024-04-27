import sqlite3
import requests
import schedule
import time
import datetime

# Function to connect to the SQLite database
def connect_db():
    conn = sqlite3.connect('station_data.db')
    return conn

# Function to fetch data from the API and insert into the database
def fetch_and_insert_data():
    # Fetch data from the API
    response = requests.get('https://gbfs.lyft.com/gbfs/2.3/bkn/en/station_status.json')
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()

        #print(data)

        vals = []
        for i in data['data']['stations']:
            dict = i
            #print(i['last_reported'])
            #time = dict['last_reported']
            bikes = dict['num_bikes_available']
            docks_available = dict['num_docks_available']
            station_id = dict['station_id']
            val = [bikes, docks_available, station_id]
            vals.append(val)

        #print(vals)
        bulk_insert_station_data(vals)
        
        # Insert data into the database
        '''
        for entry in data:
            station_name = entry['station_name']
            temperature = entry['temperature']
            humidity = entry['humidity']
            cursor.execute("INSERT INTO stations (station_name, temperature, humidity) VALUES (?, ?, ?)", 
                           (station_name, temperature, humidity))
        
        conn.commit()
        conn.close()
        '''
        print("Data inserted successfully")
    else:
        print("Failed to fetch data from the API")

# Function to bulk insert data into the database
def bulk_insert_station_data(data):
    conn = connect_db()
    cursor = conn.cursor()

    current_time = datetime.datetime.now()


    for i in data:
        i.append(current_time)

    #print(current_time)
    
    #print(data)
    # Bulk insert data into the database
    cursor.executemany("INSERT INTO StationData (BikesAvailable, DocksAvailable, StationId, Datetime) VALUES (?, ?, ?, ?)", data)
    
    conn.commit()
    conn.close()
    print("Data inserted successfully")

# Schedule the job to run once
#schedule.every(2).seconds.do(fetch_and_insert_data)
#schedule.every().hour.at(":15").do(fetch_and_insert_data)
# Calculate the minutes for scheduling


schedule.every().hour.at(":00").do(fetch_and_insert_data)
schedule.every().hour.at(":05").do(fetch_and_insert_data)
schedule.every().hour.at(":10").do(fetch_and_insert_data)
schedule.every().hour.at(":15").do(fetch_and_insert_data)
schedule.every().hour.at(":20").do(fetch_and_insert_data)
schedule.every().hour.at(":25").do(fetch_and_insert_data)
schedule.every().hour.at(":30").do(fetch_and_insert_data)
schedule.every().hour.at(":35").do(fetch_and_insert_data)
schedule.every().hour.at(":40").do(fetch_and_insert_data)
schedule.every().hour.at(":45").do(fetch_and_insert_data)
schedule.every().hour.at(":50").do(fetch_and_insert_data)
schedule.every().hour.at(":55").do(fetch_and_insert_data)

def create_station_data_db():
    conn = sqlite3.connect('station_data.db')
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS StationData (
            Datetime       NUMERIC NOT NULL,
            StationId      TEXT    NOT NULL,
            BikesAvailable INTEGER NOT NULL,
            DocksAvailable INTEGER NOT NULL,
            StationDataId  INTEGER PRIMARY KEY AUTOINCREMENT
                                UNIQUE
                                NOT NULL
        );
        '''
    )
    conn.commit()
    conn.close()

create_station_data_db()

# Allow the scheduler to run the scheduled jobs
while True:
    schedule.run_pending()
    time.sleep(1)
