import os
import requests
from collections import deque
from sys import argv

from bs4 import BeautifulSoup
from colorama import init, Fore, deinit


class Browser:
    """ Squirrel-Navigator"""

    def __init__(self):
        self.__ENCODE = 'utf-8'
        self.__FILE_EXTENSION = '.txt'
        self.__ERROR_INCORRECT_URL = Fore.RED + 'Error: Incorrect URL'
        self.__DOMAIN_PREFIX = 'https://'
        self.__DOMAIN_EXTENSION_LENGTH = 4
        self.__tags_sieve = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a']
        self.__file_path = ''
        self.__file_content = ''
        self.__current_browsing_history = deque()
        self.user_input = ''

    def process_filepath(self, args):
        """ Process command line arguments.
        If a new directory path is specified, create.
        Determine the file path.
        :param args: Command line arguments passed as-is
        :return: None
        """
        if len(args) == 2:
            directory = argv[1]
            if not os.path.exists(directory):
                os.makedirs(directory)
            self.__file_path = directory + '\\'

    def seek_input(self):
        """ Seek user input from the command line.
        :return: None
        """
        self.user_input = input('> ')
        return self.user_input

    def fetch_file_content(self, file_name):
        """ Fetch local file content.
        :param file_name: Derived from user input.
        :return: None
        """
        try:
            read_file = self.__file_path + file_name + self.__FILE_EXTENSION
            with open(read_file, encoding=self.__ENCODE) as file_open:
                for line in file_open:
                    print(line, end='')

            self.__current_browsing_history.append(file_name)
        except FileNotFoundError:
            print(self.__ERROR_INCORRECT_URL)

    def store_url_content(self, file_name):
        """ Store processed crawled website content.
        :param file_name: Derived from user input.
        :return: None
        """
        new_file_path = self.__file_path + file_name + self.__FILE_EXTENSION

        with open(new_file_path, 'w', encoding=self.__ENCODE) as new_file:
            for file_content in self.__file_content:
                new_file.write(file_content + '\n')
        self.__current_browsing_history.append(file_name)

    def browse_back(self):
        """ User enters 'back' in the command prompt.
        Just like viewing previously visited site page.
        :return: None
        """
        file_name = ''
        if len(self.__current_browsing_history) > 1:
            for _ in range(2):
                file_name = self.__current_browsing_history.pop()
            self.fetch_file_content(file_name)

    def page_colorify(self, filtered_page):
        """Text with hyperlinks on actual website are coded in blue.
        :param filtered_page: a BeautifulSoup iterable.
        :return: None
        """
        colored_page = []
        for page in filtered_page:
            stripped_line = page.get_text().strip()
            if stripped_line != '':
                colored_page.append(Fore.BLUE+stripped_line
                                    if page.name == 'a'
                                    else stripped_line)
        return colored_page

    def fetch_url_content(self, url):
        """ Crawl web-page.
        :param url: Direct user input.
        :return: None.
        """
        page = requests.get(url)
        if page:
            page_soup = BeautifulSoup(page.content, 'html.parser')
            page_soup_display = page_soup.find_all(self.__tags_sieve)
            return self.page_colorify(page_soup_display)
        return self.__ERROR_INCORRECT_URL

    def browse_url(self):
        """ Main logic
        :return: None
        """
        try:
            dot_find = dot_find_r = self.user_input.rfind('.')
            dot_find_l = self.user_input.find('.')
            if len(self.user_input[dot_find_r:]) > self.__DOMAIN_EXTENSION_LENGTH:
                dot_find = -1 if dot_find_l == dot_find_r else dot_find_r

            url = self.__DOMAIN_PREFIX + self.user_input
            if dot_find != -1:
                file_name = self.user_input[:dot_find]
                self.__file_content = self.fetch_url_content(url)

                for content in self.__file_content:
                    print(content)

                if self.__file_content == self.__ERROR_INCORRECT_URL:
                    pass
                self.store_url_content(file_name)

            elif self.user_input != 'exit':
                self.fetch_file_content(self.user_input)
        except:
            raise

    @staticmethod
    def usage():
        print(f'\n'
              f'{Fore.RED}'
              f'                                                       
              f'     _|_|_|  _|                                  _|      
              f'   _|        _|            _|_|_|      _|_|    _|_|_|_|  
              f'     _|_|    _|            _|    _|  _|_|_|_|    _|      
              f'         _|  _|            _|    _|  _|          _|      
              f'   _|_|_|    _|_|_|_|      _|    _|    _|_|_|      _|_|  
              f'{Fore.RESET}\n\n'
              'Usage:\n'
              f'1:    >>> {Fore.BLUE}A private and secure Text-Based web browser\n'
              f'                            {Fore.RESET}(Go to )\n'
              f'2:    >>> > {Fore.GREEN}Enter a URL\n'
              f'            {Fore.RESET}(type a website URL without https)\n'
              f'4:    >>> > {Fore.GREEN}back\n'
              f'            {Fore.RESET}(type back to access browsing history)\n'
              f'5:    >>> > {Fore.GREEN}exit{Fore.RESET}\n'
              f'            Text in {Fore.BLUE}blue{Fore.RESET}'
              f' are hyperlinks on a website.'
              f'{Fore.RESET}\n'
              f'6:    >>> > {Fore.GREEN}use seARch! Terminal edition!!\n'
              f'            {Fore.RESET}a private and secure web portal to use it type: squirrelcom.github.io/seARchter\n'
              )


if __name__ == '__main__':
    init(autoreset=True)
    Browser.usage()

    browse = Browser()
    browse.process_filepath(argv)
    while browse.seek_input() != 'exit':
        try:
            if browse.user_input == 'back':
                browse.browse_back()
                continue
            browse.browse_url()
        except requests.exceptions.ConnectionError:
            print(f'{Fore.MAGENTA}Unable to fetch {browse.user_input} (Squirrel-Navigator cannot locate that URL?)')
    deinit()
