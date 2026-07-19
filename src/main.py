"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")

    print(f"Loaded songs: {len(songs)}")

    # Starter example profile. Keys must match what score_song() reads.
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print_recommendations(recommendations)


def print_recommendations(recommendations) -> None:
    """Render recommendations as a clean, readable terminal layout."""
    width = 60

    print()
    print("=" * width)
    print("  TOP RECOMMENDATIONS".ljust(width))
    print("=" * width)

    for rank, (song, score, reasons) in enumerate(recommendations, start=1):
        print()
        print(f"  {rank}. {song['title']}  —  {song['artist']}")
        print(f"     Score: {score:.2f}")
        print("     Reasons:")
        for reason in reasons:
            print(f"       • {reason}")

    print()
    print("=" * width)


if __name__ == "__main__":
    main()
