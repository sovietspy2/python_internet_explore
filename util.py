import re
import requests
from bs4 import BeautifulSoup
import logging
from urllib.parse import urlparse, urlunparse
import time
import redis_repository

def measure_execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed_time = time.time() - start_time
        logging.debug(f"{func.__name__} took {elapsed_time:.2f} seconds")
        return result
    return wrapper


@measure_execution_time
def getUrlContent(url):
    try:
        content = requests.get(url, timeout=3).content
        return content
    except requests.exceptions.RequestException as e:
        logging.warning(f"Failed to get site data error: {e}")
        return bytes("", "utf-8")
    except Exception as e:
        logging.error(f"Critical error {e}")


def explore(content):
    try:
        soup = BeautifulSoup(content, "html.parser")
    except Exception as e:
        logging.error(f"Could not parse this text: {content}, the problem is: {e}")
        return []
    links = soup.find_all("a")
    
    valid_links = [link.get("href") for link in links if is_valid_url(link.get("href")) ]

    extracted_links = [extract_base_url(link) for link in valid_links]
    
    logging.debug(f"Found {len(links)} links, valid: {len(valid_links)}, extraced: {len(extracted_links)}")
    
    return set(extracted_links)

def explore_all(url):

    if redis_repository.set_contains("already_visited_urls", url):
        logging.debug(f"skipping {url} because already visited")
        return []

    redis_repository.add_to_set("already_visited_urls", url)
    found_urls = explore(getUrlContent(url))
    return found_urls

def is_valid_url(url):

    if url is None: 
        return False

    # Regular expression to match a full internet URL
    url_pattern = re.compile(r'^(https?|ftp)://[^\s/$.?#].[^\s]*$')

    # Check if the provided URL matches the pattern
    return bool(url_pattern.match(url))


def extract_base_url(url):
    # Parse the input URL
    parsed_url = urlparse(url)

    # Create a new tuple with the same scheme, netloc, and other components, but with an empty path
    base_url = urlunparse((parsed_url.scheme, parsed_url.netloc, '', '', '', ''))

    return base_url

