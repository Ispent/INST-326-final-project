"""Create routes between cities on a map."""
import sys
import argparse

# Your implementation of City, Map, bfs, and main go here.
class City:
    """ A class representing a city.
    
    Attributes:
        name (str): contains the name of the citypython3 gps.py --starting_city Washington --destination_city Richmond
        neighbors (dict): empty string representing 
    """
    
    def __init__(self, name):
        """ Initializes the city class and creates an empty dictionary called neighbors.
    
        Args:
            name (str): The name of the city.
        """
        self.name = name
        self.neighbors = {}
        
    def __repr__(self):
        """ Returns the city's name
            
        Returns:
            str: the name of the city.
        """
        return self.name
    
    def add_neighbor(self, neighbor, distance, interstate):
        """ Adds neighboring cities
    
        Args:
            neighbor (City):  City object that will be connected to this instance (and vice versa).
            distance (str): the distance between two cities.
            interstate (str): the interstate number that connects  two cities.
        """
        
        #updating neighbors dictionary to add neighboring cities if its not in the neighbors dictionary
        if neighbor not in self.neighbors:
            self.neighbors.update({neighbor:(distance,interstate)})
       
        if self not in neighbor.neighbors:
            neighbor.neighbors.update({self:(distance,interstate)})
          
          
class Map:
    """ A class storing map data.
    
    Attributes:
        cities (list): list of all unique city objects that make up the graph structure.
    """
    
    def __init__(self, relationships):
        
        """ A class storing map data.
    
        Attributes:
            relationships (dict): dictionary where the keys are cities and the values are a list of tuples 
        """
        self.relationships = relationships
        self.cities = []
        
        for city_name in relationships:
            if city_name not in [c.name for c in self.cities]:
                self.cities.append(City(city_name))
    
            #finding index position of the city
            city = next(c for c in self.cities if c.name == city_name)
        
            #appending neighboring city to the cities attribute if it's not found
            for neighbor_name, distance, interstate in relationships[city_name]:
                if neighbor_name not in [c.name for c in self.cities]:
                    self.cities.append(City(neighbor_name))
            
            #finding index position of neighboring city
                neighbor = next(c for c in self.cities if c.name == neighbor_name)


                #connecting city to neighboring city using index of the city and neighboring city
                city.add_neighbor(neighbor, distance, interstate)
    
         
    def __repr__(self):
        """ Returns the string representation of the cities attribute
        Args: 
            None     
        Returns: 
            str: the string representation of the cities attribute
        """
        return  str(self.cities)

def bfs(graph, start, goal):
    """ Implementing the Breadth First Search algorithm
    
        Args:
            graph (Map):  map object representing the graph that we will be traversing
            start (str): the starting city.
            goal (str):  The destination city.
        Returns: 
            list: A list of cities we will visit on the shortest path between the start and goal cities or none if no path is found.
    """
    explored = []
    queue = [[start]]
    
    
    while queue:
        path = queue.pop(0) #deleting first element and saving it as path variable
        last_node = path[-1]    #identifying and saving last node as a variable
        
        #saving the node neighbors attribute if last_node not in explored list.
        if last_node not in explored:
            for node in graph.cities:
                if node.name == last_node:
                    node_neighbor = node.neighbors
                    
                    for neighbor in node_neighbor:
                        new_path = list(path) #converting path variables to a list
                        new_path.append(neighbor.name) #appending neighbor to new path
                        queue.append(new_path) #appending new_path to queue list

                        #returning the path list once destination is reached
                        if neighbor.name == goal: 
                            return new_path
            
        explored.append(last_node) #appending node to explored
    
    print(f"No path can be found.")
    return None
    
    
def main(start, destinations, connections):
    """ Finds and prints the shortest route between cities.
    
        Args:
            start (str): the starting city.
            destination (str): the destination city.
            connections (dict): an adjecency list of cities and the cities they connect to.
            
        Returns: 
            str: A string that contains all of the same contents that we have printed out to the console/terminal.
    """
    
    #creating an instance of the Map with connections as the argument
    road_trip = Map(connections) 
    
    instructions = bfs(road_trip, start, destinations)    
    path_string = "" #declaring empty stringd
    try:
        for index, city in enumerate(instructions):
            #identifying and printing starting city
            if index == 0:
                starting_message = f"Starting at {city}\n"
                print(starting_message)
                path_string += starting_message            
            
                #finding the next city if the destination has not been reached
            elif index < len(instructions) - 1:
                current_city = instructions[index]
                next_city = (instructions[index + 1])
                
                current_city_obj = next((c for c in road_trip.cities if c.name == current_city), None)
                neighbor_obj = next((n for n in current_city_obj.neighbors if n.name == next_city), None)
                
                if current_city_obj and neighbor_obj:
                    distance_to_drive, interstate = current_city_obj.neighbors[neighbor_obj]
                    distance_message = f"Drive {distance_to_drive} miles on {interstate} towards {next_city}, then\n"
                    print(distance_message)
                    path_string += distance_message

                            
            else: 
                destination_message = f"You will arrive at your destination"
                print(destination_message)
                path_string += destination_message
                return path_string
    except Exception as e:
        sys.exit()
    
    
def parse_args(args_list):
    """Takes a list of strings from the command prompt and passes them through as arguments
    
    Args:
        args_list (list) : the list of strings from the command prompt
    Returns:
        args (ArgumentParser)
    """

    parser = argparse.ArgumentParser()
    
    parser.add_argument('--starting_city', type = str, help = 'The starting city in a route.')
    parser.add_argument('--destination_city', type = str, help = 'The destination city in a route.')
    
    args = parser.parse_args(args_list)
    
    return args

if __name__ == "__main__":
    
    connections = {  
        "Baltimore": [("Washington", 39, "95"), ("Philadelphia", 106, "95")],
        "Washington": [("Baltimore", 39, "95"), ("Fredericksburg", 53, "95"), ("Bedford", 137, "70"), ("Philadelphia", 139, "95")], 
        "Fredericksburg": [("Washington", 53, "95"), ("Richmond", 60, "95")],
        "Richmond": [("Charlottesville", 71, "64"), ("Williamsburg", 51, "64"), ("Durham", 151, "85"), ("Fredericksburg", 60, "95"), ("Raleigh", 171, "95")],
        "Durham": [("Richmond", 151, "85"), ("Raleigh", 29, "40"), ("Greensboro", 54, "40")],
        "Raleigh": [("Durham", 29, "40"), ("Wilmington", 129, "40"), ("Richmond", 171, "95")],
        "Greensboro": [("Charlotte", 92, "85"), ("Durham", 54, "40"), ("Ashville", 173, "40")],
        "Ashville": [("Greensboro", 173, "40"), ("Charlotte", 130, "40"), ("Knoxville", 116, "40"), ("Atlanta", 208, "85")],
        "Charlotte": [("Atlanta", 245, "85"), ("Ashville", 130, "40"), ("Greensboro", 92, "85")],
        "Jacksonville": [("Atlanta", 346, "75"), ("Tallahassee", 164, "10"), ("Daytona Beach", 86, "95")],
        "Daytona Beach": [("Orlando", 56, "4"), ("Miami", 95, "268"), ("Jacksonville", 86, "95")],
        "Orlando": [("Tampa", 94, "4"), ("Daytona Beach", 56, "4")],
        "Tampa": [("Miami", 281, "75"), ("Orlando", 94, "4"), ("Atlanta", 456, "75"), ("Tallahassee", 243, "98")],
        "Atlanta": [("Charlotte", 245, "85"), ("Ashville", 208, "85"), ("Chattanooga", 118, "75"), ("Macon", 83, "75"), ("Tampa", 456, "75"), ("Jacksonville", 346, "75"), ("Tallahassee", 273, "27") ],
        "Chattanooga": [("Atlanta", 118, "75"), ("Knoxville", 112, "75"), ("Nashville", 134, "24"), ("Birmingham", 148, "59")],
        "Knoxville": [("Chattanooga", 112,"75"), ("Lexington", 172, "75"), ("Nashville", 180, "40"), ("Ashville", 116, "40")],
        "Nashville": [("Knoxville", 180, "40"), ("Chattanooga", 134, "24"), ("Birmingam", 191, "65"), ("Memphis", 212, "40"), ("Louisville", 176, "65")],
        "Louisville": [("Nashville", 176, "65"), ("Cincinnati", 100, "71"), ("Indianapolis", 114, "65"), ("St. Louis", 260, "64"), ("Lexington", 78, "64") ],
        "Cincinnati": [("Louisville", 100, "71"), ("Indianapolis", 112, "74"), ("Columbus", 107, "71"), ("Lexington", 83, "75"), ("Detroit", 263, "75")],
        "Columbus": [("Cincinnati", 107, "71"), ("Indianapolis", 176, "70"), ("Cleveland", 143, "71"), ("Pittsburgh", 185, "70")],
        "Detroit": [("Cincinnati", 263, "75"), ("Chicago", 282, "94"), ("Mississauga", 218, "401")],
        "Cleveland":[("Chicago", 344, "90"), ("Columbus", 143, "71"), ("Youngstown", 75, "80"), ("Buffalo", 194, "90")],
        "Youngstown":[("Pittsburgh", 67, "76"), ("Cleveland", 75, "80")],
        "Indianapolis": [("Columbus", 176, "70"), ("Cincinnati", 112, "74"), ("St. Louis", 242, "70"), ("Chicago", 182, "65"), ("Louisville", 114, "65"), ("Mississauga", 498, "401")],
        "Pittsburgh": [("Columbus", 185, "70"), ("Youngstown", 67, "76"), ("Philadelphia", 305, "76"), ("New York", 389, "76"), ("Bedford", 107, "76")],
        "Bedford": [("Pittsburgh", 107, "76"), ("Washington", 137, "70")], 
        "Chicago": [("Indianapolis", 182, "65"), ("St. Louis", 297, "55"), ("Milwaukee", 92, "94"), ("Detroit", 282, "94"), ("Cleveland", 344, "90")],
        "New York": [("Philadelphia", 95, "95"), ("Albany", 156, "87"), ("Scranton", 121, "80"), ("Providence", 95, "181"), ("Pittsburgh", 389, "76")],
        "Scranton": [("Syracuse", 130, "81"), ("New York", 121, "80")],
        "Philadelphia": [("Washington", 139, "95"), ("Pittsburgh", 305, "76"), ("Baltimore", 106, "95"), ("New York", 95, "95")]
    }
    
    args = parse_args(sys.argv[1:])
    main(args.starting_city, args.destination_city, connections)