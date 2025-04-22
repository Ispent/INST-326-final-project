"""
how do i even start this

notes:
    - only requires 1 deck to play (optional multiple decks feature)
    
    - several different possible hands and needs to compare against each other
        - some kind of hierarchy needs to be in place for every hand
            - each hand needs to be comparable to itself as well

    - possible hands
        - royal flush - (A - K - Q - J - 10) - most value hand, needs to be same suit as well
        - straight flush - (6 - 7 - 8 - 9 - 10) - second highest, needs to be same suit in numerical order
        - four of a kind - (A - A - A - A - (any card)) - four cards of the same rank
        - full house - (A - A - A - K - K) - three cards of one rank with two cards of another rank
        - flush - (2 - 5 - 9 - 10 - 3) - five cards of the same suit, any order
        - straight - (2 - 3 - 4 - 5 - 6) - five cards of numerically increasing value, any suit
        - three of a kind - yk what this is
        - two pair
        - pair
        - high card 

    - tie logic
        - highest value combo of five cards within the seven available cards will win 
            - if the main hand occurs in a tie, kickers are utilized to break ties
            - highest value of unused cards
            - if everything fails and all cards are the valued the same, the pot will be split

    - turn logic
        - within a turn, the player will have the option to
            1. fold - forfeit the hand, give up essentially
            2. check - stand your hand without any bets made
                - only available if other player hasnt bet
            3. bet - first person to money in the pot in this round
            4. call - you match the current bet placed by other player
            5. raise - you increase the current bet, a fixed amount based off the blind

    - betting logic
        - planning on limit hold 'em poker

        1. blinds (reversed ????)
            - small blind - posted by dealer
            - big blind - posted by other player
        
        2. bet size
            - small bet - used in pre-flop and flop rounds
            - big bet - used on turn and river
            - ~ 2/4 or 3/6 structure
        
        3. per round
            - in each round, there is one bet, and upto three raises
        
            pre flop - occurs right after player receives the two cards
                - small bind bets first 
                - in small bet increment
                - available actions: fold, call, raise
            
            flop - first three community cards are shown
                - dealer now goes second 
                - bet size remains at $2 

            turn - when there is four cards present 
                - big bet is possible now 

            river - final card is now dealt
                - last chance to make a bet

            ::essentially
                - round 1/2 can raise by the amount of the small blind
                - round 3/4 can raise/bet by the big blind amount

        

"""