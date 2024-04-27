import sqlite3
import jsonify

def create_db():
    create_stations_db()
    create_users_db()
    create_orders_db()
    create_contracts_db()

def create_users_db():
    conn = sqlite3.connect('market.db')
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS Users (
        UserId       INTEGER NOT NULL
                            PRIMARY KEY AUTOINCREMENT
                            UNIQUE,
        AccountMoney INTEGER DEFAULT (0),
        FirstName    TEXT    NOT NULL,
        LastName     TEXT    NOT NULL
        );
        '''
    )
    conn.commit()
    conn.close()

def create_stations_db():
    conn = sqlite3.connect('market.db')
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS Stations (
        StationId   INTEGER PRIMARY KEY AUTOINCREMENT
                            UNIQUE
                            NOT NULL,
        StationName TEXT    NOT NULL
        );  
        '''
    )
    conn.commit()
    conn.close()


def create_orders_db():
    conn = sqlite3.connect('market.db')
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS Orders (
            OrderId          INTEGER UNIQUE
                                    PRIMARY KEY AUTOINCREMENT
                                    NOT NULL,
            StationId        INTEGER NOT NULL
                                    REFERENCES Stations (StationId),
            StartTime        NUMERIC,
            EndTime          NUMERIC,
            StartBikeCount   INTEGER NOT NULL,
            EndBikeCount     INTEGER NOT NULL,
            PayoutMultiplier REAL    NOT NULL,
            IsBuy            INTEGER
        );
        '''
    )
    conn.commit()
    conn.close()    


def create_contracts_db():
    conn = sqlite3.connect('market.db')
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS Contracts (
            ContractId INTEGER PRIMARY KEY AUTOINCREMENT
                            UNIQUE
                            NOT NULL,
            UserId     INTEGER REFERENCES Users (UserId) 
                            NOT NULL,
            UserBet    REAL    NOT NULL,
            OrderId    INTEGER REFERENCES Orders (OrderId) 
                            NOT NULL
        );
        '''
    )
    conn.commit()
    conn.close()




def create_station_data_db():
    conn = sqlite3.connect('market.db')
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS StationData (
        Time           INTEGER NOT NULL,
        Date           NUMERIC NOT NULL,
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


def insert_station(station_name):
    conn = sqlite3.connect('market.db')
    cursor = conn.cursor()
    
    # Insert the station into the database
    cursor.execute("INSERT INTO stations (station_name) VALUES (?)", (station_name,))
    
    conn.commit()
    conn.close()

def get_stations():
    conn = sqlite3.connect('market.db')
    cursor = conn.cursor()
    
    # Insert the station into the database
    cursor.execute("SELECT * FROM Stations")
    
    list = cursor.fetchall()

    conn.commit()
    conn.close()

    station_list = []
    for station in list:

        station_dict = {
            'id': station[0],
            'station_name': station[1],
        }
        station_list.append(station_dict)
        
    return station_list
    


# Call the function to create the database
#create_db()