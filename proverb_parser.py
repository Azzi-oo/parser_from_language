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
    cursor.execute("PRAGMA table_info(proverbs)")
    print(cursor.fetchall())

    connection.commit()
    connection.close()


def parse_and_insert(html_text):
    connection = sqlite3.connect('dict.db')
    cursor = connection.cursor()

    soup = BeautifulSoup(html_text, 'html.parser')
    proverb_pattern = re.compile(r'([^\[\]]+)\s*\[([^\[\]]+)\]')

    # proverbs = proverb_pattern.findall(text)
    for match in soup.find_all('p'):
        proverbs = proverb_pattern.findall(match.text)

        for lak, russian in proverbs:
            cursor.execute("INSERT INTO proverbs (Russian, Lak) VALUES (?, ?)", (russian.strip(), lak.strip()))

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
    text = extract_text_from_pdf(pdf_path)
    html_text = f'<html><body>{text}</body></html>'
    return html_text

def main():
    pdf_path = '/home/azat/PycharmProjects/parser_laks/lak.pdf'
    html_text = pdf_to_html(pdf_path)
    create_database()
    parse_and_insert(html_text)

if __name__ == '__main__':
    main()