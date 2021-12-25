from bs4 import BeautifulSoup
import re
import requests

APARTMENTS = {
    "Aertson Midtown": "https://www.aertsonmidtown.com/floorplans",
    "Morris": "https://livemorris.com/floor-plans/#/plan?bedrooms=31",
    "2010 West End": "https://2010westend.com/floorplans/bed-2/so-rent/sd-desc",
}


class ApartmentPriceTracker:
    def __init__(self, apts: dict=APARTMENTS):
        self.apartments = apts  # APT_NAME: APT_URL
        return

    def get_soup(self, apt_name) -> BeautifulSoup:
        try:
            assert apt_name in self.apartments
        except AssertionError:
            print(f"Price tracking for '{apt_name}' is not supported.")
            return bytes()

        web_page = requests.get(self.apartments[apt_name]).content
        soup = BeautifulSoup(web_page, "html.parser")

        return soup

    def get_prices(self, apt_name) -> list[float]:
        soup = self.get_soup(apt_name)

        apt_prices = list()

        if apt_name == "Aertson Midtown":
            # Look for h2 tag with class 'card-title' (h2 text specifies floorplan name)
            # Up two is div tag with class 'card'
            # 'card' has child div tag with class 'card-body'
            # 'card-body' has child div tag with child p tag with text of price

            floorplan_title_elems = soup.find_all("h2", class_="card-title", string=re.compile("^\s*2"))  # Only targets 2 bed floorplans
            floorplan_card_elems = [title_elem.parent.parent for title_elem in floorplan_title_elems]
            floorplan_price_elems = [card_elem.find("div", class_="card-body").find("p") for card_elem in floorplan_card_elems]
            
            # RegEx pattern for parsing price value
            pattern = re.compile(r"\$(\S*)\s")
            
            for price_elem in floorplan_price_elems:
                match = pattern.search(price_elem.text)
                price = float(match.group(1).replace(",", "")) if match is not None else 0  # Remove , characters and convert to float
                apt_prices.append(price)

        elif apt_name == "Morris":
            # TODO

            # Look for 4th (last) li tag in ul with class 'card__stats'
            # Text of li tag is 'Starting at $[price]'

            pass
        elif apt_name == "2010 West End":
            # TODO

            # Each floorplan is represented by a chart with each row being a unit
            # Charts are contained in div tag with class 'additional-content__rows'
            # Each row is div tag with class 'row'
            # Price is text of span tag within last child div tag of a row

            pass
        
        return apt_prices


if __name__ == "__main__":
    apt_price_tracker = ApartmentPriceTracker()

    print("-----------------")
    print("Apartment Prices:")
    print("-----------------")
    for apt_name in apt_price_tracker.apartments:
        print(f"{apt_name}: {[f'${price:.2f}' for price in apt_price_tracker.get_prices(apt_name)]}")
