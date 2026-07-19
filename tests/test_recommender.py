from src.recommender import score_song, recommend_songs, load_songs


def make_songs():
    """Two songs: a pop/happy/high-energy track and a chill lofi loop."""
    return [
        {
            "id": 1,
            "title": "Test Pop Track",
            "artist": "Test Artist",
            "genre": "pop",
            "mood": "happy",
            "energy": 0.8,
            "tempo_bpm": 120,
            "valence": 0.9,
            "danceability": 0.8,
            "acousticness": 0.2,
        },
        {
            "id": 2,
            "title": "Chill Lofi Loop",
            "artist": "Test Artist",
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.4,
            "tempo_bpm": 80,
            "valence": 0.6,
            "danceability": 0.5,
            "acousticness": 0.9,
        },
    ]


def make_user_prefs():
    return {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
        "target_valence": 0.9,
        "target_danceability": 0.8,
        "target_acousticness": 0.2,
    }


# --- score_song -------------------------------------------------------------

def test_score_song_perfect_match_caps_at_four():
    user = make_user_prefs()
    song = make_songs()[0]  # pop, happy, energy 0.8 == target 0.8

    score, reasons = score_song(user, song)

    # genre (1.0) + mood (1.0) + energy 2.0 * (1 - 0) = 4.0
    assert score == 4.0
    assert any("genre" in r for r in reasons)
    assert any("mood" in r for r in reasons)
    assert any("energy" in r for r in reasons)


def test_score_song_no_categorical_match_scores_lower():
    user = make_user_prefs()
    song = make_songs()[1]  # lofi, chill, energy 0.4

    score, reasons = score_song(user, song)

    # no genre, no mood, energy 2.0 * (1 - |0.4 - 0.8|) = 2.0 * 0.6 = 1.2
    assert score == 1.2
    assert not any("genre" in r for r in reasons)
    assert not any("mood" in r for r in reasons)
    # energy_points 1.2 < 1.6, so no energy reason is added
    assert reasons == []


def test_score_song_returns_score_and_reasons_tuple():
    score, reasons = score_song(make_user_prefs(), make_songs()[0])
    assert isinstance(score, float)
    assert isinstance(reasons, list)


# --- recommend_songs --------------------------------------------------------

def test_recommend_songs_sorted_by_score_highest_first():
    results = recommend_songs(make_user_prefs(), make_songs(), k=2)

    assert len(results) == 2
    # results are (song, score, reasons) tuples, sorted by score descending
    assert results[0][0]["genre"] == "pop"
    assert results[0][0]["mood"] == "happy"
    assert results[0][1] >= results[1][1]


def test_recommend_songs_respects_k():
    results = recommend_songs(make_user_prefs(), make_songs(), k=1)
    assert len(results) == 1
    assert results[0][0]["id"] == 1


def test_recommend_songs_fills_default_reason_when_no_matches():
    songs = make_songs()
    # user whose prefs match neither song's genre/mood and are far in energy
    user = {
        "favorite_genre": "metal",
        "favorite_mood": "angry",
        "target_energy": 0.4,
        "target_valence": 0.5,
        "target_danceability": 0.5,
        "target_acousticness": 0.5,
    }
    results = recommend_songs(user, songs, k=2)

    lofi_result = next(r for r in results if r[0]["id"] == 2)
    # lofi energy 0.4 == target 0.4 -> energy_points 2.0 (>= 1.6) so it has a reason
    assert lofi_result[2] != ["No strong matches, but worth a listen"]

    pop_result = next(r for r in results if r[0]["id"] == 1)
    # pop: no genre/mood match, energy 2.0 * (1 - 0.4) = 1.2 < 1.6 -> no reasons
    assert pop_result[2] == ["No strong matches, but worth a listen"]


# --- load_songs -------------------------------------------------------------

def test_load_songs_parses_csv(tmp_path):
    csv_path = tmp_path / "songs.csv"
    csv_path.write_text(
        "id,title,artist,genre,mood,energy,tempo_bpm,valence,danceability,acousticness\n"
        "1,Test Pop Track,Test Artist,pop,happy,0.8,120,0.9,0.8,0.2\n",
        encoding="utf-8",
    )

    songs = load_songs(str(csv_path))

    assert len(songs) == 1
    song = songs[0]
    assert song["id"] == 1
    assert isinstance(song["id"], int)
    assert song["title"] == "Test Pop Track"
    assert song["genre"] == "pop"
    assert song["energy"] == 0.8
    assert isinstance(song["energy"], float)
    assert song["tempo_bpm"] == 120
    assert isinstance(song["tempo_bpm"], int)
