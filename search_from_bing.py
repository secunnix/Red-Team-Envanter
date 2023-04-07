import requests

def bing_employee_search(company, subscription_key, max_results=500):
    url = "https://api.bing.microsoft.com/v7.0/search"
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    count = 50
    names = []

    for offset in range(0, max_results, count):
        params = {
            "q": f"site:linkedin.com/in/ {company}",
            "count": count,
            "offset": offset,
            "mkt": "tr-TR",
            "safesearch": "Moderate"
        }

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json()

        if 'webPages' not in search_results:
            print("No web pages found in search results.")
            continue

        for result in search_results['webPages']['value']:
            try:
                # İsimleri LinkedIn URL'den ayıklama
                name = result['name'].split(" | ")[0].strip()
                names.append(name)
            except:
                continue

    return names

def clean_turkish_characters(text):
    turkish_chars = "ğĞüÜşŞıİöÖçÇ"
    english_chars = "gGuUsSiIoOcC"
    translation_table = str.maketrans(turkish_chars, english_chars)
    return text.translate(translation_table)

def extract_and_clean_names(file_path):
    cleaned_names = []

    with open(file_path, "r", encoding="utf-8") as file:
        for name in file:
            try:
                parts = name.split(" - ")
                if len(parts) < 3 or "sirketismi" not in parts[2].lower():
                    continue  # Eğer üçüncü parametrede 'sirketismi' kelimesi geçmiyorsa atla

                name = parts[0].strip()  # Şirket ve pozisyon bilgilerini ayıklama
                first_name, last_name = name.split()[:2]  # ilk ad ve soyadı al
                first_name = clean_turkish_characters(first_name)
                last_name = clean_turkish_characters(last_name)
                cleaned_names.append((first_name, last_name))
            except:
                continue

    return cleaned_names

def generate_emails(names_list, domain):
    emails = set()

    for first_name, last_name in names_list:
        email = f"{first_name.lower()}.{last_name.lower()}@{domain}"
        emails.add(email)

    return list(emails)

subscription_key = "xxx"  # Bing API
company = "xxxx ltd"
file_path = "isimler2.txt"

names = bing_employee_search(company, subscription_key)

with open(file_path, "w", encoding="utf-8") as file:
    for name in names:
        file.write(f"{name}\n")

domain = "xxx.com.tr"
cleaned_names = extract_and_clean_names(file_path)
emails = generate_emails(cleaned_names, domain)
for email in emails:
    print(email)
