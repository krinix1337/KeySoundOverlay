import urllib.request
import json
import os

repo_url = 'https://api.github.com/repos/dusklinux/wayclick_soundpacks/contents/'
packs = [
    'glorious_panda',
    'kailh_box_white',
    'cherry_mx_black_abs',
    'cherry_mx_brown_abs',
    'cherry_mx_red_abs',
    'tealios_v2',
    'nk_cream',
    'unicomp_classic'
]

os.makedirs('assets', exist_ok=True)

for pack in packs:
    try:
        req = urllib.request.Request(repo_url + pack + '?ref=main', headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            files = json.loads(response.read().decode())
            audio_file = next((f for f in files if f['name'].endswith(('.ogg', '.wav', '.mp3'))), None)
            if audio_file:
                print(f'Found {audio_file["name"]} in {pack}')
                download_url = audio_file['download_url']
                target_name = pack + os.path.splitext(audio_file['name'])[1]
                
                req2 = urllib.request.Request(download_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req2) as resp2:
                    with open(os.path.join('assets', target_name), 'wb') as f:
                        f.write(resp2.read())
                print(f'Downloaded {target_name}')
            else:
                print(f'No audio file found in {pack}')
    except Exception as e:
        print(f'Failed {pack}: {e}')
