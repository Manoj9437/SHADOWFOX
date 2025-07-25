import requests
from bs4 import BeautifulSoup

def get_latest_headlines(site_link):
    '''
    Retrieves and prints the top news items from select news platforms.
    The code is generalized for specific URL patterns.

    Args:
        site_link (str): The target news website URL.
    '''
    url = site_link.strip().split('?')[0]
    print(f"\nTrying to reach: {url}")

    try:
        hdrs = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
        }
        resp = requests.get(url, headers=hdrs, timeout=15)
        resp.raise_for_status()
        print("Page successfully loaded.")

        soup_obj = BeautifulSoup(resp.content, 'html.parser')
        print(f"\n--- Top Headlines from {url} ---")
        found = False

        if 'hindustantimes.com' in url:
            h_lines = soup_obj.find_all('h3', class_='hdg3')
            if h_lines:
                found = True
                for idx, item in enumerate(h_lines, 1):
                    anchor = item.a
                    if anchor:
                        txt = anchor.get_text(strip=True)
                        ref = anchor['href']
                        if not ref.startswith('http'):
                            ref = f"https://www.hindustantimes.com{ref}"
                        print(f"\n{idx}. {txt}")
                        print(f"   Link: {ref}")

        elif 'aajtak.in' in url:
            anchors = soup_obj.find_all('a', title=True)
            if anchors:
                found = True
                cnt = 1
                history = set()
                for anch in anchors:
                    txt = anch['title'].strip()
                    ref = anch['href']
                    if (txt and
                        ref.startswith('https://www.aajtak.in/') and
                        'videos' not in ref and
                        txt not in history):
                        print(f"\n{cnt}. {txt}")
                        print(f"   Link: {ref}")
                        history.add(txt)
                        cnt += 1

        elif 'abplive.com' in url:
            anchors = soup_obj.find_all('a', title=True)
            if anchors:
                found = True
                cnt = 1
                history = set()
                for anch in anchors:
                    txt = anch['title'].strip()
                    ref = anch['href']
                    if txt and ref.startswith('https://') and txt not in history:
                        print(f"\n{cnt}. {txt}")
                        print(f"   Link: {ref}")
                        history.add(txt)
                        cnt += 1

        if not found:
            print("\nNo news items detected. It is possible that the site's markup was updated or isn't yet supported.")
            print("Supported on: 'hindustantimes.com', 'aajtak.in', 'abplive.com'.")
            return

        print("\n" + "=" * 40)

    except Exception as err:
        print(f"Encountered error: {err}")

if __name__ == '__main__':
    default_site = "https://www.hindustantimes.com/"

    while True:
        print("\nHeadline Scraper Utility")
        print("-------------------------------")
        print("Options:")
        print("1: Use default (Hindustan Times)")
        print("2: Supply another news URL")
        print("3: Quit")

        user_pick = input("Your choice (1, 2, or 3): ").strip()

        if user_pick == '1':
            print(f"\nSelected default: {default_site}")
            get_latest_headlines(default_site)

        elif user_pick == '2':
            link = input("\nPaste the news URL: ").strip()
            if link:
                get_latest_headlines(link)
            else:
                print("\nNo link was provided.")

        elif user_pick == '3':
            print("\nTerminating program. Bye!")
            break

        else:
            print("\nOption not recognized, please input 1, 2, or 3.")
