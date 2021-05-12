#goal: Build an ant colony optimization for POI in Austin TX 

# Make a colony of Ants that leave trails of pheremone behind among POI in Austin
 

#p is the evaporation rate, m is the number of ants, tkij is the quantity of pheromone laid on edge (i,j) by ant k
#tkij = Q/LengthofTour if ant K used edge (i,j) in its tour , 0 otherwise 


#experiment: use ant optimization to find better routes than google maps based on obstacles and destinations like POIs 


#visualize the map of Austin with the destination, origin of ants, and moving animated points of
# ants moving to their destinations via their movements 

#make into a dash app 

#Research question: can ACO perform just as well for route navigation? 

# in main function, should allow to select for x many destinations (or all destinations)

#three classes, Ant, Colony 

import networkx as nx 
import sys 
import matplotlib.pyplot as plt
import random
import matplotlib.animation
from matplotlib import rcParams

matplotlib.pyplot.switch_backend('Agg')

class Ant:
    def __init__(self, name, origin, dest_node):
        #self.lat = lat
        #self.lon = lon
        #self.dest_lat = dest_lat
        #self.dest_lon = dest_lon
        self.name = name
        self.dest_node = dest_node
        self.origin = origin
        self.tour_length = 0
        self.path_taken = list()
        self.edges = set() #set of tuples

    def traverse(self, max_nodes, G, Q_const, alpha, beta):
        #random destination location or a maximum set of nodes it's allowed to traverse 
        #get from current node to the next node 

        #ant goes to all cities possible from its current location? 
        num_nodes = 0

        #empty out path taken and tour length
        self.path_taken = list()
        self.path_taken.append(self.current_node)
        self.tour_length = 0

        #restart ant at origin
        #self.current_node = self.origin
        #print("Traversing for: ", self.name)

        undiscovered = list(G.neighbors(self.current_node))

        while num_nodes <= max_nodes and len(undiscovered) > 0:
            
            #get neighbors of current node 
            neighbors = G.neighbors(self.current_node)
            nodes_visited = set(self.path_taken)

            denominator = 0.0  # Tij * 1/dist ij for all neighbors 

            tn = dict()
            numerator = dict()
            distances = dict()

            #calculate numerator 
            for neighbor in neighbors:

                if neighbor in nodes_visited:
                    continue 

                #removed from undiscovered 
                undiscovered.remove(neighbor)

                #calculate likliehood to go there 

                #has other ants gone there?
                dist_ij = G[self.current_node][neighbor]['weight']
                pher_ij = G[self.current_node][neighbor]['pher']
                distances[neighbor] = dist_ij

                tn[neighbor] = (pher_ij**alpha) * (dist_ij**beta)
                
                if tn[neighbor] == 0:
                    print("pher_ij = ", pher_ij, " dist_ij = ", dist_ij)

                #print("dist_ij: ", dist_ij, " pheromone: ", pher_ij, "tn: ", tn)
                denominator += tn[neighbor]

            
            probs = dict()

            for neighbor in tn:
                
                if neighbor in nodes_visited:
                    continue
            
                prob_neighbor = tn[neighbor]/denominator
                probs[neighbor] = prob_neighbor
                

                
            #print("current_node: ", self.current_node, " probs: ", probs)

            #instead of choosing neighbor with highest pheremone, let the

            next_node = random.choices(list(probs.keys()), weights=list(probs.values()), k=1)[0]

            #choose neighbor with highest probability 
            #next_node = max(probs, key=lambda k: probs[k])
            #print("probs: ", probs, " next_node: ", next_node)

            #update tour length
            self.tour_length += distances[next_node]
            #update nodes taken in this partial solution
            self.path_taken.append(next_node)
            
            #update current node 
            self.current_node = next_node 

            new_neighbors = set(list(G.neighbors(self.current_node)))
            #make sure nothing in undiscovered was already taken 
            for node in new_neighbors:
                if node not in self.path_taken:
                    undiscovered.append(node)


   
            #traverse to the next node via computing the probability 
            num_nodes += 1

        return self.path_taken, self.tour_length

    def initialize_random_walk_solution(self, max_nodes, G):

        self.path_taken = list()
        self.tour_length = 0
        self.current_node = self.origin
        undiscovered = set(G.neighbors(self.current_node))
        self.path_taken.append(self.current_node)

        self.edges = set()
        
        while len(undiscovered) > 0:
            #print("current node: ", self.current_node)
            #print("undiscovered: ", undiscovered)
            #print("path_taken:  ", self.path_taken)

            available = list()
            #make sure that on
            for node in list(G.neighbors(self.current_node)):
                if node not in self.path_taken:
                    available.append(node)

            if(len(available) == 0):
                break
            #randomly choose from the current choice of neighbors
            new_node = random.choice(available)

            #print("new_node chosen from neighbors: ", new_node)
            
            G[new_node][self.current_node]['ants'] += 1
            self.tour_length += G[new_node][self.current_node]['weight']

            #add edge to edges list 
            self.edges.add((self.current_node, new_node))


            self.current_node = new_node
            self.path_taken.append(new_node)
            undiscovered.remove(self.current_node)
     
            new_neighbors = set(list(G.neighbors(self.current_node)))

            #make sure nothing in undiscovered was already taken 
            for node in new_neighbors:
                if node not in self.path_taken:
                    undiscovered.add(node)

        return G, self.path_taken, self.tour_length


class Colony: 
    def __init__(self, num_ants, evaporation_rate,Q_const, alpha, beta,G):
        self.num_ants = num_ants
        self.evaporation_rate = evaporation_rate
        self.G = G #this is the operation space 

        self.edge_data = dict()
        self.networks = dict()

    def plot_graph(self, G):
        plt.subplot(121)
        edgewidth = [ d['pher'] for (u,v,d) in G.edges(data=True)]
        pos = nx.circular_layout(G)
        nx.draw(G,pos=pos, with_labels=True, font_weight='bold', width=edgewidth)
        
        plt.show()

    def init_ants(self):
        #declare each ant, give arbitrary destination? (or all the same destination?)
        self.ants = list()
        nodes = list(self.G.nodes)
        dest_node = random.choice(nodes)
        if dest_node == self.origin:
            dest_node = random.choice(nodes)

        for i in range(self.num_ants):
            name = "ant_" + str(i)
            ant = Ant(name, self.origin, dest_node)
            self.ants.append(ant)


    def choose_origin(self):
        nodes = list(self.G.nodes)
        self.origin = random.choice(nodes)

   
    def initialize_solutions(self):
        min_length = 10000 

        paths = dict()

        print(" / / / / Initializing Beginning partial solutions / / / / ")
        
        #ants build partial solution 
        for ant in self.ants:

            self.G, path,length = ant.initialize_random_walk_solution( 1000, self.G)
            #print("ant: ", ant.name, " took: ", length, " traversed nodes: ", path)

            min_length = min(min_length,length)
            paths[ant] = paths


        #save the edge data for self.G 
        self.networks[0] = self.G
        self.edge_data[0] = list(self.G.edges(data=True))

      

    def update_pheremones(self, evaporation_rate, Q_const ):
        
        #for each edge calculate pheromone
        for u,v in list(self.G.edges):

            #go through each ant that used this edge and calculate Q/L 
            #tkij 
            trail_ants = 0.0
            for ant in self.ants:
                
                if (u,v) in ant.edges:
                    #calculate 
                    trail_ants += Q_const/ ant.tour_length

            cur_pher = self.G[u][v]['pher']
            new_pher = (1-evaporation_rate) * cur_pher + trail_ants

            self.G[u][v]['pher'] = new_pher

        return 

    def print_edge_data(self):
        for u,v in list(self.G.edges):
            print("u: ", u, " v: ", v, "num ants: ", self.G[u][v]['ants'], "pher_ij: ",self.G[u][v]['pher'] )

    def print_retro_edge_data(self, num_iterations):
        for i in range(num_iterations):
            edges = self.edge_data[i]

            for (u,v,d) in edges:
                print(i, ": ", u, " <--> ", v, " : ", d)

    def aco(self,num_iterations, evap_rate, Q_const, alpha,beta):

        min_length = 10000 

        paths = dict()

        self.shortest_run = list()

        save_data = dict()

        for i in range(num_iterations):
            #print("Iteration: ", i )
            #ants build partial solution 
            for ant in self.ants:

                path, length = ant.traverse(1000, self.G, Q_const, alpha,beta)
            
                #print("ant: ", ant.name, " took: ", length, " traversed nodes: ", path, " ant is now at: ", ant.current_node)

                min_length = min(min_length,length)
                paths[ant] = paths

            self.shortest_run.append(min_length)
        
            #self.plot_graph()
            #update pheremones 
            self.update_pheremones(evap_rate,Q_const)


            #save edges to be animated later 
            data = list()
            
            for (u,v,d) in self.G.edges(data=True):
            #    print(i, ": ", u, " <--> ", v, " : ", d['pher'] )
                data.append((u,v,d['pher']))
            
            self.edge_data[i] = data #list(self.G.edges(data=True))
            self.networks[i] = self.G
            
            save_data[i] = data #self.G.edges(data=True)
    
        return self.shortest_run,save_data

    def plot_runs(self,ax):
        #fig = plt.figure()
        ax.set_title("Minimum Ant Solution Vs Iterations")
        ax.set_xlabel("Iteration")
        ax.set_ylabel("Minimum Ant Solution")
        X = [i for i in range(len(self.shortest_run))]
        Y = self.shortest_run
        ax.plot(X,Y)
        ax.grid()
      
      



#plot animated Graphs
def update(num, colony):
    ax = colony.ax
    ax.clear()
    ax.set_title("Frame %d"%(num+1), fontweight="bold")
    ax.set_xticks([])
    ax.set_yticks([])
   
    edges = colony.edge_data[num]

    edgewidth = [ 10*d for (u,v,d) in edges]

    #draw the graph with the correct pos and updated edge_data 
    nx.draw(colony.G,pos=colony.pos, with_labels=True, font_weight='bold', edge_color='gray', style='dashed')
    nx.draw(colony.G,pos=colony.pos, with_labels=True, font_weight='bold', width=edgewidth, edge_color='red')

    return 


def plot_graphs(colony, ax, fig, sim_run):
    num_iterations = len(colony.edge_data)
    #fig,ax1,ax2 = plt.subplots(figsize=(6,6), 1,2)
    #colony.ax = ax1
    #colony.fig = fig
    pos = nx.circular_layout(colony.G)
    colony.pos = pos

    ani = matplotlib.animation.FuncAnimation(fig, update,fargs=(colony,), frames=num_iterations, interval=10, repeat=False)
    
    fname_gif = 'assets/aco_' + str(sim_run) + ".gif"
    fname_still = 'assets/still_' + str(sim_run) + ".png"

    print("saving gif to file")
    ani.save(fname_gif, writer='imagemagick', fps=num_iterations)

    plt.savefig(fname_still)

    #plt.show()

    return fig

def build_debug_graph(size_graph):
    
    weights = list(range(1, size_graph ))
    #G = nx.complete_graph(size_graph)

    #G = nx.petersen_graph()
    G = nx.complete_graph(size_graph)
    #G = nx.sedgewick_maze_graph()

    for nodex, nodey in G.edges():
        G[nodex][nodey]['weight'] = random.choice(weights)
        G[nodex][nodey]['pher'] = 1
        G[nodex][nodey]['ants'] = 0
        #print(nodex, "<-->", nodey, " = ", G[nodex][nodey]['weight'])

    return G
         

def alg(num_iterations, num_ants, evap_rate, Q_const, alpha, beta,size_graph, sim_run):
    
    print("num_iterations: ", num_iterations, "num_ants: ", num_ants, " evap_rate: ", evap_rate)
    #set up an arbitrarily small network 
    #G = nx.petersen_graph()
    #G = nx.sedgewick_maze_graph()
    
    G = build_debug_graph(size_graph)

    #define colony 
    colony = Colony(num_ants, evap_rate,Q_const,alpha,beta, G)

    colony.choose_origin()
    colony.init_ants()
    print("initializing solutions")
    colony.initialize_solutions()
    colony.update_pheremones(evap_rate, Q_const)
    
    print("Running ACO")
    shortest_run, data = colony.aco(num_iterations, evap_rate, Q_const, alpha,beta)

    #print("Shortest run found: ", shortest_run)
    print("Plotting networks")
    fig,(ax1,ax2) = plt.subplots(1,2, figsize= (10,5))
    colony.fig = fig
    colony.ax = ax2

    colony.plot_runs(ax1)
    plot_graphs(colony,ax2,fig, sim_run)

    #colony.print_retro_edge_data(num_iterations)
    #plt.show()

   
# Python 3 program to calculate Distance Between Two Points on Earth 
from math import radians, cos, sin, asin, sqrt 
def distance(lat1, lat2, lon1, lon2): 
      
    # The math module contains a function named 
    # radians which converts from degrees to radians. 
    lon1 = radians(lon1) 
    lon2 = radians(lon2) 
    lat1 = radians(lat1) 
    lat2 = radians(lat2) 
       
    # Haversine formula  
    dlon = lon2 - lon1  
    dlat = lat2 - lat1 
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
  
    c = 2 * asin(sqrt(a))  
     
    # Radius of earth in kilometers. Use 3956 for miles 
    r = 6371
       
    # calculate the result 
    return(c * r) 


def initialize_presets():
    num_ants = 4
    evap_rate = .2
    Q_const  = 1
    alpha = 1
    beta = 1
    num_iterations = 100
    size_graph = 25
    austin_graph = False


def run_command_line():
    num_ants = 10
    evap_rate = .2
    Q_const  = 1
    alpha = 1
    beta = 1
    num_iterations = 100
    size_graph = 25
    austin_graph = False
    count = 100

    print("----------------- Welcome to Command Line ACO ------------")
    print("Printing Presets: ")
    print("number of ants: ", num_ants)
    print("pheromone evaporation rate: ", evap_rate)
    print("Q: ", Q_const)
    print("alpha: ", alpha)
    print("beta: ", beta)
    print("number of iterations to run simulation: ", num_iterations)
    print("Size of graph: ", size_graph)


    #read_places()

    #build austin graph 

    stop = False

    while not stop:
        update_settings = input("Would you like to update settings? [Y/N]: ")
        
        if update_settings == "Y":
            print("Please Enter: ")
            num_ants = input("number of ants:  ")
            evap_rate = input("evaporation rate: ")
            Q_const = input("Q: ")
            alpha = input("alpha: ")
            beta = input("beta: ")
            num_iterations = input("num_iterations: ")
            size_graph = input("size_graph: ")
    
        alg(num_iterations, num_ants, evap_rate,Q_const, alpha, beta,size_graph, count)
        count +=1

        cont = input("Would you like to rerun? [Y/N]: ")
        if cont == "N":
            stop = True

def main():
    

    run_command_line()
    return

    #TODO: make inputs interactive GUI (dash or otherwise)

    #TODO: build this on Austin places data 

    #visualize austin places data 

    #make a write-up for the code 

    #build dash app


if __name__ == '__main__':
    main()

