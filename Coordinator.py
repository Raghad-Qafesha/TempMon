import pika
import json
import sqlite3

def coordinator():
    conn = sqlite3.connect('cisco.db')
    cursor = conn.cursor()
    cursor.execute("SELECT Sw_Ip, Cicco, oid FROM cisco")
    switch_details = cursor.fetchall()
    conn.close()
    return switch_details

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='Rabitmq')
    switch_ips = coordinator()
    for Sw_Ip, Cicco, oid in switch_ips:
        command = {"command": "collecter", "Sw_Ip": Sw_Ip, 'Cicco': Cicco, 'oid': oid}
        channel.basic_publish(exchange='',
                              routing_key='Rabitmq',
                              body=json.dumps(command))
        print(f" Sent command to collect temperature for switch at {Sw_Ip}")

    connection.close()

if __name__ == '__main__':
    main()

