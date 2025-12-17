import requests
import hashlib
import sys


def request_api_data(query_char):
    # Request API data with the first five chars of our hashed password.
    url = "https://api.pwnedpasswords.com/range/" + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(
            f"Error fetching: {res.status_code}, check the API and try again."
        )
    return res


def get_password_leak_count(hashes_list, hash_to_check):
    # Create a tuple by splitting each line into a hash and count of hacks.
    hashes = (line.split(":") for line in hashes_list)

    for hash, count in hashes:
        if hash == hash_to_check:
            return count
    return 0


def pwned_api_check(password):
    # Hash our password.and split it into two parts.
    sha1password = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    head, tail = sha1password[:5], sha1password[5:]

    # Make the API request with the first part of the hash.
    response = request_api_data(head)
    # Convert the response into a list of hashes and count of hacks.
    hashes_list = response.text.splitlines()
    # Send the hashes list with the tail, which is not included in the API call.
    return get_password_leak_count(hashes_list, tail)


def main(file):
    try:
        with open(file) as f:
            for p in f:
                password = p.strip()
                count = pwned_api_check(password)
                with open("results.txt", mode="a", encoding="utf-8") as results:
                    if count:
                        results.write(f"{password} - was found {count} times.\n")
                    else:
                        results.write(f"{password} - is secure.\n")
            return "done!"
    except FileNotFoundError:
        print("File was not found.")


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1]))
    except IndexError:
        print("Please enter a file name with passwords when running the script.")
