from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import time

url = "https://us-east-1-1.aws.cloud2.influxdata.com/"
token = "5ICGOzZIWyxtbikllvrsP9D1zevtxxBjbH3I6KE4_f5xL78eo_IK877q6webvC84vgwgPGNHwGjOzV4BRwbrXw=="
org = "PPU"
bucket = "tempreture"

def write_test_data():
    client = InfluxDBClient(url=url, token=token, org=org)
    write_api = client.write_api(write_options=SYNCHRONOUS)

 
    for record in data:
        point = (
            Point("switch_temperature")
            .tag("switch_ip", record["switch_ip"])
            .field("temperature", record["temperature"])
            .time(time.time_ns(), WritePrecision.NS)
        )
        write_api.write(bucket=bucket, org=org, record=point)

    client.close()


def display_temperatures_influxdb():
    client = InfluxDBClient(url=url, token=token, org=org)
    query = f'from(bucket: "{bucket}") |> range(start: -1h) |> filter(fn: (r) => r["_measurement"] == "switch_temperature")'
    tables = client.query_api().query(query, org=org)

    print("Switch Temperatures:")
    print("---------------------")
    if not tables:
        print("No data found.")
    else:
        for table in tables:
            for row in table.records:
                print(f"Switch IP: {row['switch_ip']}, Temperature: {row['_value']}°C")

if __name__ == "__main__":
    write_test_data()
    display_temperatures_influxdb()

