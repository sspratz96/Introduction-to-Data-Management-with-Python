import random
import sqlite3

import pandas as pd

from faker import Faker
from datetime import date


class Wordl():
    
    def __init__(self, user_name = None, daily_mode = False, db_link = None):
       
        self.created_connection = db_link      
        self.user = user_name
        self.daily_mode = daily_mode
        
        if self.user == None:
            play_as_guest = input('Would you like to play as guest? \n[1]: Yes\n[2]: No\n > R: ')
            while play_as_guest not in ['1','2']:
                print('Please, answer accordingly with "1" or "2"')
                play_as_guest = input('Would you like to play as guest? \n[1]: Yes\n[2]: No\n > R: ')
            if play_as_guest == '1':
                self.user = 'guest'
            else:
                pass
        else:
            pass
        
        if self.created_connection != None:
            try:
                conn = sqlite3.connect(self.created_connection)
                result = self.sql(f'''SELECT * FROM wordl_users''')
            except:
                print('The chosen ddbb is not valid.')
                self.created_connection = None
    
    def sql(self, query):        
        '''
        Nicely print the result of 'query'
        '''
        # Create a connection
        conn = sqlite3.connect(self.created_connection)
        return pd.read_sql_query(query, conn)
        
    def create_db_from_scratch(self):   
        '''
        If there is no ddbb specified to read from, a new one can be created
        '''
        
        if self.created_connection == None:
            self.created_connection = 'wordl.db'
        conn = sqlite3.connect(self.created_connection)    
        # Create a cursor
        c = conn.cursor()
        # Clean tables if they exist
        c.execute('''DROP TABLE IF EXISTS wordl_track''')
        c.execute('''DROP TABLE IF EXISTS wordl_words''')
        c.execute('''DROP TABLE IF EXISTS wordl_users''')
        c.execute('''CREATE TABLE wordl_track
                     (track_id INTEGER PRIMARY KEY,
                      user_name TEXT,
                      date_of_play DATE,
                      word_of_game TEXT,
                      win_or_loose BOOL,
                      attempts INT)''')
        c.execute('''CREATE TABLE wordl_words
                     (word_id INTEGER PRIMARY KEY,
                      word TEXT)''')
        c.execute('''CREATE TABLE wordl_users
                     (user_id INTEGER PRIMARY KEY,
                      user_name TEXT)''')
        
        fk = Faker()
        list_of_words = fk.words(nb = 1000)
        words_length_5 = [i for i in list_of_words if len(i) == 5]
        
        for i in words_length_5:
            c.execute(f'''INSERT INTO wordl_words (word) VALUES ('{i}')''')
        c.execute(f'''INSERT INTO wordl_users (user_name) VALUES ('guest')''')
        conn.commit()
        conn.close()
       
    def connect_to_existing_ddbb(self, db_link):
        try:
            self.created_connection = db_link
            conn = sqlite3.connect(self.created_connection)
            result = self.sql(f'''SELECT * FROM wordl_users''')
        except:
            print('The chosen ddbb is not valid.')
            self.created_connection = None        
    
    def check_existing_users(self):
        '''
        In case you forgot what is your username, you can print those that already exist. 
        Also works to confirm that a new one is saved.
        '''
        
        if self.created_connection == None:
            print('A ddbb must be specified')
            print('You can also create a new one.')
        else:
            result = self.sql(f'''SELECT * FROM wordl_users''')
            if len(result) == 0:
                print('There are no saved users')
            else:
                print(result)
    
    def create_username(self, new_name):
        '''
        To create a new username
        ''' 
        if self.created_connection == None:
            print('A ddbb must be specified')
            print('You can also create a new one.')
        else:
            try:
                result = self.sql(f'''SELECT * FROM wordl_users WHERE user_name = '{new_name}' ''')['user_name'][0]
                print('This username already exists.')
            except Exception as E:
                conn = sqlite3.connect(self.created_connection)
                c = conn.cursor()
                c.execute(f'''INSERT INTO wordl_users (user_name) VALUES ('{new_name}') ''')
                conn.commit()
                conn.close()     
                self.user = new_name
                print('Username created. The created username was automatically chosen to play. You can play now.')
        
    def choose_username(self, user_name):
        '''
        In order to play, you must choose a username. If you did not choose a username when instancing the game, 
        you can use this command.
        '''
        if self.created_connection == None:
            print('A ddbb must be specified')
            print('You can also create a new one.')
        else:
            try:
                result = self.sql(f'''SELECT * FROM wordl_users WHERE user_name = '{user_name}' ''')['user_name'][0]
                self.user = result
                print('Valid username. You can now play.')
            except Exception as E:
                print('That user_name does not exist.')

            
################################ FUNCTIONS FOR THE GAME BELOW ################################
            
    def generate_word(self):
        words = list(self.sql('''SELECT * FROM wordl_words''')['word'])
        return random.choice(words)

    def give_feedback(self, secret_word, guess):
        feedback = []

        # Check for correct letters in correct positions (Green)
        for i in range(len(secret_word)):
            if guess[i] == secret_word[i]:
                feedback.append('Green')
            else:
                feedback.append(None)  # Placeholder for incorrect positions

        # Check for correct letters in wrong positions (Yellow)
        remaining_secret_letters = list(secret_word)  # Track remaining occurrences of each letter in the secret word

        for i in range(len(secret_word)):
            if feedback[i] is None and guess[i] in remaining_secret_letters:
                if guess[i] == secret_word[i]:
                    remaining_secret_letters.remove(guess[i])  # Remove the letter if it's correctly placed
                else:
                    feedback[i] = 'Yellow'
                    remaining_secret_letters.remove(guess[i])  # Remove the letter if it's correctly placed

        # Fill in gray for incorrect letters
        for i in range(len(secret_word)):
            if feedback[i] is None:
                feedback[i] = 'Gray'

        return feedback

    def display_feedback(self, feedback, guess):
        for letter in guess:
            print(letter, end = ' ')
        print('\n')
        for color in feedback:
            if color == 'Green':
                print('\033[92m■\033[0m', end=' ')  # Green color
            elif color == "Yellow":
                print('\033[93m■\033[0m', end=' ')  # Yellow color
            elif color == "Gray":
                print('\033[90m■\033[0m', end=' ')  # Gray color
        print('\n')
        
    def save_play(self, word_of_game, win_or_loose, attempts):
        conn = sqlite3.connect(self.created_connection)
        c = conn.cursor()
        c.execute(f'''INSERT INTO wordl_track (user_name, date_of_play, word_of_game, win_or_loose, attempts) 
                      VALUES ('{self.user}', '{str(date.today())}', '{word_of_game}', {win_or_loose}, {attempts})''')
        conn.commit()
        conn.close()             

    def structure(self):
        secret_word = self.generate_word()
        attempts = 0

        print('Welcome to the Five-Letter Word Guessing Game!')
        print('Try to guess the word.')
        print('If you want to exit the game, tipe wordl_out.')

        while True:
            guess = input('Enter your guess: ').lower()
            
            if guess == 'wordl_out':
                exit = input('You really want to log out? Game will not be saved. \n[1] = Yes\n[2] = No\n > R: ')
                while exit not in ['1','2']:
                    print('Please, choose between 1 or 2')
                    exit = input('You really want to log out? Game will not be saved. \n[1] = Yes\n[2] = No\n > R: ')
                if exit == '1':
                    break
                    
            elif len(guess) != 5 or not guess.isalpha():
                print('Please enter a valid five-letter word.')
                continue
            
            else:
                attempts += 1
                feedback = self.give_feedback(secret_word, guess)

                self.display_feedback(feedback, guess)

                if feedback == ['Green'] * 5:
                    print(f"Congratulations! You guessed the word '{secret_word}' in {attempts} attempts.")
                    self.save_play(win_or_loose = True, word_of_game = secret_word, attempts = attempts)
                    break

                if attempts > 4:
                    print('You have ran out of attempts...')
                    print(f'The word was : {secret_word}')
                    self.save_play(win_or_loose = False, word_of_game = secret_word, attempts = attempts)
                    break

                
################################ FUNCTION OF THE GAME BELOW ################################                
                
    def play(self):
        if self.created_connection == None:
            print('You must specify a ddbb link. You can also create a new one.')
        else:
            if self.user == None:
                print('You must create or choose a user_name first.')
            else:
                try:
                    result = self.sql(f'''SELECT * FROM wordl_users WHERE user_name = '{self.user}' ''')['user_name'][0]
                    if self.daily_mode == True:
                        try:
                            result = self.sql(f'''SELECT * FROM wordl_track 
                                             WHERE user_name = '{self.user}' 
                                             AND date_of_play = '{str(date.today())}' ''')['user_name'][0]
                            print('Sorry, you have played today already.')
                            user_can_play = False
                        except:
                            user_can_play = True
                    else:
                        user_can_play = True

                    if user_can_play == True:
                        self.structure()
                except:
                    print('The specified username does not exist. Create it, or choose one that already exists.')

    def print_track(self):
        print(self.sql('''SELECT * FROM wordl_track'''))
