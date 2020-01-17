from simple_get import simple_get
from bs4 import BeautifulSoup as bs4
import csv


def parse_html(url):
    """Parse and return the html at url with Beautiful Soup 4."""
    raw_html = simple_get(url)
    return bs4(raw_html, 'html.parser')


url = 'https://databox.com/partners'
main_page = {
    'element': '#partners #listingCt li a'
}
agency_page = {
    'agency_link': '#partner #top-content .social a.web'
}
agency_info_links = []
agency_homepage_links = []


"""
Get all agency info page links from main page
Add them to agency_info_links
"""
for a in parse_html(url).select(main_page['element']):
    agency_info_links.append(f"{a['href']}")

"""
Get all agency homepage links from the info page links
Add them to agency_homepage_links
"""
for link in agency_info_links:
    html = parse_html(link)
    links_on_page = html.select(agency_page['agency_link'])

    if links_on_page:
        a = links_on_page[0]
        agency_homepage_links.append(f"{a['href']}")

with open('databox_partners.csv', mode='w') as databox_partners_file:
    databox_partners_writer = csv.writer(
        databox_partners_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for link in agency_homepage_links:
        databox_partners_writer.writerow([link])
