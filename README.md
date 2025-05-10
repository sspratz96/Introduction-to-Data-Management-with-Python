# 🟩 Wordl – A Five-Letter Word Guessing Game in Python

Wordl is a Python-based terminal game inspired by Wordle, allowing players to guess a random 5-letter word with visual feedback for each attempt. The game supports user accounts, game tracking with SQLite, and optional daily challenge mode.

## 🎮 Features

- Random 5-letter word generation using the Faker library.
- Terminal-based colored feedback (Green, Yellow, Gray) for letter accuracy.
- SQLite integration to track:
  - Players and their usernames
  - Play history (date, attempts, outcome)
- Guest and registered user support
- Daily mode option (play only once per day)

---

## 📦 Requirements

Install required libraries before playing:

```bash
pip install pandas faker
```

---

## 🛠 Setup

### 1. Clone or download the repository:

```bash
git clone https://github.com/yourusername/wordl-game.git
cd wordl-game
```

### 2. Create a new game database (optional):

If no database is provided, you can create one from scratch:

```python
from your_module_name import Wordl

game = Wordl()
game.create_db_from_scratch()
```

---

## 🚀 How to Play

### 1. Initialize a game session

```python
game = Wordl(db_link="wordl.db", user_name="your_username", daily_mode=False)
```

Or, you can be prompted interactively if no username is passed.

### 2. Register or select a user

```python
game.create_username("new_user")
game.choose_username("existing_user")
```

### 3. Start the game

```python
game.play()
```

### 4. View play history

```python
game.print_track()
```

---

## 🧠 Gameplay Rules

- You have **5 attempts** to guess the correct 5-letter word.
- Feedback per guess:
  - 🟩 Green: Correct letter in the correct position
  - 🟨 Yellow: Correct letter in the wrong position
  - ⬜ Gray: Incorrect letter
- Type `wordl_out` during the game to exit (unsaved).

---

## 🗂 Database Structure

Three tables are created:

- `wordl_users`: Stores player usernames
- `wordl_words`: Stores randomly generated 5-letter words
- `wordl_track`: Stores gameplay history per user

---

## 🧪 Example

```python
game = Wordl()
game.create_db_from_scratch()
game.create_username("alice")
game.play()
```

---

## ❓ FAQ

**Q:** How is the word list generated?  
**A:** Using `Faker.words(nb=1000)`, filtered to only include 5-letter words.

**Q:** What happens if I try to play twice in daily mode?  
**A:** You will be blocked from replaying until the next day.

---

## 📄 License

MIT License
