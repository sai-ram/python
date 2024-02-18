import csv
from datetime import datetime, timedelta
import random


def generate_bimodal_csv(filename, num_records=100000):
    start_time = datetime.strptime('2022-01-01 08:00:00', '%Y-%m-%d %H:%M:%S')
    end_time = datetime.strptime('2022-01-01 19:00:00', '%Y-%m-%d %H:%M:%S')

    # Define the peaks for the bimodal distribution
    peak1_start = datetime.strptime('2022-01-01 10:00:00', '%Y-%m-%d %H:%M:%S')
    peak1_end = datetime.strptime('2022-01-01 11:00:00', '%Y-%m-%d %H:%M:%S')

    peak2_start = datetime.strptime('2022-01-01 14:00:00', '%Y-%m-%d %H:%M:%S')
    peak2_end = datetime.strptime('2022-01-01 15:00:00', '%Y-%m-%d %H:%M:%S')

    low_period_start = datetime.strptime('2022-01-01 11:30:00', '%Y-%m-%d %H:%M:%S')
    low_period_end = datetime.strptime('2022-01-01 12:30:00', '%Y-%m-%d %H:%M:%S')

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['package_id', 'delivery_time_utc'])

        for i in range(num_records):
            rand = random.random()  # Generate a random float between 0.0 to 1.0

            # Adjust these weights to control the distribution
            if rand < 0.45:  # Approximately 45% of deliveries in the first peak
                minutes_offset = random.randint(0, int((peak1_end - peak1_start).total_seconds() // 60))
                delivery_time = peak1_start + timedelta(minutes=minutes_offset)
            elif rand < 0.9:  # Approximately 45% of deliveries in the second peak
                minutes_offset = random.randint(0, int((peak2_end - peak2_start).total_seconds() // 60))
                delivery_time = peak2_start + timedelta(minutes=minutes_offset)
            else:  # Spread the remaining 10% in the non-peak (but excluding the low delivery period)
                while True:
                    minutes_offset = random.randint(0, int((end_time - start_time).total_seconds() // 60))
                    delivery_time = start_time + timedelta(minutes=minutes_offset)
                    if not (low_period_start <= delivery_time <= low_period_end):
                        break

            writer.writerow([i, delivery_time.strftime('%Y-%m-%d %H:%M:%S')])


# Example usage
generate_bimodal_csv('bimodal_delivery_records.csv')
