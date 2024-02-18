import csv
from datetime import datetime, timedelta
import random


def generate_test_csv(filename, num_records=100000):
    start_time = datetime.strptime('08:00:00', '%H:%M:%S')
    end_time = datetime.strptime('19:00:00', '%H:%M:%S')
    total_minutes = int((end_time - start_time).total_seconds() / 60)

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['package_id', 'delivery_time_utc'])

        for i in range(num_records):
            minutes_offset = random.randint(0, total_minutes)
            delivery_time = start_time + timedelta(minutes=minutes_offset)
            writer.writerow([i, delivery_time.strftime('%Y-%m-%d %H:%M:%S')])


generate_test_csv('delivery_records.csv')
