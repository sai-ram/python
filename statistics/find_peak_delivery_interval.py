import csv
from datetime import datetime, timedelta
from collections import deque


def find_peak_delivery_interval(filename):
    delivery_times = []

    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            delivery_time = datetime.strptime(row['delivery_time_utc'], '%Y-%m-%d %H:%M:%S')
            delivery_times.append(delivery_time)

    delivery_times.sort()
    max_count = 0
    max_interval_start = None
    current_window = deque()

    for time in delivery_times:
        current_window.append(time)
        while (time - current_window[0]) > timedelta(hours=2):
            current_window.popleft()
        if len(current_window) > max_count:
            max_count = len(current_window)
            max_interval_start = current_window[0]

    # Comparing with median-based method
    median_time = delivery_times[len(delivery_times) // 2]
    median_interval_start = median_time - timedelta(hours=1)
    median_count = sum(
        1 for t in delivery_times if median_interval_start <= t <= median_interval_start + timedelta(hours=2))

    max_interval_end = max_interval_start + timedelta(hours=2)
    print(
        f"Peak Interval: {max_interval_start.strftime('%H:%M:%S')} to {max_interval_end.strftime('%H:%M:%S')}, Count: {max_count}")
    print(
        f"Median Interval: {median_interval_start.strftime('%H:%M:%S')} to {(median_interval_start + timedelta(hours=2)).strftime('%H:%M:%S')}, Count: {median_count}")

    # Efficiency comparison
    if max_count > median_count:
        print(f"The sliding window approach was better by {100*(max_count - median_count)/median_count:.2f}%")
    elif max_count < median_count:
        print(
            "The median-based method identified a more populated interval, which is unlikely but possible due to distribution characteristics.")
    else:
        print("Both methods identified intervals with the same number of deliveries.")


# Assuming the CSV file is named 'delivery_records.csv'
print(f"First, we will do this for the first test file")
find_peak_delivery_interval('delivery_records.csv')
print(f"Now, we will do this for the second test file")
find_peak_delivery_interval('uniform_delivery_records.csv')
print(f"Now, we will do this for the third test file")
find_peak_delivery_interval('bimodal_delivery_records.csv')