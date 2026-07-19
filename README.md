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

# Phase 2 — Algorithm Recipe: Scoring Logic

This document is the **design** for how `score_song()` ranks songs against a
user's preferences. It is intentionally code-free — it is the recipe the
implementation should follow.

## Design stance: genre-first

This recommender is designed as a **genre-first** tool. Genre is the coarsest,
most identity-defining filter of taste: a listener who asks for `rock` and is
handed `classical` experiences a hard miss, no matter how well the mood lines
up. The primary job is to get the *category* right; mood is a secondary
refinement that fine-tunes within the desired genre.

Consequence: **genre is weighted above mood.** This system might over-prioritize genre, ignoring great songs that match the user's mood

## The two kinds of fields

| Field type   | Fields                                              | Nature                        | Scoring approach            |
|--------------|-----------------------------------------------------|-------------------------------|-----------------------------|
| Categorical  | `genre`, `mood`                                     | Exact match or no match       | Flat bonus (all-or-nothing) |
| Continuous   | `energy`, `valence`, `danceability`, `acousticness` | 0.0–1.0 scale, closeness matters | Distance-based (partial credit) |

Categorical fields can only match or miss, so they earn a fixed bonus.
Continuous fields live on a 0–1 scale, so "close" should earn partial credit.

## Point weighting

| Signal            | Weight | Max contribution | Rationale                                              |
|-------------------|--------|------------------|--------------------------------------------------------|
| **Genre match**   | +2.0   | 2.0              | Primary signal — the category that defines taste       |
| **Mood match**    | +1.0   | 1.0              | Secondary refinement within the desired genre          |
| **Energy closeness** | ×1.0 | 1.0             | Meaningful, but should not outvote the genre match     |

A "perfect" song therefore caps at **4.0 points**, with genre as the dominant lever.

### Why these numbers

- Genre at 2× mood encodes the genre-first stance directly in the math: getting
  the category right is worth twice getting the mood right.
- Energy is capped at 1.0 so that even a flawless energy match cannot, on its
  own, outrank a genre match. Energy fine-tunes; it does not decide.

## Similarity math for continuous fields

Because energy is already on a 0–1 scale, use **linear closeness** rather than
raw distance:

```
energy_points = W_energy * (1 - abs(song.energy - user.target_energy))
```

- Identical energy → `1 - 0 = 1.0` → full points
- Opposite extremes (0.0 vs 1.0) → `1 - 1 = 0.0` → nothing
- Always bounded to [0, 1], so it composes cleanly with the flat bonuses.

## Scope decisions for v1

1. **Energy only, for now.** `UserProfile` also carries targets for `valence`,
   `danceability`, and `acousticness`. v1 scores **energy only** to keep the
   logic simple and the explanations readable. Once scoring + explanations work,
   the same closeness formula can be extended to the other three continuous
   fields (suggested weight ×0.5 each) for a richer signal.

2. **Collect reasons while scoring.** `score_song()` returns `(score, reasons)`.
   Build the `reasons` list *in the same pass* that computes the score, so
   `explain_recommendation()` can reuse it — e.g. "Matched your favorite genre
   (lofi); mood also matched (chill); energy was a close match." Do not score and
   explain in two separate passes.

## Worked example

User wants: genre `lofi`, mood `chill`, target energy `0.40`.

Song #2 "Midnight Coding" (lofi, chill, energy 0.42):

| Signal  | Match?              | Points                        |
|---------|---------------------|-------------------------------|
| Genre   | lofi == lofi ✓      | +2.0                          |
| Mood    | chill == chill ✓    | +1.0                          |
| Energy  | 1 - |0.42 - 0.40|   | +0.98                         |
| **Total** |                   | **3.98** (near-perfect)       |

Song #6 "Spacewalk Thoughts" (ambient, chill, energy 0.28):

| Signal  | Match?              | Points                        |
|---------|---------------------|-------------------------------|
| Genre   | ambient != lofi ✗   | +0.0                          |
| Mood    | chill == chill ✓    | +1.0                          |
| Energy  | 1 - |0.28 - 0.40|   | +0.88                         |
| **Total** |                   | **1.88**                      |

The genre-first stance is visible here: the ambient track scores much lower
because it misses the genre, even though it nails the mood and energy.


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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
$ python3 src/main.py
Loading songs from data/songs.csv...
Loaded songs: 18

============================================================
  TOP RECOMMENDATIONS                                       
============================================================

  1. Sunrise City  —  Neon Echo
     Score: 3.98
     Reasons:
       • Matched your favorite genre (pop)
       • mood also matched (happy)
       • energy was a close match

  2. Gym Hero  —  Max Pulse
     Score: 2.87
     Reasons:
       • Matched your favorite genre (pop)
       • energy was a close match

  3. Rooftop Lights  —  Indigo Parade
     Score: 1.96
     Reasons:
       • mood also matched (happy)
       • energy was a close match

  4. Night Drive Loop  —  Neon Echo
     Score: 0.95
     Reasons:
       • energy was a close match

  5. Concrete Verses  —  MC Grayline
     Score: 0.92
     Reasons:
       • energy was a close match

============================================================
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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



