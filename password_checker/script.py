import requests
import hashlib
import sys


def request_api_data(query_char):
    url = "https://api.pwnedpasswords.com/range/" + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(
            f"Error fetching: {res.status_code}, check the API and try again."
        )
    return res


def get_password_leak_count(hashes, hash_to_check):
    hashes = (line.split(":") for line in hashes)
    for hash, count in hashes:
        if hash == hash_to_check:
            return count
    return 0


def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    head, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(head)
    hashes = response.text.splitlines()
    return get_password_leak_count(hashes, tail)


def main(file):
    try:
        with open(file) as f:
            for password in f:
                count = pwned_api_check(password.strip())
                with open("results.txt", mode="a", encoding="utf-8") as results:
                    if count:
                        results.write(
                            f"{password.strip()} - was found {count} times.\n"
                        )
                    else:
                        results.write(f"{password.strip()} - is secure.\n")
            return "done!"
    except FileNotFoundError:
        print("File was not found.")


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1]))
    except IndexError:
        print("Please enter a file name when running the script.")
