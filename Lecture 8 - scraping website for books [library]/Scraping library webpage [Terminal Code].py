xfrom bs4 import BeautifulSoup as soup
import requests
import csv

def read_html(url = "https://books.toscrape.com/index.html"):
    """Read links in requests and returns a single html.parser"""
    # First step read the url as normal links
    libraries = soup(requests.get(url).text, "html.parser")
    
    # return html tags
    return libraries

def get_category_links(libraries):
    """Returns lis of full links of category`s book"""
    # Fixed domain (i.e part of link doesn`t change)
    DomainLinks = "https://books.toscrape.com/"
    FullLinks = [ ]
    # make list for all cateogry links 
    for link in libraries.find_all("li", attrs={"class":""}):
        FullLinks.append(DomainLinks + link.find("a").get("href"))
        
    # return that list
    return FullLinks

def make_single_url_chunked(single_url = "https://books.toscrape.com/index.html"):
    """Cut a single link"""
    # split the coming link
    chunked = single_url.split("/")[:-1]
    page_html_link = [page for page in chunked ] 
    # combine after chunking with forward slash '/'
    https = "/".join(page_html_link) + "/"
    
    # return parts of https link
    return https

def get_next_page(single_page):
    """expected html tags"""
    while single_page != '':
        if single_page.find("ul", attrs = {"class":"pager"}):
            # Try if single_page could used 'find' on it!
            try:
                return single_page.find("ul", attrs = {"class":"pager"}).find("li", attrs={"class":"next"}).find("a").get("href")
            # Catch errors and break the loop in display_scarping
            except Exception as e:
                break
        else:
            # returning "" if there`s no next page to scrap
            return ""

def url_merge(part1, part2):
    """Mergeing url the fixed part and nexts part"""
    if part2 != None:
        # return mergeed URL-> links webpage
        return part1 + part2
    else:
        # returning "" if there`s no next page to scrap
        return part1 + ""

def write_file_header():
    """This function didicated to wite only header on file before calling scraping function"""
    # open the file and wite header
    with open("Books.csv", "a+", newline='',encoding='utf-8' ) as f:
        file = csv.writer(f)
        # the names of each column (i.e the header of whole informations)
        file.writerow(["Book-Name", "Rates", "Price", "Category"])

def write_on_file(page_html):
    """This function store scraped infromation on csv file"""
    # make dictionary to convert strings into ordinal numbers
    numerical_rates = {"One":1, "Two":2, "Three":3, "Four":4, "Five":5}
    
    # open a file in append position to write on it
    with open("LibraryScraping.csv", "a+", newline='',encoding='utf-8' ) as f:
        file = csv.writer(f)
        
        # fet the name of current category
        book_category = page_html.find("title").get_text().split("|")[0].strip()
        
        # loop in whole "HTML tags" to scraping and store information on csv file
        for row in page_html.find_all("article" , attrs= {"class":"product_pod"}):
            
            # assign variables scraped infromation and to save it on csv file later
            book_names = row.find("h3").find("a").get("title")
            book_rates = numerical_rates[row.find("p").get("class")[1]]
            book_prices = float(row.find_all("p", attrs={"class":"price_color"})[0].get_text()[2:])
            
            # save all information that has been scraped to csv file according to thier header`s name
            file.writerow([book_names, book_rates, book_prices, book_category])
            
def display_scraping(first_reading):
    """The main function starts scraping"""
    for single_link in get_category_links(first_reading)[10:12]:
        step2 = read_html(single_link)
        write_on_file(step2)

        lp_step3 = get_next_page(step2)
        fp_step4 = make_single_url_chunked(single_link)

        step5 = url_merge(fp_step4, lp_step3)

        while get_next_page(step2):
            lp_step3 = get_next_page(step2)
            fp_step4 = make_single_url_chunked(single_link)
            step5 = url_merge(fp_step4, lp_step3)

            step2 = read_html(step5)
            write_on_file(step2)
    print("The webpage has been scrapped")


if __name__ == "__main__":
    write_file_header()
    first_reading = read_html()
    display_scraping(first_reading)