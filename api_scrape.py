import csv
import requests

from bs4 import BeautifulSoup


languages = ["java", "python", "dotnet", "ruby"]


def pagescraper(response):
    soup = BeautifulSoup(r.text, "html.parser")
    api_table = soup.find("table", class_="directory responsive")
    api_table_rows = api_table.find_all("tr")
    for row in api_table_rows:
        if row.find("div", class_="google-directory-api"):
            line = []
            line.append(
                row.find("div", class_="google-directory-api").get_text()
            )
            api_details = row.find(
                "td", class_="google-directory-details-cell"
            )
            api_data = api_details.find_all(
                "td", class_="google-directory-api-data"
            )
            for detail in api_data:
                line.append(detail.get_text())

            library_writer.writerow(line)
        else:
            pass


with open("apis.csv", "w") as f:
    library_writer = csv.writer(f, delimiter=",")
    for language in languages:
        try:
            print("Requesting " + language + "...")
            r = requests.get(
                "https://developers.google.com/api-client-library/"
                + language
                + "/apis/"
            )
            r.raise_for_status()
            if r.status_code == 200:
                print("200 OK")
                pagescraper(r)
        except requests.exceptions.HTTPError as err:
            print(err)
            print("Skipping...")
            pass
