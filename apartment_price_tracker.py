from bs4 import BeautifulSoup
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

    def get_prices(self, apt_name) -> list[float]:
        try:
            assert apt_name in self.apartments
        except AssertionError:
            print(f"Price tracking for '{apt_name}' is not supported.")
            return list()

        response = requests.get(self.apartments[apt_name])
        soup = BeautifulSoup(response.content, "html.parser")

        apt_prices = list()

        if apt_name == "Aertson Midtown":
            # TODO
            
            # Look for h2 tag with class 'card-title' (h2 text specifies floorplan name)
            # Up two is div tag with class 'card'
            # 'card' has child div tag with class 'card-body'
            # 'card-body' has child div tag with child p tag with text of price

            pass
        elif apt_name == "Morris":
            # TODO

            # Look for 4th li tag in ul with class 'card__stats'
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

    print("Minimum prices found:")
    print("---------------------")
    for apt_name in APARTMENTS:
        print(f"{apt_name}: ${min(apt_price_tracker.get_prices(apt_name)):.2f}")
