import streamlit as st
import requests

# on VPN to work

    
st.write('# Hello World')
player_tag = st.text_input('Enter player tag without #')

API_KEY = ''

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json"
}

response = None
    
    
    
if len(player_tag)>1 and player_tag.startswith('#') :
    
    request_url = f"https://api.brawlstars.com/v1/players/{player_tag}"
    response = requests.get(request_url, headers=headers)

elif len(player_tag)>0 and player_tag.startswith('#') == False:
    
    request_url = f"https://api.brawlstars.com/v1/players/%23{player_tag}"
    response = requests.get(request_url, headers=headers)
    
else:
    st.write(response)


if response and response.status_code == 200:
        
    data = response.json()
    
    st.write(data)
    
    tag = data['tag']
    st.write(f'Tag: {tag}')
    
    name = data['name']
    st.write(f'Name: {name}')
    
    trophies = data['trophies']
    st.write(f'Current Trophies: {trophies}')
    
    highest_trophies = data['highestTrophies']
    st.write(f'Highest Trophies: {highest_trophies}')
    
    exp_level = data['expLevel']
    st.write(f'Exp Level: {exp_level}')
    
    three_victories = data['3vs3Victories']
    st.write(f'3v3 Victories: {three_victories}')
    
    soloVictories = data['soloVictories']
    st.write(f'Solo Victories: {soloVictories}')
    
    duoVictories = data['duoVictories']
    st.write(f'2v2 Victories: {duoVictories}')
    
    brawlers = data['brawlers']
    st.write(f'Brawlers: {len(brawlers)}')
    

else:
    if response:
        st.write(f'There was an error. Status code: {response.status_code}')
    else:
        st.write('Its either blank or you entered the wrong tag')


