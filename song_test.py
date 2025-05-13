import sys
import argparse

class Song:
    """ Represents a song with attributes like name, artists, bpm, and chords.
    
    Attributes:
        name (str): Represents the song's name.
        primary_artists (list): Represents the artists that perform that song.
        bpm (int): Represents the beats per minute/tempo of the song.
        chords (list): Represents a list of chords that the song is comprised of.
    """
    
    def __init__(self, name, primary_artists, bpm, chords):
        """ Initializes the Song object with given attributes. """
        self.name = name
        self.primary_artists = primary_artists
        self.artists = {"primary_artists": primary_artists, "features": []}
        self.bpm = bpm
        self.chords = chords
        
    def associated_artists(self, other_artists):
        """ Appends featured artists to the features key of the artist list. 
        
        Args:
        other_artists (str): The name of the featured artist.
        """
        self.artists["features"].append(other_artists)
    
    def change_beat(self, increase=True, change=5):
        """ Changes the bpm by the given amount. 
        
        Args:
        increase (bool): Whether to increase or decrease bpm. Default is True.
        change (int): Amount to increase or decrease bpm. Default is 5.
        """
        if increase:
            self.bpm += change
        else:
            self.bpm -= change
    
    def modulate(self, steps=1):
        """ Modulates the chords based on the given steps. 
        
        Args:
        steps (int or float): The number of steps to modulate by. Default is 1.
        """
        chromatic_scale = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
        
        modulated_chords = []
        
        for chord in self.chords:
            # Finding the starting index of the chord in the chromatic scale
            starting_chord_index = chromatic_scale.index(chord)
            
            # Calculating the modulated index with steps (each step is 2 half-steps)
            modulated_index = (starting_chord_index + int(steps * 2)) % 12
            modulated_chords.append(chromatic_scale[modulated_index])
        
        # Updating the chords with the modulated ones
        self.chords = modulated_chords
    
    def info(self):
        """ Returns a string with information about the song. """
        
       #returning the songs name, artists (including featured artists if they exist), chords and beats per minute
        if self.artists["features"]:
            return (f"{self.name} was sung by {self.primary_artists} and {self.artists['features']}.\n Other aspects of {self.name} include: \n Chords: {self.chords} \n Beats Per Minute: {self.bpm}")
        else: 
            return (f"{self.name} was sung by {self.primary_artists}. \n Other aspects of {self.name} include: \n Chords: {self.chords} \n Beats Per Minute: {self.bpm}")


if __name__ == "__main__":
    # Example usage:
    song_info = Song("Indie Vibes", ["Faye Webster", "Cigarettes After Sex"], 120, ["C", "G", "D", "F"])
    
    print(song_info.info())  # Print the song info
    
    song_info.associated_artists("Phoebe Bridgers")  # Add an associated artist
    print("\nAfter adding an associated artist:")
    print(song_info.info())

    song_info.change_beat(increase=False, change=10)  # Decrease BPM
    print("\nAfter changing the beat:")
    print(song_info.info())

    song_info.modulate(1)  # Modulate chords by 1 step
    print("\nAfter modulating the chords:")
    print(song_info.info())
