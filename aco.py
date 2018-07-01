import random as rn
import numpy as np
from numpy.random import choice as np_choice

n_ants=0
n_best=0
n_iterations=0
decay=0
alpha=0
beta=0
pheromone=0
all_inds=0

def pick_move(pheromone, dist, visited):
   pheromone = np.copy(pheromone)
   #Make zero if the path has been visited
   pheromone[list(visited)] = 0

   #Ant makes a decision on what city to go using this formula
   row = pheromone ** alpha * (( 1.0 / dist) ** beta)

   #Probability formula
   norm_row = row / row.sum()

   #Move randomly using probability (select path to go using probability)
   #p=probability
   #Get index of an element that has bigger probability 
   move = np_choice(all_inds, 1, p=norm_row)[0]
   #print(move)

   #Return path that randomly selected
   return move

def spread_pheronome(all_paths, n_best, shortest_path):
   global pheromone, distances
   # sorted a path form small to big (with values to be shorted are values on second collumn)
   sorted_paths = sorted(all_paths, key=lambda x: x[1])

   for path, dist in sorted_paths[:n_best]:
      print "{0} ## {1}".format(path, dist)
      for move in path:
         print (move)
         # ant deposits a pheromone on the way that its travelled 
         # the amount of pheromone that the ant deposit is (1/distances between 2 cities)
         pheromone[move] += 1.0 / distances[move]

def gen_path_dist(path):
   global distances
   total_dist = 0
   for ele in path:
      total_dist += distances[ele]
   return total_dist

def gen_path(start):
   global pheromone, distances
   path = []
   #Start path to 0
   visited = set()
   visited.add(start)
   #prev = start
   prev = start
   for i in xrange(len(distances) - 1):
      move = pick_move(pheromone[prev], distances[prev], visited)
      #Append path
      path.append((prev, move))
      #Change previous path to move path after append path
      prev = move
      #add Path that has been moved to visited, so the path that has
      #been visited can be made to zero
      visited.add(move)
   path.append((prev, start)) # going back to where we started    
   return path

def gen_all_paths():
   all_paths = []
   for i in xrange(n_ants):
      path = gen_path(0) #0 is start
      all_paths.append((path, gen_path_dist(path)))
   return all_paths

def aco(distances_, n_ants_, n_best_, n_iterations_, decay_, alpha_=1, beta_=1):
   global distances, n_ants, n_best, n_iterations, decay, alpha, beta, pheromone, all_inds
   distances = distances_
   n_ants = n_ants_
   n_best = n_best_
   n_iterations = n_iterations_
   decay = decay_
   alpha = alpha_
   beta = beta_
   pheromone = np.ones(distances_.shape) / 10
   all_inds=range(len(distances_))

   shortest_path = None
   all_time_shortest_path = ("placeholder", np.inf)
   for i in range(n_iterations_):
      #Get all paths
      all_paths = gen_all_paths()
      
      #Spread Pheromone
      spread_pheronome(all_paths, n_best_, shortest_path=shortest_path)

      #Get the minimal value in array all_paths in collumn 2
      #example :
      # a = [(0, 8), (3, 7), (2, 6), (1, 9), (4, 5)]
      # min(a, key=lambda x: x[1])
      # the result is : (4, 5)
      # x[1] means second collumn
      # x[0] means first collumn
      # sortest path = (path )

      #Get the shortest path in all paths, based on its distance (x[1])
      shortest_path = min(all_paths, key=lambda x: x[1])

      print "shortest path : ## {0}".format(shortest_path)

      # if total distance < infinity then :
      # all_time_shortest_path = shortest_path
      if shortest_path[1] < all_time_shortest_path[1]:
        all_time_shortest_path = shortest_path

      # pheromone decay (pheromone * decay rate)           
      pheromone = pheromone * decay            

      #return the shortest path that founded by the ants
   print all_time_shortest_path
   return all_time_shortest_path


#============================
#let's try the ACO algorithm
distances = np.array([[np.inf, 2, 2, 5, 7],
                      [2, np.inf, 4, 8, 2],
                      [2, 4, np.inf, 1, 3],
                      [5, 8, 1, np.inf, 2],
                      [7, 2, 3, 2, np.inf]])

aco(distances, 1, 1, 10, 0.95, 1, 1)
