from datetime import datetime, timedelta, timezone


d = datetime.now(timezone.utc).astimezone()  # local time
utc_offset = d.utcoffset() // timedelta(seconds=1)
print(utc_offset)
dd = datetime.now().date()

print(dd)
