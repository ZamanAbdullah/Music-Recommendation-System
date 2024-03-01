import pickle
import pandas 
import spotipy
import streamlit as st
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = ""
CLIENT_SECRET = ""

client_credentials_manager = SpotifyClientCredentials(client_id = CLIENT_ID, client_secret = CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_song_cover_album(artist, song):
    query = f"track:{song} artist:{artist}"
    result = sp.search(q=query, type="track")

    if result and result["tracks"]["items"]:
        track = result["tracks"]["items"][0]
        album_url = track["album"]["images"][0]["url"]
        return album_url

def recommender(song):
    idx = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[idx])), reverse=True, key = lambda x:x[1])
    recom_music = []
    recom_poster = []

    for s_id in distances[1:6]:
        artist = music.iloc[s_id[0]].artist
        recom_poster.append(get_song_cover_album(artist, music.iloc[s_id[0]].song))
        recom_music.append(music.iloc[s_id[0]].song)

    return recom_music, recom_poster

st.header("Music Reommender")

music = pickle.load(open('data.pkl', "rb"))
similarity = pickle.load(open('similarity.pkl', "rb"))

music_list = music['song'].values
selected_music = st.selectbox(
    "Type or Select a Song from the Dropbox",
    music_list
)

if st.button("Show Recommendations"):
    recom_music, recom_poster = recommender(selected_music)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recom_music[0])
        st.image(recom_poster[0])
    with col2:
        st.text(recom_music[1])
        st.image(recom_poster[1])
    with col3:
        st.text(recom_music[2])
        st.image(recom_poster[2])
    with col4:
        st.text(recom_music[3])
        st.image(recom_poster[3])
    with col5:
        st.text(recom_music[4])
        st.image(recom_poster[4])



