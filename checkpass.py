import requests
import hashlib
import sys


def getAPIData(query):
    url = 'https://api.pwnedpasswords.com/range/' + query
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(
            f'Error fetching from api, status code: {res.status_code}')
    return res


def getLeaksCount(hashes, check_hash):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == check_hash:
            return count
    return 0


def checkAPIData(password):
    hashedpass = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5, tail = hashedpass[:5], hashedpass[5:]
    response = getAPIData(first5)
    return getLeaksCount(response, tail)


def main(args):
    if not args:
        print('Please provide your password as a command line argument.')
    try:
        for password in args:
            count = checkAPIData(password)
            if count:
                print(
                    f'Your password {password} has been cracked {count} times.')
            else:
                print(f'Your password {password} has never been cracked!')
    except IndexError:
        print('Please provide your password as a command line argument.')


if __name__ == "__main__":
    main(sys.argv[1:])
