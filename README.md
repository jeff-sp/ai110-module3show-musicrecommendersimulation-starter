# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Real-world recommendation systems compare each item's characteristics to a user's preferences by measuring similarity across multiple features, then rank the highest-scoring results. My version will prioritize the features that best represent musical taste: genre, mood, energy, and acousticness. Continuous features such as energy and acousticness will use a closeness score (1 - abs(distance)) so songs closer to the user's preferred values receive higher scores, while categorical features like genre and mood provide bonus points for exact matches. After each song is scored independently, the recommendations are ranked from highest to lowest score allowing the system to recommend the top matches while keeping the scoring and ranking logic separate for flexibility and maintainability.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
  - The `Song` dataclass stores 10 fields, but the system scores on four core features: genre and mood (categorical), and energy and acousticness (continuous 0–1). tempo_bpm, valence, and danceability are stored but held back from v1 scoring (tempo needs min-max scaling; the other two are optional smoothing axes). id, title, and artist are identity/display only — never scored.
- What information does your `UserProfile` store
  - Four preference fields: favorite_genre and favorite_mood (categorical targets for exact-match bonuses), target_energy (the value energy closeness is measured against), and likes_acoustic (a boolean that maps onto the acousticness axis).
- How does your `Recommender` compute a score for each song
  - Each song is scored independently against the profile:
    - Continuous features use closeness: 1 - abs(song.energy - user.target_energy), so smaller distance → higher score (a perfect match = 1.0). Same form for acousticness.
    - Categorical features add an all-or-nothing bonus: +bonus if song.genre == user.favorite_genre (likewise mood).
    - Total = averaged/summed closeness scores + categorical bonuses. This lives in the Scoring Rule (score_song), which knows only about one song.
- How do you choose which songs to recommend
  - The Ranking Rule (recommend / recommend_songs) is separate: it scores every song, sorts descending by score, and returns the top k. Keeping scoring (a per-song number) apart from ranking (the sort-and-cut policy) lets you change the math or the display policy independently.

You can include a simple diagram or bullet list if helpful.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



