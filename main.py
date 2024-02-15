from bs4 import BeautifulSoup
import re
import sqlite3
import fitz


def create_database():
    try:
        connection = sqlite3.connect('dict.db')
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS proverbs (
                id INTEGER PRIMARY KEY,
                Russian TEXT,
                Lak TEXT,
                OrderIndex INTEGER
            )
        ''')
        connection.commit()
        connection.close()
    except sqlite3.Error as e:
        print(f"Error creating db: {e}")


def parse_and_insert(html_text):
    connection = sqlite3.connect('dict.db')
    cursor = connection.cursor()

    soup = BeautifulSoup(html_text, 'html.parser')
    proverbs = soup.find_all('p')

    for i in range(0, len(proverbs)-1, 3):
        if i + 2 < len(proverbs):
            lak_proverb = proverbs[i].text.strip()
            translation_proverb = proverbs[i+1].text.strip()
            russian_translation = proverbs[i+2].text.strip()

            cursor.execute("INSERT INTO proverbs (Lak, Russian, OrderIndex) VALUES (?, ?, ?)", (lak_proverb, translation_proverb, i))
            cursor.execute("INSERT INTO proverbs (Russian, OrderIndex) VALUES (?, ?)", (russian_translation, i+1))
        else:
            print(f"Skipping incomplete pair at index {i}")
    connection.commit()
    connection.close()


def extract_text_from_pdf(pdf_path):
    text = ''
    with fitz.open(pdf_path) as pdf_document:
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text += page.get_text()
    return text


def pdf_to_html(html_path):
    # html_text = '<html><body>'

    # with fitz.open(pdf_path) as pdf_document:
    #     for page_num in range(pdf_document.page_count):
    #         page = pdf_document[page_num]
    #         text = page.get_text()
    #         lines = text.split('\n')

    #         for i in range(0, len(lines)-1, 2):
    #             html_text += f'<p>{lines[i]} - {lines[i + 1]}</p>'
    #             # if i + 1 < len(lines):
    #             #     html_text += f'<p>{lines[i + 1]}</p>'

    # html_text += '</body></html>'
    # return html_text
    with open(html_path, 'r', encoding='utf-8') as html_file:
        html_text = html_file.read()
    return html_text


def main():
    # pdf_path = '/home/azat/PycharmProjects/parser_laks/lak.pdf'
    html_path = '/home/azat/PycharmProjects/parser_laks/lak.html'
    # html_path = 'lak.html'
    # with open(html_path, 'r', encoding='utf-8') as html_file:
    #     html_text = html_file.read()
    create_database()
    parse_and_insert(pdf_to_html(html_path))


if __name__ == '__main__':
    main()
