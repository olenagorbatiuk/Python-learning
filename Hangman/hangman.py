# Write your code here
import random
words_list = ['python', 'java', 'kotlin', 'javascript']
random.seed()
word = list(random.choice(words_list))
print("H A N G M A N")
print('Type "play" to play the game, "exit" to quit:')
print()
user_choise = input()
slashed_word = ("-" *(len(word)))
attempts = 8
guess = list()
input_before = set()
alphabet = "abcdefghijklmnopqrstuvwxyz" 

if user_choise == 'play':
    while attempts > 0:
        print()
        print(slashed_word)
        if "-" not in slashed_word:  
            print("You guessed the word!")
            print("You survived!")
            break     
        letter = input("Input a letter:")
        if len(letter)>1 or len(letter)==0:
            print("You should input a single letter")
            continue
        
        if letter not in  alphabet:
            print("Please enter a lowercase English letter")
            continue
        
        if letter in guess or letter in input_before:   
            input_before.add(letter)           
            print("You've already guessed this letter")
            continue

        input_before.add(letter)            
        
        if letter in word:
            position = word.index(letter)
            slashed_word = (slashed_word[:position] + letter + slashed_word[position+1:])
            print(''.join(slashed_word))
            guess.append(letter) 
        else:
            print("That letter doesn't appear in the word")
            attempts -= 1 
        
        if attempts == 0:
            print('You lost!')
            break
else:        
    print('Type "play" to play the game, "exit" to quit:')  
   
   
    

    
        
