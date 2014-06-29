def getValues(hand):
    """Pull the values out of the hand.

    :param hand: list of 5 lists of value, suit pairs
    :return: list of 5 ints
    """
    return sorted([c[0] for c in hand])

def getSuits(hand):
    """Pull the suits out of the hand

    :param hand: list of 5 lists of value, suit pairs
    :return: list of 5 character literals
    """
    return sorted([c[1] for c in  hand])

def sameValue(handValues):
    """Return list of lists of count, value pairs. [1, 3, 3, 5, 5] -> [[1,1], [2,3], [2,5]]

    :param handValues: list of 5 int
    :return: list of lists of int pairs
    """
    return [[handValues.count(x),x] for x in set(handValues)]

def sameValueCount(handValues):
    """Reduces return of sameValue to just the counts of values, not their values

    :param handValues: list of 5 int
    :return: list of ints
    """
    return [v[0] for v in sameValue(handValues)]

def highCard(handValues):
    """Returns the high value in the hand

    :param handValues: list of 5 ints
    :return: int
    """
    return handValues[4]

def cardGroups(handValues, groupSize):
    """Return the number of groupSize groups in hand

    :param handValues: list of 5 ints
    :param groupSize: int
    :return: number of groups of cards (same value) of size groupSize in hand
    """
    return [x[0] for x in sameValue(handValues)].count(groupSize)

def hasOnePair(handValues):
    """Returns True if there is at least one pair in the hand

    :param handValues: list of 5 ints
    :return: boolean
    """
    return cardGroups(handValues,2) > 0

def hasTwoPair(handValues):
    """Returns True if there are two pair in the hand

    :param handValues: list of 5 ints
    :return: boolean
    """
    return cardGroups(handValues,2) > 1

def hasThreeOfAKind(handValues):
    """Return True if there are three of a kind in the hand

    :param handValues: list of 5 ints
    :return: boolean
    """
    return cardGroups(handValues,3) > 0

def isStraight(handValues):
    """Return True if the 5 cards in the hand are consecutive

    :param handValues: list of 5 ints
    :return: boolean
    """
    return handValues == range(handValues[0],handValues[0]+5)

def isFlush(handSuits):
    """Return True if all cards have the same suit

    :param handSuits: list of 5 character literals
    :return: boolean
    """
    return [handSuits.count(x) for x in set(handSuits)][0] == 5

def isFullHouse(handValues):
    """Return True if there are 2 of one value card and 3 of another

    :param handValues: list of 5 ints
    :return: boolean
    """
    return sameValueCount(handValues) == [2, 3]

def hasFourOfAKind(handValues):
    """Returns True if there are four of a kind in the hand

    :param handValues: list of 5 ints
    :return: boolean
    """
    return 4 in sameValueCount(handValues)

def isStraightFlush(handValues, handSuits):
    """Return True if the hand is a straight flush, i.e., 5 consecutive values all of the same suit

    :param handValues: list of 5 ints
    :param handSuits: list of 5 character literals
    :return: boolean
    """
    return isStraight(handValues) and isFlush(handSuits)

def isRoyalFlush(handValues, handSuits):
    """Returns True if the hand holds a straight flush with the Ace as the high card

    :param handValues: list of 5 ints
    :param handSuits: list of 5 character literals
    :return: boolean
    """
    return isStraightFlush(handValues,handSuits) and highCard(handValues) == 14

def getHands(fileName):
    """Read in list of hands from fileName. The file format is 10 pairs of alphanumerics per line.
    The first 5 pairs go to player 1, and the second 5 to player 2. The cards are encoded with the first
    character being either a number from 2 to 9 or one of the letters TJQKA (Ten, Jack, Queen, King, Ace).
    The second character is one of CDHS (Clubs, Diamonds, Hearts, Spades). The lines are stored as a large list
    consisting of a list of two hands, each of which is a list of 5 lists, one for each card, holding a value
    from 2 to 14 (2 to Ace) and a suit letter ('C', 'D', 'H', and 'S').

    :param fileName: string containing the name of the file containing the hands.
    :return:list of lists of hands
    """
    allHands = []
    values = {'2':2,'3':3, '4':4, '5':5, '6':6, '7':7,'8':8,'9':9,'T':10,'J':11,'Q':12,'K':13,'A':14}
    for line in open(fileName):
        # Translate the value characters to ints; just record the suit
        bothHands = [[values[c[0]], c[1]] for c in line.split()]
        player1 = bothHands[:5]
        player2 = bothHands[5:]
        allHands.append([player1, player2])
    return allHands

def evaluateHand(hand):
    """Return the rank of the hand. This consists of a value for each of the major hand types, and any additional
    values needed in case of a tie (both hands of the same type).

    :param hand: list of 5 ints
    :return: list of ints encoding the strength of the hand
    """

    # Separate out the list of card values and suits, as they are used frequently below
    handValues = getValues(hand)
    handSuits = getSuits(hand)
    # Determine the tie-breaking breakdown of card values
    breakdown = [x[1] for x in sorted(sameValue(handValues), None, None, True)]

    # Evaluate from highest hand to lowest. This avoids confusion between a full house and three of a kind
    # since the full house will be evaluated first
    if isRoyalFlush(handValues,handSuits):
        return [10]
    if isStraightFlush(handValues,handSuits):
        return [9, highCard(handValues)]
    if hasFourOfAKind(handValues):
        return [8] + breakdown
    if isFullHouse(handValues):
        return [7] + breakdown
    if isFlush(handSuits):
        return [6, highCard(handValues)]
    if isStraight(handValues):
        return [5, highCard(handValues)]
    if hasThreeOfAKind(handValues):
        return [3] + breakdown
    if hasTwoPair(handValues):
        return [2] + breakdown
    if hasOnePair(handValues):
        return [1] + breakdown
    return [0] + breakdown

def whoWins(hands):
    """Compare the rankings of the two hands and return a winner pair with 1 set in the winning position.

    :param hands:list of two lists of 5 cards, each a value/suit pair
    :return:list of 2 ints
    """
    player1, player2 = hands
    eval1 = evaluateHand(player1)
    eval2 = evaluateHand(player2)
    if eval1 > eval2:
        return [1, 0]
    if eval2 > eval1:
        return [0, 1]
    return [0, 0]

def main():
    """Read in the hands to a master list. Iterate through the list, evaluating the winner of each hand.
    Keep a running total of games won by player 1, and print that number at the end of the run.
    """
    handList = getHands('poker.txt')
    player1Wins = 0
    for hands in handList:
        player1Wins = player1Wins + whoWins(hands)[0]
    print player1Wins, "hands won by player 1"

if __name__ == "__main__":
    main()
