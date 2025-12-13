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
    with open(file) as f:
        for p in f:
            password = p.strip()
            count = pwned_api_check(password)
            if count:
                print(f"{password} was found {count} times ...")
            else:
                print(f"{password} was not found in the hack archive.")
        return "done!"


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
