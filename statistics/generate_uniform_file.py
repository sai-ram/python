import csv
from datetime import datetime, timedelta
import random


def generate_uniform_csv(filename, num_records=100000):
    start_time = datetime.strptime('2022-01-01 08:00:00', '%Y-%m-%d %H:%M:%S')
    end_time = datetime.strptime('2022-01-01 19:00:00', '%Y-%m-%d %H:%M:%S')
    delta = end_time - start_time

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['package_id', 'delivery_time_utc'])

        for i in range(num_records):
            random_seconds = random.randint(0, int(delta.total_seconds()))
            delivery_time = start_time + timedelta(seconds=random_seconds)
            writer.writerow([i, delivery_time.strftime('%Y-%m-%d %H:%M:%S')])


# Example usage
generate_uniform_csv('uniform_delivery_records.csv')
