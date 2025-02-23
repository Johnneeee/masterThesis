import datetime

ja = datetime.datetime.strptime("0:00:12","%H:%M:%S").time()

print(ja)
# print(datetime.timedelta("0:00:12"))