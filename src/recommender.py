from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    target_valence: float
    target_danceability: float
    target_acousticness: float

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        """Stores the song catalog this recommender ranks against."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the top-k songs for the given user profile."""
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a human-readable reason why this song fits the user."""
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv

    print(f"Loading songs from {csv_path}...")

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": int(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    # Scoring logic from Phase 2 Algorithm Recipe (weight shift: energy-first).
    # Weights: genre +1.0, mood +1.0 (flat categorical bonuses),
    # energy ×2.0 linear closeness. Perfect song still caps at 4.0.
    # Reasons are collected in the same pass so explain_recommendation() can reuse them.
    W_GENRE = 1.0
    W_MOOD = 1.0
    W_ENERGY = 2.0

    score = 0.0
    reasons: List[str] = []

    # Genre — categorical, all-or-nothing (primary signal).
    if song["genre"] == user_prefs["favorite_genre"]:
        score += W_GENRE
        reasons.append(f"Matched your favorite genre ({song['genre']})")

    # Mood — categorical, all-or-nothing (secondary refinement).
    if song["mood"] == user_prefs["favorite_mood"]:
        score += W_MOOD
        reasons.append(f"mood also matched ({song['mood']})")

    # Energy — continuous, linear closeness on the 0-1 scale (partial credit).
    energy_points = W_ENERGY * (1 - abs(song["energy"] - user_prefs["target_energy"]))
    score += energy_points
    if energy_points >= 1.6:
        reasons.append("energy was a close match")

    return (score, reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, List[str]]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py

    Returns a list of (song, score, reasons) tuples sorted by score,
    highest first. `reasons` is the raw list from score_song() so the
    caller can format each reason however it likes.
    """
    # Score every song in the catalog using score_song() as the judge.
    scored = [
        (song, *score_song(user_prefs, song))  # (song, score, reasons)
        for song in songs
    ]
    # Sort by score, highest first.
    ranked = sorted(scored, key=lambda item: item[1], reverse=True)
    return [
        (song, score, reasons if reasons else ["No strong matches, but worth a listen"])
        for song, score, reasons in ranked[:k]
    ]
