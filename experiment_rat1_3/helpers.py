from flask import session, make_response #stores user

import numpy as np
import random
from .db import Player, Board

#gets current user from data
def current_user():
    return session.get("user")

#gets player.id object for current user, if none return none.
def current():
    return Player.get_or_none(Player.id == current_user())

#gets board associated with player, if none return none.
def current_board():
    return Board.get_or_none(Board.player == current_user())

#setting up api_errors.
def api_error(message, status=404, **kwargs):
    response = {"message": message, **kwargs}
    return make_response(response, status)


def softmax(x, temperature=0.1):
    e_x = np.exp(np.array(x) / temperature)
    return e_x / e_x.sum(axis=0)

#def weighted_sample_without_replacement(population, weights, k=2):

    #population = list(population)  # Make a copy to prevent altering the original list
    #weights = list(weights)  # Make a copy to prevent altering the original list
    #combined = list(zip(population, weights))
    
    #chosen = []

    #for _ in range(k):
       # if not combined:  # If there's no one left to choose from, break the loop
           # break

        # Normalize weights and create a probability distribution
        #weights = softmax([x[1] for x in combined])
        #p = np.array(weights)
       # p /= p.sum()

        # Select one index from the available ones
        #chosen_index = np.random.choice(len(combined), p=p)

        # Add the chosen index to the chosen ones and remove it from the available ones
        #chosen.append(combined[chosen_index][0])
        #del combined[chosen_index]

    #return chosen

def weighted_sample_without_replacement(population, weights, k=2):
    # Combine population and weights, and sort in descending order of weights
    combined = sorted(zip(population, weights), key=lambda x: x[1], reverse=True)
    
    # Select the top k entries from the sorted list
    chosen = [item[0] for item in combined[:k]]

    return chosen


