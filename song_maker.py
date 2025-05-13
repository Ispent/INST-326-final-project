"""A template for a python script deliverable for INST326.

Driver: Brenda Ngaba
Navigator:  None (uneven # of people in discussion)
Assignment:  Exercise 4 Song Maker
Date: 2_21_25

Challenges Encountered: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import sys
import argparse

class Song:
    """ desc
    
    Attributes:
        name (str): represents the song's name.
        primary_artist (list): represents the artists that perform that song.
        bpm (int): represents the beats per minute/tempo of the song.
        chords (list): represents a list of chords that the song is comprised of.
    """
    
    def __init__(self, name, primary_artist, bpm, chords):
        self.name = name
        
        #Creating a dictionary containing the primary artist and features
        self.artists = {"primary_artist": primary_artist, "features": []}
        self.primary_artist = primary_artist
        self.bpm = bpm
        self.chords = chords
        
    def associated_artists (self, other_artists):
        """ Appends featured artists to the features key of the artist list
    
        Args:
        other_artists (str): represents featured artists.
        """
        self.other_artists = other_artists
        self.artists["features"].append(other_artists)
    
    def change_beat (self, increase=True, change=5):
        """ Changes the bpm by a specified amount
        Args:
        increase (bool): whether to increase or decrease bpm. Default value of True.
        change (int): represents the amount to change bpm by. Default value of 5.
        """
        self.increase = increase
        self.change = change
        
        
        if increase == True: #increasing bpm by change value if increase is true
            self.bpm += change
        else:
            self.bpm -= change  #decreasing bpm by change value if increase is not true
    
    def modulate(self, steps=1):
        """ Modulates the chords based on the steps. 
    
        Args:
        steps (int or float): represents the number of steps to modulate by. Default value s 1.
        """
        self.steps = steps
        
        #creating list of all notes in the chromatic scale
        chromatic_scale = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
        
        #intializing empty list to hold modulated chords 
        modulated_chords = []
             
        
        #iterating over every chord in the song to modulate
        for chord in self.chords:
            #creating a variable representing the index position of the starting chord
            starting_chord_index = chromatic_scale.index(chord)
            
            #calculating modulated index
            modulated_index = int((starting_chord_index + (steps*2))%12)
            
            #appending modulated chords to modulated chord list
            modulated_chords.append(chromatic_scale[modulated_index]) 
            self.chords = modulated_chords #setting chords attribute to updated list of modulated chords
            
    
    def info(self):
        """ Returns a string with the song's information.
        
        Returns:
            Returns the songs name, artists, chords and beats per minute
        """
        #returning the songs name, artists (including featured artists if they exist), chords and beats per minute
        if self.artists["features"]:
            return (f"{self.name} was sung by {self.primary_artist} and {self.artists['features']}.\n Other aspects of {self.name} include: \n Chords: {self.chords} \n Beats Per Minute: {self.bpm}")
        else: 
            return (f"{self.name} was sung by {self.primary_artist}. \n Other aspects of {self.name} include: \n Chords: {self.chords} \n Beats Per Minute: {self.bpm}")

if __name__ == "__main__":
    song_info = Song('Lust for Life', ['Lana del Rey'], 100, ['B', 'F#', 'A#', 'D'])
    song_info.associated_artists('The Weekend')
    song_info.change_beat(increase=False, change=10)
    song_info.modulate(2)
    print(song_info.info())