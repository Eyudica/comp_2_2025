import requests
from bs4 import BeautifulSoup, SoupStrainer
import argparse
def urls_list():
    urls=[]
    while True:
        url = input("Introduce la url a extraer: ")
        
        if url == "": 
            break
        else:
            urls.append(url)
    return urls


def send_request(url):
    try:
        response = requests.get(url)
        return response.text
    except:
        return "Error"

def get_title(soup):
    page_title_tag = soup.title
    if page_title_tag:
        page_title = page_title_tag.text
        return f"Page Title: {page_title}"
    else:   
        return "No title found"
def get_links(soup):
    hrefs=set()
    for link in BeautifulSoup(response, 'html.parser', parse_only=SoupStrainer('a')):
        if link.has_attr('href'):   
            if link['href'].startswith('http'):
                hrefs.add(link['href'])
    return hrefs

def process_data(soup): 
    title=get_title(soup)   
    hrefs=get_links(soup)
    return title,hrefs        
def meta_description(soup):
    meta_description_tag = soup.find("meta", attrs={"name": "description"})
    if meta_description_tag:
        meta_description = meta_description_tag["content"]
        return f"Meta Description: {meta_description}"
    else:
        return "No meta description found"  
def meta_keywords(soup):
    meta_keywords_tag = soup.find("meta", attrs={"name": "keywords"})
    if meta_keywords_tag:
        meta_keywords = meta_keywords_tag["content"]
        return f"Meta Keywords: {meta_keywords}"
    else:
        return "No meta keywords found"
def open_graph(soup):
    og_tags = soup.find_all("meta", attrs={"property": True})  # todas las <meta> con "property"
    og_data = {}

    for tag in og_tags:
        prop = tag.get("property")
        if prop and prop.startswith("og:"):  # filtra las que son Open Graph
            content = tag.get("content", "")
            og_data[prop] = content

    return og_data if og_data else "No Open Graph tags found"
 
def count_images(soup):
    images=len(soup.find_all('img'))
    return f"Cantitad de imagenes: {images}"
def count_headers(soup):
    
    headers_count = {}
    for i in range(1, 7):  # del H1 al H6
        tag = f'h{i}'
        headers_count[tag] = len(soup.find_all(tag))
    return headers_count
def extract_page_data(soup):
    data = {}
    data['title'] = get_title(soup)
    data['links'] = list(get_links(soup))
    data['meta_description'] = meta_description(soup)
    data['meta_keywords'] = meta_keywords(soup)
    data['open_graph'] = open_graph(soup)
    data['images_count'] = count_images(soup)
    data['headers_count'] = count_headers(soup)
    return data

if __name__ == "__main__":
    # parser=argparse.ArgumentParser()
    # parser = argparse.ArgumentParser(description="Servidor de Procesamiento Distribuido")
    # parser.add_argument("--ip","-ip",required=True,help="Direccion de escucha")
    # parser.add_argument("--port","-p",required=True,type=int,help="Puerto de escucha")
    # parser.add_argument("--workers","-w",required=True,type=int,help="workers (default: 4)")

    # args=parser.parse_args()

    urls=[]
    while True:
        url=input("Introduce la url a extraer: ")
        if url == "": 
            break
        else:   
            urls.append(url)

  
    for url in urls:
            response = send_request(url)
            soup = BeautifulSoup(response, "html.parser")
            page_data = extract_page_data(soup)
            print(page_data)
