import pandas as pd
from io import StringIO
import re

def parse_height_restriction_to_cm(height_str): #Curated to fetch from sample data
    if not isinstance(height_str, str) or height_str.strip().lower() == 'none':
        return 0  # No restriction

    cm_match = re.search(r'\((\d+)\s*cm\)', height_str)
    if cm_match:
        return int(cm_match.group(1))

    inch_match = re.search(r'(\d+)"', height_str)
    if inch_match:
        return int(int(inch_match.group(1)) * 2.54) 

    return float('inf')

def get_ride_details_map(original_rides_info_df):
        # dict for ride details by name
    ride_details_map = {}
    for index, row in original_rides_info_df.iterrows():
        ride_details_map[row['Ride Name']] = row
    return ride_details_map

def pick_rides_based_on_constraints(
    original_rides_info_df,      # Ride details
    mcts_ranked_names,           # List of ride names
    user_age_years=None,         # User Age(years)
    user_height_cm=None,         # User Height(cm)
    preferred_categories=None    # List of preferred ride categories (e.g., ["Thrill Ride", "Boat Ride"])
):
    '''

    Filters the MCTS ranked list of rides based on user constraints.

    '''
    # dict for ride details by name
    ride_details_map = get_ride_details_map(original_rides_info_df)

    filtered_and_ranked_rides = []

    for ride_name in mcts_ranked_names:
        if ride_name not in ride_details_map:
            continue

        details = ride_details_map[ride_name]
        passes_constraints = True

        if user_age_years is not None:
            pass

        if not passes_constraints:
            continue

        # 2. Height Check
        if user_height_cm is not None:
            required_height_cm = parse_height_restriction_to_cm(details['Height Restriction'])
            if user_height_cm < required_height_cm:
                passes_constraints = False
        
        if not passes_constraints:
            continue

        # 3. Ride Category Check
        if preferred_categories and isinstance(preferred_categories, list) and len(preferred_categories) > 0:
            if details['Ride Category'] not in preferred_categories:
                passes_constraints = False
        
        if not passes_constraints:
            continue

        if passes_constraints:
            filtered_and_ranked_rides.append(ride_name)
            
    return filtered_and_ranked_rides

def get_ride_wait_time(ride_wait_time_str):
    numbers = re.findall(r'\d+', ride_wait_time_str)
    if numbers:
        return int(numbers[-1])
    else:
        return None

def ride_itineary_for_user(time_at_park, original_rides_info_df, recommended_rides, mcts_map, preference):
    ride_itineary = []
    # dict for ride details by name
    ride_details_map = get_ride_details_map(original_rides_info_df)

    all_itineary = {}
    for i in range(len(recommended_rides)):
        cur_itineary = []
        time_completed = 0
        for j in range(i, len(recommended_rides)):
            ride_name = recommended_rides[j]
            details = ride_details_map[ride_name]

            # ride_total_time = ride_duration + ride_wait_time
            ride_wait_time = get_ride_wait_time(details['Avg. Weekly Wait Time (Past 5 Years)'])
            # Can add another 10minutes for travel time between ride locations.
            ride_total_time =  details['Ride Duration(Minutes)'] + ride_wait_time 
            if time_completed + ride_total_time <= time_at_park:
                cur_itineary.append(ride_name)
                time_completed += ride_total_time
            else:
                continue
        all_itineary[str(cur_itineary)] = cur_itineary

    res = []

    if preference == 'popularity':
        max_score = float('-inf')
        for key, val in all_itineary.items():
            score = 0.0
            for ride in val:
                score += abs(mcts_map[ride])
                if score >= max_score:
                    max_score = score
                    res = val
        return res
    else:
        #To maximize rides per user preferance
        max_num = 0
        for key, val in all_itineary.items():
            temp_num = len(val)
            if temp_num >= max_num:
                max_num = temp_num
                res = val
        return res





