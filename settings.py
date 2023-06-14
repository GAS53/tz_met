import os
from random import choice
from time import sleep


MIN_SLEEP_TIME = 2
MAX_SLEEP_TIME = 7

# главное не перебрать количесво запросов
COUNT_CATEGORY_PARSER = 10 # 40  т.к. всего примерно 170 категорий 170/40 это примерно 4 экземпляра парсера
REQUETS_CATEGORY_PARSER = 1 # 4 количество одновременно работающих парсеров категорий

COUNT_LINKS_PARSER = 10 # 40  сколько максимально может парсить один парсер ссылок
REQUETS_LINKS_PARSER = 1 # 5 количество одновременно работающих парсеров каждой таблици




IS_VISIBLE = False


COOKIE_WITOUT_CITIES = [
                    {'name': 'banners_top_current_id', 'value': 'dipos_M_3_2021', 'path': '/', 'domain': '.23met.ru', 'secure': False, 'httpOnly': True, 'expiry': 1686719033, 'sameSite': 'None'},
                    {'name': 'banners_bottom_current_id', 'value': 'liskitrybprom_728_DV', 'path': '/', 'domain': '.23met.ru', 'secure': False, 'httpOnly': True, 'expiry': 1686719033, 'sameSite': 'None'},
                    {'name': '_ga', 'value': 'GA1.2.848863211.1686632634', 'path': '/', 'domain': '.23met.ru', 'secure': False, 'httpOnly': False, 'expiry': 1749704634, 'sameSite': 'None'},
                    {'name': '_gid', 'value': 'GA1.2.851770240.1686632634', 'path': '/', 'domain': '.23met.ru', 'secure': False, 'httpOnly': False, 'expiry': 1686719034, 'sameSite': 'None'},
                    {'name': '_gat', 'value': '1', 'path': '/', 'domain': '.23met.ru', 'secure': False, 'httpOnly': False, 'expiry': 1686632694, 'sameSite': 'None'},
                    {'name': '_ym_uid', 'value': '1686632634695394621', 'path': '/', 'domain': '.23met.ru', 'secure': False, 'httpOnly': False, 'expiry': 1718168634, 'sameSite': 'None'},
                    {'name': '_ym_d', 'value': '1686632634', 'path': '/', 'domain': '.23met.ru', 'secure': False, 'httpOnly': False, 'expiry': 1718168634, 'sameSite': 'None'},
                    {'name': '_ym_isad', 'value': '2', 'path': '/', 'domain': '.23met.ru', 'secure': False, 'httpOnly': False, 'expiry': 1686704634, 'sameSite': 'None'}]

COOKIE_WITOUT_CITIES1 =[
                    {'name': 'banners_top_current_id', 'value': 'severstal_P_2021', 'path': '/', 'domain': '.23met.ru', 'secure': False, 'httpOnly': True, 'expiry': 1686720585, 'sameSite': 'None'},
                    {'name': 'banners_bottom_current_id', 'value': 'liskitrybprom_728_M', 'path': '/', 'domain': '.23met.ru', 'secure': False, 'httpOnly': True, 'expiry': 1686720585, 'sameSite': 'None'},
                    {'name': '_ga', 'value': 'GA1.2.473618719.1686634186', 'path': '/', 'domain': '.23met.ru', 'secure': False, 'httpOnly': False, 'expiry': 1749706186, 'sameSite': 'None'},
                    {'name': '_gid', 'value': 'GA1.2.1206484626.1686634186', 'path': '/', 'domain': '.23met.ru', 'secure': False, 'httpOnly': False, 'expiry': 1686720586, 'sameSite': 'None'},
                    {'name': '_gat', 'value': '1', 'path': '/', 'domain': '.23met.ru', 'secure': False, 'httpOnly': False, 'expiry': 1686634246, 'sameSite': 'None'},
                    {'name': '_ym_uid', 'value': '1686634187297499128', 'path': '/', 'domain': '.23met.ru', 'secure': False, 'httpOnly': False, 'expiry': 1718170186, 'sameSite': 'None'},
                    {'name': '_ym_d', 'value': '1686634187', 'path': '/', 'domain': '.23met.ru', 'secure': False, 'httpOnly': False, 'expiry': 1718170186, 'sameSite': 'None'},
                    {'name': '_ym_isad', 'value': '2', 'path': '/', 'domain': '.23met.ru', 'secure': False, 'httpOnly': False, 'expiry': 1686706186, 'sameSite': 'None'}]



COOKIE_WITH_CITIES = [
                    {'name': '_gat', 'value': '1', 'path': '/', 'domain': '.23met.ru', 'secure': False, 'httpOnly': False, 'expiry': 1686632874, 'sameSite': 'None'},
                    {'name': '_ym_uid', 'value': '16866328151247839', 'path': '/', 'domain': '.23met.ru', 'secure': False, 'httpOnly': False, 'expiry': 1718168815, 'sameSite': 'None'},
                    {'name': '_ym_d', 'value': '1686632815', 'path': '/', 'domain': '.23met.ru', 'secure': False, 'httpOnly': False, 'expiry': 1718168815, 'sameSite': 'None'},
                    {'name': '_ym_isad', 'value': '2', 'path': '/', 'domain': '.23met.ru', 'secure': False, 'httpOnly': False, 'expiry': 1686704815, 'sameSite': 'None'},
                    {'name': 'mc_e_cn', 'value': 'msk%2Cspb%2Carhangelsk%2Castrahan%2Cbarnayl%2Cbelgorod%2Cbratsk%2Cbryansk%2Cvnovgorod%2Cvladivostok%2Cvladikavkaz%2Cvladimir%2Cvolgograd%2Cvologda%2Cvoronezh%2Cekb%2Civanovo%2Cizhevsk%2Cyoshkarola%2Cirkytsk%2Ckazan%2Ckalyga%2Ckemerovo%2Ckirov%2Ckrasnodar%2Ckrasnoyarsk%2Ckyrsk%2Clipetsk%2Cmagnitogorsk%2Cmahachkala%2Cminvody%2Cnabchelny%2Cnalchik%2Cnn%2Ctagil%2Cnovokyzneck%2Cnsk%2Cnovocherkassk%2Comsk%2Corel%2Corenbyrg%2Cpenza%2Cperm%2Cpyatigorsk%2Crostov%2Cryazan%2Csamara%2Csaransk%2Csaratov%2Csevastopol%2Csimferopol%2Csmolensk%2Csochi%2Cstavropol%2Csyrgyt%2Coskol%2Csyzran%2Ctaganrog%2Ctambov%2Ctver%2Ctolyatti%2Ctula%2Ctumen%2Cylianovsk%2Cylanyde%2Cufa%2Chabarovsk%2Ccheboksary%2Cchelyabinsk%2Ccherepovec%2Cchita%2Cusahalinsk%2Cyakytsk%2Cyaroslavl', 'path': '/', 'domain': '.23met.ru', 'secure': False, 'httpOnly': True, 'expiry': 2464232817, 'sameSite': 'None'},
                    {'name': 'banners_top_current_id', 'value': 'severstal_CH_2021', 'path': '/', 'domain': '.23met.ru', 'secure': False, 'httpOnly': True, 'expiry': 1686719217, 'sameSite': 'None'},
                    {'name': 'banners_bottom_current_id', 'value': 'liskitrybprom_728_SK', 'path': '/', 'domain': '.23met.ru', 'secure': False, 'httpOnly': True, 'expiry': 1686719217, 'sameSite': 'None'},
                    {'name': '_ga', 'value': 'GA1.2.1239410647.1686632815', 'path': '/', 'domain': '.23met.ru', 'secure': False, 'httpOnly': False, 'expiry': 1749704817, 'sameSite': 'None'},
                    {'name': '_gid', 'value': 'GA1.2.577805685.1686632815', 'path': '/', 'domain': '.23met.ru', 'secure': False, 'httpOnly': False, 'expiry': 1686719217, 'sameSite': 'None'}]

COOKIE_WITH_CITIES1 = [
                    {'name': '_gat', 'value': '1', 'path': '/', 'domain': '.23met.ru', 'secure': False, 'httpOnly': False, 'expiry': 1686634246, 'sameSite': 'None'},
                    {'name': '_ym_uid', 'value': '1686634187297499128', 'path': '/', 'domain': '.23met.ru', 'secure': False, 'httpOnly': False, 'expiry': 1718170186, 'sameSite': 'None'},
                    {'name': '_ym_d', 'value': '1686634187', 'path': '/', 'domain': '.23met.ru', 'secure': False, 'httpOnly': False, 'expiry': 1718170186, 'sameSite': 'None'},
                    {'name': '_ym_isad', 'value': '2', 'path': '/', 'domain': '.23met.ru', 'secure': False, 'httpOnly': False, 'expiry': 1686706186, 'sameSite': 'None'},
                    {'name': 'mc_e_cn', 'value': 'msk%2Cspb%2Carhangelsk%2Castrahan%2Cbarnayl%2Cbelgorod%2Cbratsk%2Cbryansk%2Cvnovgorod%2Cvladivostok%2Cvladikavkaz%2Cvladimir%2Cvolgograd%2Cvologda%2Cvoronezh%2Cekb%2Civanovo%2Cizhevsk%2Cyoshkarola%2Cirkytsk%2Ckazan%2Ckalyga%2Ckemerovo%2Ckirov%2Ckrasnodar%2Ckrasnoyarsk%2Ckyrsk%2Clipetsk%2Cmagnitogorsk%2Cmahachkala%2Cminvody%2Cnabchelny%2Cnalchik%2Cnn%2Ctagil%2Cnovokyzneck%2Cnsk%2Cnovocherkassk%2Comsk%2Corel%2Corenbyrg%2Cpenza%2Cperm%2Cpyatigorsk%2Crostov%2Cryazan%2Csamara%2Csaransk%2Csaratov%2Csevastopol%2Csimferopol%2Csmolensk%2Csochi%2Cstavropol%2Csyrgyt%2Coskol%2Csyzran%2Ctaganrog%2Ctambov%2Ctver%2Ctolyatti%2Ctula%2Ctumen%2Cylianovsk%2Cylanyde%2Cufa%2Chabarovsk%2Ccheboksary%2Cchelyabinsk%2Ccherepovec%2Cchita%2Cusahalinsk%2Cyakytsk%2Cyaroslavl', 'path': '/', 'domain': '.23met.ru', 'secure': False, 'httpOnly': True, 'expiry': 2464234189, 'sameSite': 'None'},
                    {'name': 'banners_top_current_id', 'value': 'severstal_Y_2021', 'path': '/', 'domain': '.23met.ru', 'secure': False, 'httpOnly': True, 'expiry': 1686720589, 'sameSite': 'None'},
                    {'name': 'banners_bottom_current_id', 'value': 'liskitrybprom_728_SZ', 'path': '/', 'domain': '.23met.ru', 'secure': False, 'httpOnly': True, 'expiry': 1686720589, 'sameSite': 'None'},
                    {'name': '_ga', 'value': 'GA1.2.473618719.1686634186', 'path': '/', 'domain': '.23met.ru', 'secure': False, 'httpOnly': False, 'expiry': 1749706189, 'sameSite': 'None'},
                    {'name': '_gid', 'value': 'GA1.2.1206484626.1686634186', 'path': '/', 'domain': '.23met.ru', 'secure': False, 'httpOnly': False, 'expiry': 1686720589, 'sameSite': 'None'}
                    ]



def get_path(val):
    return os.path.join(os.getcwd(), 'results', f'{val}.csv')

times = [i for i in range(MIN_SLEEP_TIME, MAX_SLEEP_TIME)]

def delay(multiplier=None):
    if multiplier:
        sleep(choice(times*multiplier))
    else:
        sleep(choice(times))



