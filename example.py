"""Create routes between cities on a map."""
import sys
import argparse

def parse_args(args_list):
    """Takes a list of strings from the command prompt and passes them through as arguments
    
    Args:
        args_list (list) : the list of strings from the command prompt
    Returns:
        args (ArgumentParser)
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--starting_city', type=str, help='The starting city in a route.')
    parser.add_argument('--destination_city', type=str, help='The destination city in a route.')
    args = parser.parse_args(args_list)
    return args

class City:
    def __init__(self, name):
        self.name = name
        self.neighbors = {}
    
    def __repr__(self):
        return self.name
    
    def add_neighbor(self, neighbor, distance, interstate):
        if neighbor not in self.neighbors:
            self.neighbors[neighbor] = (int(distance), str(interstate))
        if self not in neighbor.neighbors:
            neighbor.neighbors[self] = (int(distance), str(interstate))

class Map:
    def __init__(self, relationships):
        self.cities = {}
        
        for city_name, neighbors in relationships.items():
            if city_name not in self.cities:
                self.cities[city_name] = City(city_name)
            
            for neighbor_name, distance, interstate in neighbors:
                if neighbor_name not in self.cities:
                    self.cities[neighbor_name] = City(neighbor_name)
                
                self.cities[city_name].add_neighbor(self.cities[neighbor_name], distance, interstate)
    
    def __repr__(self):
        return str(list(self.cities.keys()))

def bfs(graph, start, goal):
    explored = set()
    queue = [[graph.cities[start]]]
    
    while queue:
        path = queue.pop(0)
        node = path[-1]
        
        if node.name not in explored:
            for neighbor in node.neighbors:
                new_path = path + [neighbor]
                queue.append(new_path)
                
                if neighbor.name == goal:
                    return [city.name for city in new_path]
            
            explored.add(node.name)
    
    print("No path found.")
    return None

def main(start, destination, connections):
    road_map = Map(connections)
    
    if start not in road_map.cities or destination not in road_map.cities:
        return "Invalid city name."
    
    instructions = bfs(road_map, start, destination)
    
    if instructions:
        output = ""
        for i, city in enumerate(instructions):
            if i == 0:
                msg = f"Starting at {city}"
            else:
                prev_city = instructions[i - 1]
                distance, interstate = road_map.cities[prev_city].neighbors[road_map.cities[city]]
                msg = f"Then travel {distance} miles on I-{interstate} to {city}"
            
            print(msg)
            output += msg + "\n"
        return output.strip()
    else:
        return "No valid route found."
    
    
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
class City:
    def __init__(self, name):
        self.name = name
        self.neighbors = {}
    
    def __repr__(self):
        return self.name
    
    def add_neighbor(self, neighbor, distance, interstate):
        if neighbor not in self.neighbors:
            self.neighbors[neighbor] = (int(distance), str(interstate))
        if self not in neighbor.neighbors:
            neighbor.neighbors[self] = (int(distance), str(interstate))


class Map:
    def __init__(self, relationships):
        self.cities = []
        
        for city_name, neighbors in relationships.items():
            city = next((c for c in self.cities if c.name == city_name), None)
            if not city:
                city = City(city_name)
                self.cities.append(city)
            
            for neighbor_name, distance, interstate in neighbors:
                neighbor = next((c for c in self.cities if c.name == neighbor_name), None)
                if not neighbor:
                    neighbor = City(neighbor_name)
                    self.cities.append(neighbor)
                
                city.add_neighbor(neighbor, distance, interstate)
    
    def __repr__(self):
        return str(self.cities)


def bfs(graph, start, goal):
    explored = []
    queue = [[start]]
    
    while queue:
        path = queue.pop(0)
        node = path[-1]
        
        if node not in explored:
            city_obj = next((c for c in graph.cities if c.name == node), None)
            if city_obj:
                for neighbor in city_obj.neighbors:
                    new_path = list(path)
                    new_path.append(neighbor.name)
                    queue.append(new_path)
                    
                    if neighbor.name == goal:
                        return [city.name for city in new_path]
            explored.append(node)
    
    print("No path found.")
    return None


def main(start, destination, connections):
    road_map = Map(connections)
    instructions = bfs(road_map, start, destination)
    
    if instructions:
        output = ""
        for i, city in enumerate(instructions):
            if i == 0:
                msg = f"Starting at {city}"
            else:
                prev_city = instructions[i - 1]
                prev_city_obj = next(c for c in road_map.cities if c.name == prev_city)
                distance, interstate = prev_city_obj.neighbors[next(c for c in road_map.cities if c.name == city)]
                msg = f"Then travel {distance} miles on I-{interstate} to {city}"
            
            print(msg)
            output += msg + "\n"
        return output.strip()
    else:
        return "No valid route found."
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