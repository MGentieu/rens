import requests
import json

if __name__ == "__main__":
    start_timestamp = 1697519436
    end_timestamp = 1723733825
    
    cookies = {
        'spid': '1762416677769_4d11908e78245e99dd3d069ed254b36f_tupnvn4ji0djeaum',
        'newsListCounter': '0',
        '_ym_uid': '1762416685335675595',
        '_ym_d': '1762416685',
        '_ym_isad': '1',
    }

    headers = {
        'authority': 'tass.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/json;charset=UTF-8',
        # 'cookie': 'spid=1762416677769_4d11908e78245e99dd3d069ed254b36f_tupnvn4ji0djeaum; newsListCounter=0; _ym_uid=1762416685335675595; _ym_d=1762416685; _ym_isad=1',
        'origin': 'https://tass.com',
        'referer': 'https://tass.com/',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }

    json_data = {
        'sectionId': 4953,
        'limit': 10000,
        'type': 'all',
        'excludeNewsIds': '2039839,2039681,2039641,2039585',
        'imageSize': 434,
        'timestamp': 1723733825,
    }

    response = requests.post('https://tass.com/userApi/categoryNewsList', cookies=cookies, headers=headers, json=json_data)

    if response.status_code == 200:
        data = response.json()
        articles = data.get("newsList", [])

        # Filtrage par date
        filtered_articles = [
            article for article in articles
            if start_timestamp <= article.get("date", 0) <= end_timestamp
        ]

        # Format final
        output = {
            "newsList": filtered_articles
        }
    # Écriture dans le fichier articles.json
        with open("../data/articles.json", "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)

        print(f"{len(filtered_articles)} articles sauvegardés dans articles.json")
    else:
        print(f"❌ Erreur {response.status_code} : {response.text}")

