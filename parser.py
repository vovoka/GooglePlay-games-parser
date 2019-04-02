
from selenium import webdriver
import time
import logging


logging.getLogger().setLevel(logging.INFO)


class Parser():
    ''' Parses game categories at Google play '''

    def __init__(self, initial_page='https://play.google.com/store/apps/category/GAME') -> object:
        logging.info(f'Start to create new Parser() instance')
        self.root_address = initial_page
        self.driver = webdriver.Chrome('./chromedriver')

    def parse_html(self, address: str) -> list:
        ''' Parse page, return list of all unique links'''

        logging.info(f'Load the page.')
        self.driver.get(address)
        logging.info(f'Wait...')
        # Wait page loads completely. It's not perfect, but simple way. 
        time.sleep(6)
        logging.info(f'Extract all links from the page.')
        links = self.get_unique_links(self.driver)
        return links

    def scroll_down_page(self, browser: object) -> None:
        ''' Scroll current page till it's end'''

        # Value might be changed. Depends of CPU and connection speed
        SCROLL_PAUSE_TIME = 1

        # Get scroll height
        last_height = self.driver.execute_script(
            "return document.body.scrollHeight")
        while True:
            logging.info('    scrolling...')
            # Scroll down to bottom
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script(
                "return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        return 0

    def get_unique_links(self, browser: object) -> set:
        ''' Return set of unique hrefs'''

        return set([(obj.get_attribute('href')) for obj in self.driver.find_elements_by_xpath('//*[@href]')])

    def get_games_by_category(self, category: str) -> list:
        ''' Returns list of games belonged to the category'''

        logging.info(f'Handle category: {category}.')
        # Create a list to populate later
        games_by_category = list()

        links = self.parse_html(f'{self.root_address}_{category}')

        # Filter game-links only
        collection_links = list(
            filter(lambda link: 'apps/collection' in link, links))

        logging.info(
            f'Collected collections links psc.: {len(collection_links)}')
        # If no any collection link found then check current page for a games.
        if len(collection_links) == 0:
            logging.info(f'No collections found -> parse this page for games.')
            game_links = list(filter(lambda link: 'id=com.' in link, links))
            logging.info(f'At the page collected games : {len(game_links)} psc.')
            # Add recently founeded game name(s) to common list
            games_by_category.extend([(g.split('id=com.')[1]) for g in game_links])

        logging.info(f'Handle category links.')
        # Visit all 'collections'.
        for collection_link in collection_links:
            logging.info(f'Visit link: {collection_link}')
            # Get all the page links
            links = self.parse_html(collection_link)
            # Filter link of games only
            game_links = list(filter(lambda link: 'id=com.' in link, links))
            logging.info(f'Collected games psc.: {len(game_links)}')
            # Add recently founeded game name(s) to the cumulative list
            games_by_category.extend(
                [(g.split('id=com.')[1]) for g in game_links])
        return games_by_category

    def get_games_by_keyword(self, key_word: str) -> list:
        ''' Returns list of games with a keywords'''

        logging.info(f'CALL get_games_by_keyword(). ARG: "{key_word}"')
        links = self.parse_html(f'https://play.google.com/store/search?q={key_word}&c=apps')
        logging.info(f'PARSE PAGE: https://play.google.com/store/search?q={key_word}&c=apps')
        # Filter game-links only
        collection_links = list(
            filter(lambda link: 'apps/collection' in link, links))
        game_full_links = list(filter(lambda link: 'id=com.' in link, links))
        game_links = [(g.split('id=com.')[1]) for g in game_full_links]
        return game_links

