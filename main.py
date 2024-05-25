from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import time
from selenium import webdriver
from datetime import datetime


def convert_date(date_str):
    try:
        parsed_date = datetime.strptime(date_str, "%d %B %Y")
        formatted_date = parsed_date.strftime("%Y-%m-%d")
        return formatted_date
    except ValueError:
        return None


output = []
def to_scrape(url):
    driver_ = webdriver.Chrome()
    driver_.get(url)
    time.sleep(2)
    # print(url)
    data = BeautifulSoup(driver_.page_source, 'html.parser')
    # print(data)

    try:
        title = data.find('h1', class_=True).text.strip()
        # print(title)
    except:
        title = ''

    try:
        author = data.find('span', class_='MuiTypography-root MuiTypography-body1 mui-style-1plnxgp').text.strip()
        # print(author)
    except:
        author = ''

    try:
        # book_ = data.find('ol', class_='MuiBreadcrumbs-ol mui-style-19zjai3')
        book_type = data.find('button', class_='MuiButtonBase-root MuiTab-root MuiTab-textColorInherit mui-style-9gsvmy').text.strip().replace('Details','').strip()
        # print(book_type)
    except:
        book_type = ''

    actual_price = ''
    discount_price = ''
    try:
        price_ = data.find('div', class_='MuiGrid-root MuiGrid-item MuiGrid-grid-xs-12 MuiGrid-grid-md-5 mui-style-1r482s6')
        if price_.find('span', class_='strike'):
            actual_price = price_.find('span', class_='strike').text.strip()
            discount_price = price_.find('p', class_='MuiTypography-root MuiTypography-body1 BuyBox_sale-price__PWbkg mui-style-tgrox').text.strip()
            # print(actual_price)
            # print(discount_price, '-----> discount price')
        else:
            actual_price = price_.find('p', class_='MuiTypography-root MuiTypography-body1 BuyBox_sale-price__PWbkg mui-style-tgrox').text.strip()
            # print(actual_price)
    except:
        book_price = ''

    try:
        book_detail = data.find('div', attrs={'aria-labelledby': 'pdp-tab-details'})
    except:
        book_detail = ''

    isbn_number = ''
    try:
        isbn_number = book_detail.find_all('p')[1].text.strip().replace('ISBN-10:','').strip()
        # print(isbn_number)
    except:
        isbn_number = ''

    book_detail_ = str(book_detail)
    publication_date = ''
    try:
        book_detail1 = re.sub(r'(Published: </span>)(.*?)(</p>)', r'<h1>\2</h1>', book_detail_)
        date_ = BeautifulSoup(book_detail1, 'html.parser').find('h1').text.strip()
        pub_date = re.sub(r'(\d+)(\w+ )(\w+ )(\d+)', r'\1 \3\4', date_).strip()
        publication_date = convert_date(str(pub_date))
        # print(publication_date)
    except:
        date_ = ''

    publisher = ''
    try:
        publish = re.sub(r'(Publisher: </span>)(.*?)(</p>)', r'<h2>\2</h2>', book_detail_)
        publisher = BeautifulSoup(publish, 'html.parser').find('h2').text.strip()
        # print(publisher)
    except:
        publish = ''

    pages = ''
    try:
        pages_ = re.sub(r'(Number of Pages: </span>)(.*?)(</p>)', r'<h3>\2</h3>', book_detail_)
        pages = BeautifulSoup(pages_, 'html.parser').find('h3').text.strip().replace('Pages','').strip()
        # print(pages)
    except:
        pages_ = ''

    dictionary = {'Title': title, 'Author': author, 'Book Type': book_type, 'Original Price': actual_price, 'Discount Price': discount_price,
                  'ISBN-10 NUmber': isbn_number, 'Publication Date': publication_date, 'Publisher': publisher, 'Pages': pages}
    output.append(dictionary)

    sub_data_ = ''
    try:
        sub_data = data.find('div', class_='MuiButtonGroup-root MuiButtonGroup-outlined MuiButtonGroup-fullWidth mui-style-1jmsxqb')
        sub_data_ = sub_data.find_all('a')[0]['href']
        # print(sub_data_)
    except:
        sub_data = ''

    if '/book/' in str(sub_data_):
        # print(sub_data_)
        driver_.get(sub_data_)
        time.sleep(2)
        data1 = BeautifulSoup(driver_.page_source, 'html.parser')

        try:
            book_title = data1.find('h1', class_='MuiTypography-root MuiTypography-h1 mui-style-1ngtbwk').text.strip()
            # print(book_title)
        except:
            book_title = ''

        try:
            book_author = data1.find('span', class_='MuiTypography-root MuiTypography-body1 mui-style-1plnxgp').text.strip()
            # print(book_author)
        except:
            book_author = ''

        book_actual_price = ''
        book_discount_price = ''
        try:
            book_price_ = data1.find('div',
                               class_='MuiGrid-root MuiGrid-item MuiGrid-grid-xs-12 MuiGrid-grid-md-5 mui-style-1r482s6')
            # print(book_price_)
            if book_price_.find('span', class_='strike'):
                book_actual_price = book_price_.find('span', class_='strike').text.strip()
                book_discount_price = book_price_.find('p', class_='MuiTypography-root MuiTypography-body1 BuyBox_sale-price__PWbkg mui-style-tgrox').text.strip()
                # print(book_actual_price)
                # print(book_discount_price, '-----> discount price')
            else:
                book_actual_price = book_price_.find('p',  class_='MuiTypography-root MuiTypography-body1 BuyBox_sale-price__PWbkg mui-style-tgrox').text.strip()
                # print(book_actual_price)
        except:
            book_price_ = ''

        book_type_ = ''
        book_pages_ = ''
        try:
            book_types_ = data1.find('div', class_='MuiButtonBase-root MuiTab-root MuiTab-labelIcon MuiTab-textColorInherit mui-style-ax6ycu')
            book_type_1 = str(book_types_).split('<br/>')[0]
            book_page1 = str(book_types_).split('<br/>')[1]
            book_type_ = BeautifulSoup(book_type_1, 'html.parser').text.strip()
            book_pages_ = BeautifulSoup(book_page1, 'html.parser').text.strip().replace('Pages','').strip()
            # print(book_type_)
            # print(book_pages_)
            # print()
        except:
            book_type_ = ''
            book_type = ''
            book_pages = ''

        book_detail_ = ''
        try:
            book_detail_ = data1.find('div', attrs={'aria-labelledby': 'pdp-tab-details'})
        except:
            book_detail_ = ''

        isbn_number_ = ''
        try:
            isbn_number_ = book_detail_.find_all('p')[1].text.strip().replace('ISBN-10:','').strip()
            # print(isbn_number_)
        except:
            isbn_number_ = ''

        book_detail_1 = str(book_detail)
        book_publication_date = ''
        try:
            book_details1 = re.sub(r'(Published: </span>)(.*?)(</p>)', r'<h1>\2</h1>', book_detail_1)
            book_date_ = BeautifulSoup(book_details1, 'html.parser').find('h1').text.strip()
            publ_date = re.sub(r'(\d+)(\w+ )(\w+ )(\d+)', r'\1 \3\4', book_date_).strip()
            book_publication_date = convert_date(str(publ_date))
            # print(book_publication_date)
        except:
            book_details1 = ''

        book_publisher = ''
        try:
            book_publish_ = re.sub(r'(Publisher: </span>)(.*?)(</p>)', r'<h2>\2</h2>', book_detail_1)
            book_publisher = BeautifulSoup(book_publish_, 'html.parser').find('h2').text.strip()
            # print(book_publisher)
        except:
            book_publisher = ''

        dictionary1 = {'Title': book_title, 'Author': book_author, 'Book Type': book_type_, 'Original Price': book_actual_price,
                      'Discount Price': book_discount_price,
                      'ISBN-10 NUmber': isbn_number_, 'Publication Date': book_publication_date, 'Publisher': book_publisher,
                      'Pages': book_pages_}
        output.append(dictionary1)

        audio_data_ = ''
        try:
            audio_data = data.find('div',
                                 class_='MuiButtonGroup-root MuiButtonGroup-outlined MuiButtonGroup-fullWidth mui-style-1jmsxqb')
            audio_data_ = sub_data.find_all('a')[-1]['href']
            # print(audio_data_)
        except:
            audio_data_ = ''

        if '/audiobook/' in str(audio_data_):
            print(audio_data_)
            driver_.get(audio_data_)
            time.sleep(2)
            audio_data = BeautifulSoup(driver_.page_source, 'html.parser')

            try:
                audio_title = audio_data.find('h1',
                                        class_='MuiTypography-root MuiTypography-h1 mui-style-1ngtbwk').text.strip()
                # print(audio_title)
            except:
                audio_title = ''

            try:
                audio_author = audio_data.find('span',
                                         class_='MuiTypography-root MuiTypography-body1 mui-style-1plnxgp').text.strip()
                # print(audio_author)
            except:
                audio_author = ''

            audio_actual_price = ''
            audio_discount_price = ''
            try:
                audio_price_ = audio_data.find('div',
                                         class_='MuiGrid-root MuiGrid-item MuiGrid-grid-xs-12 MuiGrid-grid-md-5 mui-style-1r482s6')
                # print(audio_price_)
                if audio_price_.find('span', class_='strike'):
                    audio_actual_price = audio_price_.find('span', class_='strike').text.strip()
                    audio_discount_price = audio_price_.find('p',
                                                           class_='MuiTypography-root MuiTypography-body1 BuyBox_sale-price__PWbkg mui-style-tgrox').text.strip()
                    print(audio_actual_price)
                    print(audio_discount_price, '-----> discount price')
                else:
                    audio_actual_price = audio_price_.find('p',
                                                         class_='MuiTypography-root MuiTypography-body1 BuyBox_sale-price__PWbkg mui-style-tgrox').text.strip()
                    print(audio_actual_price)
            except:
                audio_price_ = ''
            audio_type_ = ''
            audio_pages_ = ''

            try:
                audio_detail = audio_data.find('div', attrs={'aria-labelledby': 'pdp-tab-details'})
            except:
                audio_detail = ''

            audio_isbn_number = ''
            try:
                audio_isbn_number = book_detail.find_all('p')[1].text.strip().replace('ISBN-10:', '').strip()
                # print(audio_isbn_number)
            except:
                audio_isbn_number = ''

            audio_detail_ = str(audio_detail)
            audio_publication_date = ''
            try:
                audio_detail1 = re.sub(r'(Published: </span>)(.*?)(</p>)', r'<h1>\2</h1>', audio_detail_)
                audio_date_ = BeautifulSoup(audio_detail1, 'html.parser').find('h1').text.strip()
                audio_pub_date = re.sub(r'(\d+)(\w+ )(\w+ )(\d+)', r'\1 \3\4', audio_date_).strip()
                audio_publication_date = convert_date(str(audio_pub_date))
                print(audio_publication_date)
            except:
                audio_date_ = ''

            audio_publisher = ''
            try:
                audio_publish = re.sub(r'(Publisher: </span>)(.*?)(</p>)', r'<h2>\2</h2>', audio_detail_)
                audio_publisher = BeautifulSoup(audio_publish, 'html.parser').find('h2').text.strip()
                # print(audio_publisher)
            except:
                audio_publish = ''

            audio_pages = ''
            try:
                audio_pages_ = re.sub(r'(Number of Pages: </span>)(.*?)(</p>)', r'<h3>\2</h3>', audio_detail_)
                audio_pages = BeautifulSoup(audio_pages_, 'html.parser').find('h3').text.strip().replace('Pages', '').strip()
                # print(audio_pages)
            except:
                audio_pages = ''

            audio_book_type = ''
            try:
                audio_book_type = audio_data.find('h3',
                                      class_='MuiTypography-root MuiTypography-h3 mui-style-lijwn').text.strip().replace(
                    'Details', '').strip().title()
                print(audio_book_type)
            except:
                audio_book_type = ''

            dictionary2 = {'Title': audio_title, 'Author': audio_author, 'Book Type': audio_book_type, 'Original Price': audio_actual_price,
                          'Discount Price': audio_discount_price,
                          'ISBN-10 NUmber': audio_isbn_number, 'Publication Date': audio_publication_date, 'Publisher': audio_publisher,
                          'Pages': audio_pages}
            output.append(dictionary2)
            df = pd.DataFrame(output)
            df.to_csv('Output.csv', index=False)


if __name__ == "__main__":
    df_urls = pd.read_csv('input_list.csv', index_col=False)
    for ISBN_number in df_urls.itertuples():
        # print(ISBN_number[1])
        scrape_url = f"https://www.booktopia.com.au/across-the-seas-griff-hosker/ebook/{ISBN_number[1]}.html"
        scrape_urls = to_scrape(scrape_url)
        # print(scrape_url)
