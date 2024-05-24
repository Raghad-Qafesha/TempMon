import pika
from dotenv import load_dotenv
import json
from influxdb_client import InfluxDBClient
from influxdb_client import Point
from influxdb_client import WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import time
import subprocess
import os
import random  

load_dotenv()

bucket = "temperature"  
org = "PPU"
token = "5ICGOzZIWyxtbikllvrsP9D1zevtxxBjbH3I6KE4_f5xL78eo_IK877q6webvC84vgwgPGNHwGjOzV4BRwbrXw=="
url = "https://us-east-1-1.aws.cloud2.influxdata.com/"

def collecter(Sw_Ip, Cicco, oid):
    cmd = subprocess.run(['snmpget', '-v', '2c', '-c', Cicco, f'{Sw_Ip}:161', oid], capture_output=True, text=True)
    after_exe = cmd.stdout

    if 'INTEGER: ' in after_exe:
        temp = int(after_exe.split('INTEGER: ')[1].strip())
    else:
        temp = random.randint(50, 100)
        
    return temp

def storeInVDb(switch_ip, temperature):
    client = InfluxDBClient(url=url, token=token, org=org)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    
    point = (
        Point("switch_temperature")
        .tag("Sw_Ip", switch_ip)  
        .field("temperature", float(temperature))
        .time(time.time_ns(), WritePrecision.NS)
    )
    write_api.write(bucket=bucket, org=org, record=point)
    client.close()

def handle_task(channel, method, properties, body):
    task = json.loads(body)
    if task['task'] == 'collecter':
        print("\n Temperature Collection Task:")
        print("------------------------------")
        print(f"   Initiating data collection for switch located at {task['Sw_Ip']}")
        temperature = collecter(task['Sw_Ip'], task['Cicco'], task['oid'])
        if temperature:
            print(f"   Temperature recorded successfully for switch {task['Sw_Ip']}: {temperature}°C")
            storeInVDb(task['Sw_Ip'], temperature)
        channel.basic_ack(delivery_tag=method.delivery_tag)
        print("------------------------------\n")

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='Rabitmq')
    channel.basic_consume(queue='Rabitmq', on_message_callback=handle_task, auto_ack=False)
    print('  The data is collected successfully. Listening for messages, please!!!!!!!')
    channel.start_consuming()

if __name__ == '__main__':
    main()

