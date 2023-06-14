import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import FirefoxOptions

from settings import IS_VISIBLE, delay, get_path


class BaseParser():
    def __init__(self, links=[]):
        self.links = links
        self.driver = self.init_parser()
        self.preparate()
        

    def run(self):
        try:
            res = self.sub_run()
            if res:
                return res
        finally:
            self.driver.close()

        
    def init_parser(self):
        opt = FirefoxOptions()
        if IS_VISIBLE:
            opt.add_argument('-headless')
        return webdriver.Firefox(options=opt)

    def preparate(self):
        '''загружаем сайт выбираем все регионы'''
        self.driver.get('https://multicity.23met.ru/')
        delay(2)
        city_table = self.driver.find_element(by=By.CLASS_NAME, value='citychooser-tab')
        choose_all_cities = city_table.find_element(by=By.ID, value='regionchooser-0')
        choose_all_cities.click()
        delay()
        btn_save = city_table.find_element(by=By.XPATH, value='/html/body/div[4]/table/tbody/tr/td[10]/div/input[11]')
        btn_save.click()
        delay()


class AllCategoresParser(BaseParser):

    def sub_run(self):
        categories_kit = self.driver.find_element(by=By.CLASS_NAME, value='tabs ')
        categories = categories_kit.find_elements(by=By.TAG_NAME, value='a')
        li = []
        for i in categories:
            li.append(i.get_attribute('href'))
        return li


class OneCategoryParser(BaseParser):

    def sub_run(self):
        categorys = []
        for link in self.links:
            print(f'link get OneCategoryParser {link}')
            self.driver.get(link)
            delay()
            categorys.extend(self.get_sub_category())
        return categorys

    def get_sub_category(self):
        pre_sub_category = self.driver.find_element(by=By.CLASS_NAME, value='panes ')
        sub_category = pre_sub_category.find_elements(by=By.TAG_NAME, value='a')
        li = []
        for i in sub_category:
            li.append(i.get_attribute('href'))
        return li


class OneLinkParser(BaseParser):

    def sub_run(self):
        for link in self.links:
            print(f'onelinkparser get {link}')
            self.driver.get(link)
            delay()
            fieldnames, all_rows = self.get_table(link)
            pre_name = link.split('/')
            name = f'{pre_name[-2]}_{pre_name[-1]}'
            print(f'for save {name} {fieldnames}')
            self.save_csv(name, fieldnames, all_rows)
        

    def get_table(self, link):
        '''получить таблицу и названия заголовков таблици для сохранения в csv'''
        table = self.driver.find_element(by=By.ID, value='table-price')
        pre_fieldnames = table.find_element(by=By.TAG_NAME, value='tr')
        pre_fieldnames = pre_fieldnames.find_elements(by=By.TAG_NAME, value='th')
        fieldnames = []
        for f_name in pre_fieldnames:
            fieldnames.append(f_name.text)
        pre_all_rows = table.find_element(by=By.TAG_NAME, value='tbody')
        all_rows = pre_all_rows.find_elements(by=By.TAG_NAME, value='tr')
        return fieldnames, all_rows
    
    def clean_values(self, val):
        '''очистка каждого значекния из таблици'''
        return val.strip().replace('\n', '')

    def update_fieldnames(self, fieldnames):
        res = []
        for fn in fieldnames:
            if fn == 'Цена за 1т, руб. с НДС':
                res.append('Цена за 1т, руб.')
            res.append(fn)
        return res

    def save_csv(self, name, fieldnames, all_rows):
        '''сохранение в csv'''
        fieldnames = self.update_fieldnames(fieldnames)
        print(f'fieldnames after update {fieldnames}')
        with open(get_path(name), 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in all_rows:
                line = row.find_elements(by=By.TAG_NAME, value='td')
                write_dict = {name: self.clean_values(line[num].text) for num, name in enumerate(fieldnames)}
                writer.writerow(write_dict)



def func_category_parser(links):
    OCP = OneCategoryParser(links)
    return OCP.run()



def func_link_parser(links):
    OLP = OneLinkParser(links)
    OLP.run()



if __name__ == '__main__':
    # m = OneCategoryParser('https://multicity.23met.ru/price/zaglyshka_flancevaya')
    # m.run()

    m = OneLinkParser('https://multicity.23met.ru/price/zaglyshka_flancevaya/250')
    m.run()

    # ['https://multicity.23met.ru/price/zaglyshka_flancevaya/250', 'https://multicity.23met.ru/price/zaglyshka_flancevaya/300', 'https://multicity.23met.ru/price/zaglyshka_flancevaya/350', 'https://multicity.23met.ru/price/zaglyshka_flancevaya/400', 'https://multicity.23met.ru/price/zaglyshka_flancevaya/450', 'https://multicity.23met.ru/price/zaglyshka_flancevaya/500', 'https://multicity.23met.ru/price/zaglyshka_flancevaya/600']