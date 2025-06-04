import pandas as pd
from io import StringIO
import mcts 
import inference
import csv
from datetime import datetime, timedelta
import pprint
from tabulate import tabulate

def read_data():
      filename = 'rides_data.csv'
      rides_df = []
      try:
         rides_df = pd.read_csv(filename)
         return rides_df
      except FileNotFoundError:
         print(f"Error: The file '{filename}' was not found in the current directory.")
         return rides_df
      except pd.errors.EmptyDataError:
         print(f"Error: The file '{filename}' is empty or does not contain valid CSV data.")
         return rides_df
      except Exception as e:
         print(f"An error occurred: {e}")
         return rides_df

def get_park_time(start_time_str, end_time_str):
    # Define the format for parsing. %I for 12-hour, %p for AM/PM.
    time_format = "%I:%M%p"
    try:
        norm_start_time = start_time_str.replace(" ", "").upper()
        norm_end_time = end_time_str.replace(" ", "").upper()

        start_time_obj = datetime.strptime(norm_start_time, time_format)
        end_time_obj = datetime.strptime(norm_end_time, time_format)

    except ValueError as e:
        return f"Error: Invalid time format. Please use HH:MM AM/PM. Details: {e}"

    # Calculate the difference
    time_difference_delta = end_time_obj - start_time_obj
    if time_difference_delta.total_seconds() < 0:
        time_difference_delta += timedelta(days=1)

    difference_in_minutes = int(time_difference_delta.total_seconds() / 60)
    return difference_in_minutes

def pretty_print_indexed_tabulate(data_list):
    if not data_list:
        print("List is empty.")
        return
    table_data = []
    for index, value in enumerate(data_list):
        table_data.append([index+1, str(value)])
    headers = ["Ride #", "Ride Name"]
    print("--- Rides to go in order as below ---")
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    print("---------Enjoy your rides------------")


def run_algo(config, rides_df):
      ride_sequences = mcts.monte_carlo_tree_search_for_ranking(rides_df, 100)
      #print("Ride sorting to pick based on MCTS:")
      #print(ride_sequences)
         
      mcts_ranked_ride_names = ride_sequences['Ride Name'].tolist()
      mcts_ranked_ride_scores = ride_sequences['Avg MCTS Score'].tolist()
      mcts_map = {}
      for i in range(len(mcts_ranked_ride_names)):
         mcts_map[mcts_ranked_ride_names[i]] = mcts_ranked_ride_scores[i]

      user_age = config['age']
      user_height = config['height'] #in inches
      user_categories = config['categories']

      print(f"User Profile: Age={user_age}, Height={user_height}cm, Preferred Categories={user_categories}")

      recommended_rides = inference.pick_rides_based_on_constraints(
         rides_df,
         mcts_ranked_ride_names,
         user_age_years=user_age,
         user_height_cm=user_height,
         preferred_categories=user_categories
      )

      start_time = config['start']
      end_time = config['end']
      time_at_park = get_park_time(start_time, end_time)
      final_ride_itineary = inference.ride_itineary_for_user(time_at_park, rides_df, recommended_rides, mcts_map, ' ')
      pretty_print_indexed_tabulate(final_ride_itineary)
         