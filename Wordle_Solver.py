import random

def main():
    answer = ''
    print('\nDIRECTIONS: If giving manual feedback for a guess, use the form RRGYR where R denotes a gray square, \nY denotes a yellow square, and G denotes a green square on the Wordle board\n')
    manual = input("ENTER 1 if you want to enter the answer and have the AI run from there \nENTER 2 if you want to respond to each AI guess manually \nENTER 3 if you want a suggestion for your next guess\n")
    if manual == '1': 
        answer = input("Type your 5-letter answer word: ").strip().upper()
        answer = str(answer)
    word_list, frequency_dict = make_word_list("words.txt")
    #guess = "SLATE"
    if manual == '1' or manual == '2':
        guess = get_first_guess(word_list, frequency_dict)
    else:
       guess = input("What was your first guess?").strip().upper() 
       help_needed = True
    turn = 1
    if manual != '3': print("AI Guess {}:".format(turn), guess)
    if manual == '2' or manual == '3': colors = input("How accurate is this guess?").strip().upper()
    else: colors = get_colors(guess, answer)
    guess_dict = {guess[x]+str(x):colors[x] for x in range(5)}
    while colors != "GGGGG" and turn <=6:
        print("guess: ", guess)
        guess, word_list = get_best_guess(guess_dict, word_list, frequency_dict, guess)
        frequency_dict = get_frequencies(word_list)
        if manual == '3': manual_guess = input("What was your next guess? (Type N/A if you want the AI to provide your next guess): \n").strip().upper()
        if manual != '3' or manual_guess == 'N/A':
            print("AI Guess {}:". format(turn+1), guess)
        else:
            guess = manual_guess
        if manual == '2' or manual == '3': colors = input("How accurate is this guess?").strip().upper()
        else: colors = get_colors(guess, answer)
        guess_dict = {guess[x]+str(x):colors[x] for x in range(5)}
        turn += 1
    if colors == "GGGGG": print("AI guessed the Wordle in {}/6 guesses!".format(turn))
    else: print("AI failed to guess the Wordle in 6 tries :(")

def get_frequencies(word_list):
    frequencyDict = {}
    for word in word_list:
        for index, character in enumerate(word):
                if (index, character) not in frequencyDict: frequencyDict[(index, character)] = 0
                frequencyDict[(index, character)]+=1
    return frequencyDict

def get_colors(guess, answer):
    colors = ''
    for index, char in enumerate(guess):
        if char == answer[index]: colors = colors + "G"
        elif char in answer: colors = colors + "Y"
        else: colors = colors + "R"
    return colors

def make_word_list(filename):
    wl = []
    frequencyDict = {}
    infile = open(filename)
    for word in infile.readlines():
        word = word.upper().strip()
        wl.append(word)
        for index, character in enumerate(word):
            if (index, character) not in frequencyDict: frequencyDict[(index, character)] = 0
            frequencyDict[(index, character)]+=1
    return wl, frequencyDict

def get_first_guess(word_list, frequency_dict):
    scores = []
    for word in word_list:
        scores.append((rate(word, frequency_dict), word))
    scores = sorted(scores, reverse=True)
    best_score = scores[0][0]
    best_possible = [x for x in scores if x[0] == best_score]
    return random.choice(best_possible)[1]

def get_best_guess(guess_dict, word_list, frequency_dict, guess):
    print("guess: ", guess, "guess_dict: ", guess_dict)
    possible = []
    alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P', 'Q','R','S','T','U','V','W','X','Y','Z']
    spot_info = {0:alphabet[:], 1:alphabet[:], 2:alphabet[:], 3:alphabet[:], 4:alphabet[:]}
    scores = []
    ind = 0
    for key in guess_dict:
        letter = key[0]
        if guess_dict[key] == 'G': spot_info[ind] = [letter]
        if guess_dict[key] == 'R': 
            for x in range(5):
                if letter in spot_info[x] and len(spot_info[x]) > 1: spot_info[x].remove(letter)
        if guess_dict[key] == 'Y': 
            if letter in spot_info[ind]: spot_info[ind].remove(letter)
        ind+=1
    for word in word_list:
        if isValid(word, spot_info, guess, guess_dict): possible.append(word)
    for word in possible:
        scores.append((rate(word, frequency_dict), word))
    scores = sorted(scores, reverse=True)
    best_score = scores[0][0]
    best_possible = [x for x in scores if x[0] == best_score]
    return random.choice(best_possible)[1], possible

def rate(word, frequency_dict):
    score = 0
    seen = []
    for x in range(5):
        if word[x] not in seen: score += frequency_dict[(x, word[x])]
        seen.append(word[x])
    return score

    #return best guess and updated word list with only possible options remaining
def isValid(word, spot_info, guess, guess_dict):
    for index, char in enumerate(word):
        if char not in spot_info[index]: return False
    for key in guess_dict:
        if guess_dict[key] == 'Y' and key[0] not in word: 
            return False
    return True

if __name__ == '__main__': main()