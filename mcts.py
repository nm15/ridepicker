import pandas as pd
from io import StringIO
import numpy as np
import random

def score_ride_in_rollout(ride_idx, rides_df):
    ride_data = rides_df.iloc[ride_idx]
    
    popularity_map = {'High': 3, 'Medium': 2, 'Low': 1}
    popularity_score = popularity_map.get(ride_data['Popularity'], 1) 
    
    wait_time_str = ride_data['Avg. Weekly Wait Time (Past 5 Years)']
    avg_wait = 30 # Default
    if isinstance(wait_time_str, str) and '-' in wait_time_str:
        try:
            low, high = wait_time_str.replace(' min', '').split('-')
            avg_wait = (float(low) + float(high)) / 2
        except ValueError:
            pass 
            
    # Score: 
    # Higher popularity is better, lower wait time is better.
    # The coefficient balances importance.
    score = (popularity_score * 25) - avg_wait
    return score

# --- MCTS Node Definition ---
class MCTSNode:
    def __init__(self, state, parent=None):
        self.state = state  
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0  # Total value

    def is_fully_expanded(self, all_possible_next_actions):
        return len(self.children) == len(all_possible_next_actions)

    def best_child(self, c_param=1.4):
        choices_weights = [
            (child.value / child.visits) + c_param * np.sqrt((2 * np.log(self.visits) / child.visits))
            if child.visits > 0 else float('inf')
            for child in self.children
        ]
        return self.children[np.argmax(choices_weights)]

    def expand(self, action, rides_df):
        new_node = MCTSNode(state=action, parent=self)
        self.children.append(new_node)
        return new_node

    def rollout(self, rides_df):
        if isinstance(self.state, int):
            return score_ride_in_rollout(self.state, rides_df)
        elif isinstance(self.state, list): # If state is a sequence
            current_score = 0
            for ride_idx in self.state:
                current_score += score_ride_in_rollout(ride_idx, rides_df)
            return current_score
        return 0

    def backpropagate(self, result):
        self.visits += 1
        self.value += result
        if self.parent:
            self.parent.backpropagate(result)

#MCTS
def monte_carlo_tree_search_for_ranking(rides_df, iterations=10000):
    root = MCTSNode(state=None)
    all_ride_indices = list(range(len(rides_df)))

    for ride_idx_to_explore in all_ride_indices:        
        child_node = None
        for child in root.children:
            if child.state == ride_idx_to_explore:
                child_node = child
                break
        if child_node is None:
            child_node = root.expand(ride_idx_to_explore, rides_df) # 'state' of child is ride_idx

        for _ in range(iterations // len(all_ride_indices) + 1): # iterations
            result = child_node.rollout(rides_df) 
            child_node.backpropagate(result) # Backpropagate

    ranked_rides_info = []
    for child_node in root.children:
        ride_idx = child_node.state # which is the ride index
        avg_score = child_node.value / child_node.visits if child_node.visits > 0 else float('-inf')
        ranked_rides_info.append({
            'Ride Name': rides_df.iloc[ride_idx]['Ride Name'],
            'Avg MCTS Score': avg_score,
            'Visits': child_node.visits
        })
    
    ranked_df = pd.DataFrame(ranked_rides_info).sort_values(by='Avg MCTS Score', ascending=False)
    return ranked_df
