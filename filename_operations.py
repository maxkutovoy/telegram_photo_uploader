import os
from urllib.parse import unquote, urlsplit

from tldextract import extract


def define_filename_prefix(url):
    extracted_url = extract(url)
    return extracted_url.domain


def pars_filename(url):
    parsed_url = urlsplit(url)
    filename = os.path.split(unquote(parsed_url.path))[1]
    return filename
