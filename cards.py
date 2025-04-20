class Card:
  """ Creates a card object that will hold the values of the card

  args:
    suit(str): holds what suit the card is
    value(str): holds what value the card has
  """
  def __init__(self, suit, value):
    self.suit = suit
    self.value = value

  def get_value(self):
    """ performs conversion of the value attribute of the card into their point value
    
    args:
      values(dict): dictionary holding each possible value and their point equiavalence
      
    returns:
      returns the point value of the card's value
    """
    # note that for games where Ace can be one or 11 this is wack
    values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
                  '8': 8, '9': 9, '10': 10, 'Jack': 10, 'Queen': 10,
                  'King': 10, 'Ace': 11}
    return values[self.value]
  
  def __str__(self):
    # returns readable string representation of a card
    return f"{self.value} of {self.suit}"
  
  