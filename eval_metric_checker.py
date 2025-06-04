import re

def parse_height_restriction(height_str):
    if not height_str or height_str.lower() == 'none':
        return None
    match = re.search(r'(\d+)\s*cm', height_str)
    if match:
        return int(match.group(1))
    match = re.search(r'(\d+)\s*"', height_str)
    if match:
        return int(round(int(match.group(1)) * 2.54))
    return None

def can_ride(ride, user_age, user_height_cm, accompanied_by_14plus=True):
    # Age check: "Children under 7 must be accompanied by 14+ year old"
    if 'under 7' in ride['Age Restriction']:
        if user_age < 7 and not accompanied_by_14plus:
            return False
    # Height check
    min_height_cm = parse_height_restriction(ride['Height Restriction'])
    if min_height_cm is not None and user_height_cm < min_height_cm:
        return False
    return True

def verify_itinerary(itinerary, ride_data, user_age, user_height_cm):
    ride_lookup = {ride['Ride Name']: ride for ride in ride_data}
    for ride_name in itinerary:
        if ride_name not in ride_lookup:
            print(f"Ride '{ride_name}' not found in data!")
            return False
        ride = ride_lookup[ride_name]
        if not can_ride(ride, user_age, user_height_cm):
            print(f"User does not meet requirements for '{ride_name}'")
            return False
    return True

ride_data = [
    {'Ride Name': 'Indiana Jones Adventure', 'Age Restriction': 'Children under 7 must be accompanied by 14+ year old', 'Height Restriction': '46" (117 cm)'},
    {'Ride Name': 'Dumbo the Flying Elephant', 'Age Restriction': 'Children under 7 must be accompanied by 14+ year old', 'Height Restriction': 'None'},
    {'Ride Name': 'Pinocchio\'s Daring Journey', 'Age Restriction': 'Children under 7 must be accompanied by 14+ year old', 'Height Restriction': 'None'},
    {'Ride Name': 'Storybook Land Canal Boats', 'Age Restriction': 'Children under 7 must be accompanied by 14+ year old', 'Height Restriction': 'None'},
    {'Ride Name': 'Snow White\'s Enchanted Wish', 'Age Restriction': 'Children under 7 must be accompanied by 14+ year old', 'Height Restriction': 'None'},
    {'Ride Name': 'Casey Jr. Circus Train', 'Age Restriction': 'Children under 7 must be accompanied by 14+ year old', 'Height Restriction': 'None'}
]

user_age = 10
user_height_cm = 120
itinerary = ['Pinocchio\'s Daring Journey', 'Storybook Land Canal Boats', 'Snow White\'s Enchanted Wish', 'Casey Jr. Circus Train']

result = verify_itinerary(itinerary, ride_data, user_age, user_height_cm)
print("Itinerary valid for user:", result)
