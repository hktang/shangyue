# shangyue: Broadcast moonrise time via Google Nest

## Introduction

* `get_moonrise.py` retrieves the daily moonrise data using the
  [IPGeolocation][1] API.
* `notify_moonrise.py` broadcasts an announcement via Google Home devices if
  the moon rises within a certain timeframe before the current time.

## Usage

To retrieve annual moonrise data, update the coordinates in `get_moonrise.py`
and run:

```bash
python get_moonrise.py
```

To check if the moon has recently risen (the default is 10-20 minutes
before the check), run:

```bash
python notify_moonrise.py
```

Adjust the start/end times in the script to specify when you want to
receive reminders (and by extension when not to).

## Automation using a cron job

Use a cronjob to grab annual moonrise data for your location, and
run the notification script at certain intervals. In the example
below, the system will retrieve moonrise data of the following year
first of January each year. It then checks whether the moon has risen
at 10-minute intervals between 15:00 and 23:00.

```txt
0     0      1  1  *  /usr/bin/python /path/to/get_moonrise.py
*/10  15-23  *  *  *  /usr/bin/python /path/to/notify_moonrise.py
```

## Requirements

[Assistant Relay][2], for relaying your announcements to Google Nest.

## Credit

[IPGeolocation][1], for providing the moonrise data.

[1]: https://github.com/IPGeolocation
[2]: https://github.com/greghesp/assistant-relay
