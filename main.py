from bs4 import BeautifulSoup
import re
import sqlite3
import fitz


def create_database():
    connection = sqlite3.connect('dict.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS proverbs (
            id INTEGER PRIMARY KEY,
            Russian TEXT,
            Lak TEXT
        )
    ''')
    # cursor.execute("PRAGMA table_info(proverbs)")
    # print(cursor.fetchall())

    connection.commit()
    connection.close()


def parse_and_insert(html_text):
    connection = sqlite3.connect('dict.db')
    cursor = connection.cursor()

    soup = BeautifulSoup(html_text, 'html.parser')
    proverb_pattern = re.compile(r'([^а-яА-Я]+)\s*([^а-яА-Я]+)\s*—\s*([^а-яА-Я]+)\s*([^а-яА-Я]+)\s*')

    proverbs = soup.find_all('p')
    for i in range(0, len(proverbs), 2):
        match = proverb_pattern.search(proverbs[i].text)

        lak_match = proverb_pattern.search(proverbs[i].text)
        russian_match = proverb_pattern.search(proverbs[i + 1].text)

        if lak_match and russian_match:
            lak = lak_match.group(1).strip()
            russian = russian_match.group(1).strip()

        if match:
            russian = proverbs[i + 1].text.strip()
            lak = match.group(1).strip()
    # for match in soup.find_all('p'):
    #     proverbs = proverb_pattern.findall(match.text)

    #     for lak, russian in proverbs:
            cursor.execute("INSERT INTO proverbs (Russian, Lak) VALUES (?, ?)", (russian, lak))

    connection.commit()
    connection.close()

def extract_text_from_pdf(pdf_path):
    text = ''
    with fitz.open(pdf_path) as pdf_document:
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text += page.get_text()
    return text

def pdf_to_html(pdf_path):
    html_text = '<html><body>'

    with fitz.open(pdf_path) as pdf_document:
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            html_text += f'<p>{page.get_text()}</p>'

    html_text += '</body></html>'
    return html_text

def main():
    pdf_path = '/home/azat/PycharmProjects/parser_laks/lak.pdf'
    html_text = pdf_to_html(pdf_path)
    create_database()
    parse_and_insert(html_text)

if __name__ == '__main__':
    main()
