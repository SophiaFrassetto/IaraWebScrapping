# build-in imports
import logging
from dataclasses import dataclass

# external imports
import pandas as pd
from bs4 import BeautifulSoup
from requests import get, Response
from typing import List

# project imports
from .model import Country


logging.basicConfig(level=logging.INFO)


@dataclass
class WebScrappingController:
    url: str
    file_name: str = 'countries.csv'

    def process(self):
        # get url response for parse later.
        resp = self._get_url_response()

        # parse HTML to beautifulsoup.
        soup = self._parse_html_response(html_response=resp.content)

        # response scrapping and transform in pandas Dataframe.
        dataframe = self._response_scrapping(soup=soup)

        # convert pandas dataframe to CSV and write.
        self._write_csv(dataframe=dataframe)

    def _get_url_response(self) -> Response:
        logging.info('Getting url reponse...')

        try:
            # get url response
            resp = get(self.url)
        except Exception as err:
            raise Exception(f'Error to get {self.url} respose - Error: {err}')

        # check if response exists and status != 200 for generate a error
        if not resp or resp == None or resp.status_code != 200:
            stts = resp.status_code if resp else None
            body = resp.text if resp else None
            raise Exception(f'Error to get {self.url} response - Response: {resp} - Status: {stts}, Body: {body}')

        return resp

    def _parse_html_response(self, html_response: str) -> BeautifulSoup:
        logging.info('parsing HTML reponse...')
        try:
            # create a Beutifulsoup from HTML response 
            soup = BeautifulSoup(html_response, 'html.parser')
        except Exception as err:
            raise Exception(f'Error to parse HTML with html.parser - {html_response[:15]} - {err}')

        return soup

    def _response_scrapping(self, soup: BeautifulSoup) -> pd.DataFrame:
        logging.info('Scrapping parsed response...')
        # set countries to populate later
        countries: List[Country] = []

        # get the section in <section class='countries'>
        section = soup.find(id='countries')
        # get all divs in <div class='row'>
        rows = section.find_all("div", class_="row")

        for row in rows:
            # get all columns with class='col-md-4 country' from that row
            collumns = row.find_all('div', class_="col-md-4 country")

            # pass if you don't have valid columns
            if not collumns:
                continue

            for collumn in collumns:
                if not collumn:
                    continue

                # create List with Countries
                countries.append(
                    Country(
                        # get name in <h3 class='country-name'>
                        name=collumn.find('h3', class_="country-name").text.strip(),
                        # get name in <span class='country-capital'>
                        capital=collumn.find('span', class_="country-capital").text.strip(),
                        # get name in <span class='country-population'>
                        population=int(collumn.find('span', class_="country-population").text.strip()),
                        # get name in <span class='country-arean'>
                        area=float(collumn.find('span', class_="country-area").text.strip())
                    )
                )

        # convert List[dict] to pandas dataframe and return that
        return pd.DataFrame([x.__dict__ for x in countries])

    def _write_csv(self, dataframe: pd.DataFrame):
        logging.info('Converting pandas dataframe to CSV...')
        try:
            # dataframe to csv with encoding utf-8
            dataframe.to_csv(self.file_name, encoding='utf-8', index=False)
        except Exception as err:
            raise Exception(f'Error to convert Pandas Dataframe to CSV - {err}')
