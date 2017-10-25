# pySMHI
Little script for downloading weather forcast from SMHI and saving to a .json file.

Position form freegeoip every 15 min, and a forecast for that position is added to last_position.json in current working directory.

Unicode symbols is from weather_desc.json according to the wsymb2 parameter wind_direction (N/NE/E/SE/S/SW/W/NW) calculated from wind_direction parameter is added to last_position.json.

Finally this data is printed to console. Primarlly for output on desktop through

First ever Python project. Still a work in progress.

If you decide to use and improve this spagetticode, please send me a message.

TODO:
 -Clean up code
 -Implement some kind of config file solution.
 -Fix the check of last forecast
 -Check wind speed parameter (seems to be off.)
