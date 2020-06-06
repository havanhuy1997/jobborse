from jobborse.chrome_broswer import ChromeDriver
from jobborse.file import Excel
from jobborse.utils import get_3_first_words
from django.conf import settings
import os

URL = 'https://jobboerse.arbeitsagentur.de/vamJB/stellenangeboteFinden.html?execution=e1s1'

def get_existing_code(output_file):
    existing_codes = []
    for line in output_file.get_lines():
        code = line['Code']
        if code not in existing_codes: 
            existing_codes.append(code)
    print('Existing code:', existing_codes)
    return existing_codes

def clear_input_and_send_key(input, key):
    input.clear()
    input.send_keys(key)

def run(task):
    output_file = Excel('output.xlsx')
    input_file = Excel(task.input_file.name)  
    chrome_driver = ChromeDriver()
    existing_codes = get_existing_code(output_file)
    lines = input_file.get_lines()
    for i in range(len(lines)):
        task.progress = (i + 1) / len(lines)
        task.save()
        line = lines[i]
        code = line['Code']
        if code not in existing_codes:
            keyword = line['Keyword']
            company_name = get_3_first_words(line['Company Name'])
            post_code = line['Post Code']
            print('\n--searching for keyword {}, company name {}, post code {}'.format(keyword, company_name, post_code))
            
            back_btn = chrome_driver.find_element(ChromeDriver.ID_TYPE, 'sucheandern_unten')
            if back_btn:
                back_btn.click()
            else:
                chrome_driver.get(URL)

            keyword_input = chrome_driver.find_element(ChromeDriver.ID_TYPE, 'berufe')
            company_name_input = chrome_driver.find_element(ChromeDriver.ID_TYPE, 'nurstellenmitfolgendenbegriffen')
            post_code_input = chrome_driver.find_element(ChromeDriver.ID_TYPE, 'arbeitsort.postleitzahl')
            if keyword_input and company_name_input and post_code_input:
                clear_input_and_send_key(keyword_input, keyword)
                clear_input_and_send_key(company_name_input, company_name)
                clear_input_and_send_key(post_code_input, post_code)
                address_input = chrome_driver.find_element(ChromeDriver.ID_TYPE, 'arbeitsort.ort')
                if address_input:
                    address_input.clear()
                submit_btn = chrome_driver.find_element(ChromeDriver.ID_TYPE, 'stellenangebotesuchen_unten')
                submit_btn.click()
                if 'Es sind keine Einträge vorhanden.' in chrome_driver.driver.page_source:
                    print('No job found, adding to output file')
                    output_file.add_row(list(line.values()))
                    existing_codes.append(code)
        else:
            print('{} already exists in output.xlsx'.format(code))

    output_file.save()
    chrome_driver.quite()   