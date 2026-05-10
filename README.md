# Simple Model UN Allocation Script 

Author: Harold Gao

Here I present a python script to allocate delegates to model UN teams. There are `C` countries, with `D` delegates, each delegate should be assigned to a country, and a country has atmost one delegate. Each delegate also has a first preference country, second preference country, and `order` integer field, which represents a timestamp the delegate's preference came through. 

## Rules 

- For each delegate starting from the lowest to highest `order`, Match the delegate to their first or second preference if possible. Otherwise add to list of unmatched delegates. 
- In the end, unmatched delegates are randomly assigned remaining countries. If the remaining number of delegates exceed the number of countries, prioritise random assignment of delegates with lower `order`.


## Usage 

- Download the script, go to "Code" in the github page, and click "Download ZIP".
- Extract the downloaded ZIP file.
- If not already, please install `python3` on your computer. `https://www.python.org/downloads/`
- Change to this folder through the command line. On Mac or Linux this will be `cd <path_to_this_folder>`
- Then, run `python3 allocate.py <countries_csv> <delegates_csv>` where `countries_csv` is a list of countries, and `delegates_csv` is a list of delegates and their preferences.
- If successful and that CSV files are formatted correctly, this will produce a `matched.csv` file containing a pair of names and their matched countries.

You may want to run the provided example csv files:

```
python3 allocate.py examples/193countries.csv examples/delegates.csv
```

## Countries CSV File 

Simply list the countries as follows, each row has just one entry. Country names with commas need to be wrapped in string laterals (e.g. `Korea, South` must turn into `"Korea, South"`)

```
Australia
New Zealand
America
Argentina
Germany
France
"Korea, South"
.
.
.
```

## Delegates CSV File 

Each row must have the following fields in order separated by commas: name, first preferred country, second preferred country, order, where order is a decimal number. 

Example:
```
John, Australia, New Zealand, 10
Alex, America, Canada, 5
```
The order doesn't need to represent an actual timestamp, as long as it captures the order in which these entries come through. If you are working with human-readable timestamps such as "March 24th, 12:33 AM 2025", I would recommend converting them to Unix timestamp as a single number. `https://www.unixtimestamp.com/`