import argparse
import requests

VERSION = 1.0
NAME = 'sic-feedback {}'.format(VERSION)


def shouldiclick_api(url: str, label: int, public_scan: bool, api_key: str) -> str:

    data = {
        'url': url,
        'label': int(label),
        'public_scan': bool(public_scan),
        'api_key': api_key

    }

    response: requests.models.Response = requests.post('http://147.32.83.233:8080',
                                                       data=data, json=data)
    try:
        res_dict = response.json()
        uuid = res_dict.get('uuid', None)
        if uuid:
            res = 'https://urlscan.io/result/' + uuid
        else:
            res = response.content
    except:
        res = response.content
    return res


def read_api_key(api_key_path: str) -> str:
    try:
        with open(api_key_path) as f:
            for line in f:
                if line[0] == '#':
                    continue
                api_key = line.strip().rstrip()
                return api_key
            return None
    except (FileNotFoundError, FileExistsError):
        return None


def check_arguments(api_key: str, api_key_path: str, label: int, public_scan: bool) -> bool:
    if api_key is None:
        print('Error: Api key file: {} was not found. Create or specify the path.'.format(api_key_path))
        return False
    try:
        label = int(label)
        if label < 0 or label > 3:
            print('Error: label must be integer from 0 to 3. Read help.')
            return False
    except ValueError:
        print('Error: label must be integer from 0 to 3. Read help.')
        return False

    try:
        _ = bool(public_scan)
    except ValueError:
        print('Error: Wrong usage of -p argument. Read help.')
    return True


def _print(v: int, link: str) -> None:
    if v > 0:
        if v > 1:
            print('Done! Wait few second and you can click for urlscsn.io result. (The urlscan analysis usually takes 30 seconds)')
        print(link)


def main() -> None:
    example_text = '''Examples:
     Submit "www.google.com" as normal website: 
            python sic-feedback.py -u 'www.google.com' -l 0
     Submit "www.google.com" as normal website wit public scan.: 
            python sic-feedback.py -u 'www.google.com' -l 0 -p
     Submit "www.phishing-website.com" as phishing website.
        python sic-feedback.py -u 'www.phishing-website.com' -l 2'''


    parser = argparse.ArgumentParser(epilog=example_text, formatter_class=argparse.RawDescriptionHelpFormatter)
    # action='store_true'
    parser.add_argument("-v", "--version", action='version', version='{}'.format(VERSION))
    parser.add_argument("-u", "--url", help="A URL to submit.", required=True)
    parser.add_argument("-l", "--label", help="A label: 0=normal URL, 1=malicious URL, 2=phishing, 3=malware. "
                                              "If you are not sure if a website is phishing or malwere, use 1 as malicious website.", required=True)
    parser.add_argument("-p", "--public", help="A scan in urlscan.io will be public.", action='store_true')
    parser.add_argument("-k", "--key_path", help="A path to Api key file. By default we try to red api_key.txt")
    parser.add_argument("-V", "--verbosity", help="Print: 0=nothing, 1=only link, 2=everything. Default: 2", default=2)
    args = parser.parse_args()

    api_key_path = args.key_path if args.key_path else 'api_key.txt'
    api_key = read_api_key(api_key_path)

    if check_arguments(api_key, api_key_path, args.label, args.public):
        link = shouldiclick_api(args.url, args.label, args.public, api_key)
        _print(int(args.verbosity), link)
    else:
        print('Nothing was done. Check errors and run again.')


if __name__ == '__main__':
    main()
