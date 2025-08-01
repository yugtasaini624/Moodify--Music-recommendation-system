import pandas as pd

dfMain = pd.read_csv('music.csv')
df = dfMain.copy()
dfRes = df.drop_duplicates()

def extract_track_id(url):
    # used to get the track id
    if pd.isna(url):
        return None
    if "open.spotify.com/track/" in url:
        try:
            return url.split("/track/")[1].split("?")[0]
        except:
            return None
    return None

def getSongs(mood):
    # take all songs with given mood and drop those rows with None url
    mood_songs = dfRes[dfRes['mood'] == mood].dropna(subset=['url']).sample(6)
    songs_list = []

    # for each row in mood_songs
    for _, row in mood_songs.iterrows():
        track_id = extract_track_id(row['url'])
        if track_id:
            songs_list.append({
                'song_name': row['song_name'],
                'artist': row['artist'],
                'track_id': track_id
            })

    return songs_list[:6] 

def get_motivational_tip(mood):
    tips = {
        'happy': "Keep smiling! 😊 Spread the joy!",
        'sad': "It's okay to feel down. Better days are ahead 💙",
        'calm': "Enjoy the peace 🌿. You deserve it.",
        'focused': "You're in the zone! 🚀 Keep going!",
        'anxious': "Take a deep breath. You're doing great 🤍",
        'refreshed': "You're glowing! 🌞 Make the most of your energy."
    }
    # return mood related motivation tip
    return tips.get(mood, "Stay strong and keep moving forward! 💫")