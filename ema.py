import csp
from csp import ts
import requests
import numpy as np
from datetime import datetime, timedelta
import random
import matplotlib.pyplot as plt

@csp.node
def fetch_citibike_data(trigger: ts[bool]) -> ts[dict]:
    if csp.ticked(trigger):
        url = "https://gbfs.lyft.com/gbfs/2.3/bkn/en/station_status.json"
        response = requests.get(url)
        data = response.json()
        return data


@csp.node
def update_station_data(data: ts[dict], window_size: int) -> ts[dict]:
    with csp.state():
        s_station_data = {}

    if csp.ticked(data):
        stations = data["data"]["stations"]
        timestamp = datetime.fromtimestamp(data["last_updated"])

        for station in stations:
            station_id = station["station_id"]
            num_bikes = station["num_bikes_available"]

            if station_id not in s_station_data:
                s_station_data[station_id] = {"timestamps": [], "num_bikes": []}

            s_station_data[station_id]["timestamps"].append(timestamp)
            s_station_data[station_id]["num_bikes"].append(num_bikes)

            # Remove data points outside the window
            while len(s_station_data[station_id]["timestamps"]) > window_size:
                s_station_data[station_id]["timestamps"].pop(0)
                s_station_data[station_id]["num_bikes"].pop(0)

        return s_station_data


@csp.node
def peturbate_number_of_bikes_to_simulate_users(x: ts[float]) -> ts[float]:
    if csp.ticked(x):
        if random.random() > 0.8:
            return x + random.randint(-2, 2)
        return x


@csp.node
def my_node_does_something(x: ts[float]) -> ts[float]:
    # return sum of all counts
    with csp.start():
        x.setTickCount(100)

    sum = 0
    for i in range(min(x.count(), 100)):
        sum += csp.value_at(x, -i)
    return sum

@csp.graph
def citibike_graph(window_size: int, interval: timedelta):
    trigger = csp.timer(interval)
    data = fetch_citibike_data(trigger)
    station_data = update_station_data(data, window_size)

    all_station_data = {}
    for station_id in all_station_ids[:3]: # data in station_data.items():
        # extract individual station
        num_bikes_at_station = csp.apply(station_data, lambda x, station_id=station_id: x[station_id]["num_bikes"][0], float)

        # inject some simulated randomness
        num_bikes_at_station_with_simulated_use = peturbate_number_of_bikes_to_simulate_users(num_bikes_at_station)

        # calculate ema
        ewm_per_station = csp.stats.ema(num_bikes_at_station_with_simulated_use, halflife=interval/2)
        all_station_data[station_id] = ewm_per_station
        #x = my_node_does_something(ewm_per_station)
        #csp.print(
        csp.print(f'w-{station_id}', ewm_per_station) #"Weighted Average for Station {station_id}: {weighted_avg}")
        #csp.add_graph_output(f'w-{station_id}', ewm_per_station, tick_count=1)

    #csp.print('x', all_station_data)

if __name__ == "__main__":
    window_size = 8  # Number of 15-minute intervals in 2 hours
    interval = timedelta(seconds=2)  # 15-minute interval

    csp.run(citibike_graph, window_size, interval, realtime=True, endtime=timedelta(seconds=20))
    # fix, ax = plt.subplots()