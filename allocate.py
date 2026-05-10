"""
Simple model UN allocator based on preferences and timestamp.
Author: Harold Gao
"""

import csv
import sys 
import random 
from pathlib import Path

if len(sys.argv) != 3:
    print("Usage: python3 allocate.py <countries> <preferences>")
    exit(0)
    
def get_countries(file_name):
    """
    Gets a list of countries from a given csv file
    """
    s = set()
    try:
        with open(file_name, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for country in reader:
                if(len(country) != 1):
                    print(f"Error: each row in {file_name} must have a single entry")
                    exit(0)
                if(country[0] in s):
                    print(f"Warning: found duplicate country {country[0]}, skipping it for now")
                    continue 
                s.add(country[0].strip())
    except FileNotFoundError:
        print(f"Error: cannot find {file_name}")
        exit(0)
            
    return s

def get_delegates(file_name):
    """ 
    Gets a list of delegates from a given csv file.
    """
    l = []
    try:
        with open(file_name, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for delegate in reader:
                if(len(delegate) != 4):
                    print(f"Error: each row in {file_name} must have exactly 4 comma-separated values")
                    exit(0)
                order = int(delegate[3])
                firstPref = delegate[1]
                secondPref = delegate[2]
                name = delegate[0]
                l.append({
                    "name": name,
                    "first_pref": firstPref.strip(),
                    "second_pref": secondPref.strip(),
                    "order": order
                })
    except FileNotFoundError:
        print(f"Error: cannot find {file_name}")
        exit(0)
    except ValueError:
        print(f"Error: the 4th entries in each row must be a number")
        exit(0)
    return l

def matchedEntry(name, country):
    return {"name": name, "country": country}

def match(delegates, countries):
    """ 
    Given a list of delegates and their preferences, timestamp, and 
    a set of countries, match them and return a list of names paired
    with a distinct country using a simple greedy algorithm. 
    If the number of delegates does not equal the number of countries, 
    some delegates/countries may not matched. Furthermore, if delegates
    prefer nonexisting countries, they will be randomly allocated one
    in the end.
    """
    
    # Sort in ascending order by the timestamp (order field in a delegate)
    delegates.sort(key=lambda p: p["order"])
   
    # Delegates that we can't satisfy based on their preferences 
    unallocated_delegates = []
    matched = []
    
    for delegate in delegates:
        fst = delegate["first_pref"]
        snd = delegate["second_pref"]
        name = delegate["name"]
        if fst in countries:
            matched.append(matchedEntry(name, fst))
            countries.remove(fst)
        elif snd in countries:
            matched.append(matchedEntry(name, snd))
            countries.remove(snd)
        else: # Preferences both taken :( 
            unallocated_delegates.append(name)
       
    # Time to process the unmatched delegates! In case there are too many delegates
    # we should probs prioritise the ones with earliest time stamp. 
    clen = len(countries)
    dlen = len(unallocated_delegates)
    to_match = []
    no_match = []
    if dlen > clen:
        to_match = unallocated_delegates[0:clen]
        no_match = unallocated_delegates[clen:]
    else: # we can match all delegates
        to_match = unallocated_delegates
    
    random.shuffle(to_match)
    for delegate, country in zip(to_match, countries):
        matched.append(matchedEntry(delegate, country))
    
    for delegate in no_match:
        matched.append(matchedEntry(delegate, "NO MATCH")) 
    
    return matched

def write_matched(file_name, matched):
    
    """ 
    Writes the matched delegate-country pairs to a CSV file.
    """ 
    
    if Path(file_name).exists():
        print(f"Error: cannot write to file {file_name}, as the file already exists!") 
        exit(0)
    
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for pair in matched:
            writer.writerow([pair["name"], pair["country"]]) 
            
    

countries_csv = sys.argv[1]
preferences_csv = sys.argv[2]
matched_file = "matched.csv"

countries = get_countries(countries_csv)
num_countries = len(countries)
print(f"Info: successfully initialised {str(num_countries)} countries")
delegates = get_delegates(preferences_csv)
num_delegates = len(delegates)
print(f"Info: successfully initialised {str(num_delegates)} delegates")

# Check for number of delegates matching num of countries.
if num_countries != num_delegates:
    print("Warning: number of countries does not match number of delegates! Some countries or delegates will be unallocated")

print("Info: matching delegates to countries")
# Match them!
matched = match(delegates, countries)

print(f"Info: writing matched delegates-country pair to {matched_file}")
write_matched(matched_file, matched)

print(f"Info: success!")