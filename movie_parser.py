"""Parses movie scripts to extract scenes, actions, and dialogues"""
import re
import argparse
import sys
import os

class Scene:
    """Stores the data related to individual scenes.
    
    Attributes:
        scene_number (int): An integer representing the scene number in the script.
        scene_heading (str): The scene heading represented as a string.
        action (list): A list of strings representing action descriptions in the scene.
        dialogues (list): A list of dictionaries, each containing 'character' and 'speech' keys representing character dialogues.
        unique_characters (int): An integer representing the number of unique characters in the scene.
        dialogue_count (int): An integer representing number of times characters speak in the scene 
        estimated_duration (int): An integer representing the estimated length of time of the scene in seconds.
    """
    
    def __init__(self, scene_heading, action, dialogues, scene_number):
        """ Initializes the Scene object with provided attributes and calculates additional metrics.

        Args:
            scene_heading (str): See class documentation.
            action (list): See class documentation.
            dialogues (list): See class documentation.
            scene_number (int): See class documentation.
        """
        self.scene_heading = scene_heading
        self.action = action
        self.dialogues = dialogues
        self.scene_number = scene_number
            
        #Calculating total number of dialogues and unique characters
        self.dialogue_count = len(dialogues)
        self.unique_characters = len(set(d['Character'] for d in dialogues))
        
        #Counting  number of actions and calculating duration of the scene
        self.number_of_actions = len(action) 
        self.estimated_duration = (self.dialogue_count * 3) + (self.number_of_actions * 2)

    def __repr__(self):
        """ Returns formatted string representation of the scene.
            
        Returns:
            str: The scene number and heading
        """
        return f"Scene {self.scene_number}: {self.scene_heading}" 
        
    def print_info(self):
        """Prints a summary of the scene details."""
        print(f"Scene {self.scene_number}: {self.scene_heading} \n Unique Characters: {self.unique_characters} \n Dialogue Count: {self.dialogue_count} \n Estimated Duration: {self.estimated_duration} seconds")
        
class Script:
    """Represents a movie script containing multiple scenes.

    Attributes:
        name (str):  A string representing the name of the script
        scenes (list): List of Scene objects where each object corresponds to one scene in the script.
    """
    def __init__(self, path):
        """ Initializes Script object

        Args:
            path (str): The path to the script file that will be read.
        """
        self.scenes = []
        self.name = None
        
        #Opening and reading file
        with open(path, 'r') as f:
            content = f.read()
        
      
        for line in content.splitlines():
            stripped_line = line.strip() #Line without white spaced
            
              #Parsing script name from script
            if stripped_line and not re.match(r"^(INT\.|EXT\.)", stripped_line):
                self.name = stripped_line
                break
        
        if not self.name: #Using filename if no script name is found
            self.name = os.path.basename(path)
                
        self.parse_script(content)
                
    def parse_script(self, script):
        """ Parses the script and populates the scenes attribute.
    
        Args:
            script (str):  The entire content of the script file as a string.
        """
        
        #Initializing variables
        scene_number = 0
        scene_heading = None
        actions = []
        dialogues = []
        current_character = None
        new_dialogue = False
           
        #Iterating through each line of the script 
        for line in script.splitlines():
            stripped_line = line.strip() 
                
            if not stripped_line:
                current_character = None
                continue
                
            #Identifying scene headings
            if re.match(r"^(INT\.|EXT\.)", stripped_line):
                if scene_number > 0:
                    scene = Scene(scene_heading, actions, dialogues, scene_number)
                    self.scenes.append(scene)
                        
                scene_number += 1 #Increasing scene_number by 1 for each scene identified
                
                #Resetting actions and dialogues for each new scene
                scene_heading = stripped_line
                actions, dialogues = [], []
                current_character = None
                new_dialogue = False
                continue
              
                #Parsing character names to indicate the start of dialogue
            elif re.match(r'^\s+([A-Z][A-Z\s]*?(?:\s*\([A-Z\.]+\))?)$', line):
                current_character = stripped_line    
                continue
                
                #Parsing dialogue lines and appending to dictionary
            elif current_character and re.match(r'^\s+(?![A-Z\s]+(?:\([A-Z\.]+\))?$)\S.*$', line):
                dialogue = stripped_line
                dialogues.append({'Character': current_character, 'Speech': dialogue})
                new_dialogue = True
                continue
            
                 #Parsing action
            elif not new_dialogue and re.match(r'^(?!INT\.|EXT\.|CUT TO:|FADE OUT\.)(?![A-Z\s]+$)\S.*$', stripped_line):
                actions.append(stripped_line)
                continue
          
        if scene_heading:
            scene = Scene(scene_heading, actions, dialogues, scene_number)
            self.scenes.append(scene)
            
    def __repr__(self):
        return f"Name: {self.name} | Scenes: {len(self.scenes)}"
    
def main(path):
    """ Parses all scripts in the folder path and prints their information
    Args:
        path (str): A string that represents the path of the folder with the scripts that will be parsed.
    Returns:
       screenplays (list): The list of Script instances created.
    """
    screenplays = []
    
    #Iterating through files in specified path
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
         
        #Creating an instance of script if a file exists in the path
        if os.path.isfile(file_path):
            script = Script(file_path)
            screenplays.append(script)
    
        
        #Printing each script
    for script in screenplays:
        print(script)
        for scene in script.scenes: #Printing parsed info for each script
            scene.print_info()
                
    return screenplays

def parse_args(args_list):
    """ Parse command-line arguments.
    Args:
        args_list (list of str): list of arguments from the command line.

    Returns:
        Namespace: the parsed arguments, as returned by argparse.ArgumentParser.parse_args().
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="The path to the folder containing the script files (as a str)")
    return parser.parse_args(args_list)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args.path)


