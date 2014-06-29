def main():
    """Sum the names of the digits from one to one thousand. Exclude spaces and hyphens.
    Use the British "one hundred and one" convention for numbers between 100 and 1000.
    """

    digits = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    teens = ['ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen']
    decades = ['twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']

    # Sum up the first two decades
    allDigits = sum([len(x) for x in digits])
    first99 =  allDigits + sum([len(x) for x in teens])

    # Add remaining decades < 100 to first99. This is be reused later.
    for decade in decades:
        first99 = first99 + len(decade)*10 + allDigits

    # All numbers in the 100s except the first (100, 200, etc.) share the same suffix, "hundred and <something>"
    # Once computed, adding 100 lengths of the leading number to that base gives the correct length
    # for that 100s segment
    hundredLength = len('hundred')*100 + len('and')*99 + first99
    total = first99
    for digit in digits:
        total = total + len(digit)*100 + hundredLength

    # Add in the final "one thousand" and the total is complete
    total = total + len('one') + len('thousand')
    print 'Sum of the lengths of number names from 1 to 1000:', total

if __name__ == "__main__":
    main()
