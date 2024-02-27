from urllib.parse import urlsplit


def build_url(*argv:str):
    scheme, hostname, path, *other = urlsplit(argv[0])
    return f'{scheme}://' + '/'.join((hostname, path) + argv[1:]).replace('///', '/').replace('//', '/')