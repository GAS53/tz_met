from all_parsers import AllCategoresParser
from multiprocessing import Pool


from all_parsers import func_category_parser, func_link_parser
from settings import COUNT_CATEGORY_PARSER, REQUETS_CATEGORY_PARSER, COUNT_LINKS_PARSER, REQUETS_LINKS_PARSER




def chunks(lst, n):
    '''разбиенене на заданное количество ссылок для парса'''
    li = []
    for i in range(0, len(lst), n):
        li.append(lst[i:i + n])
    return li

def multiprocess_parser(func, COUNT, REQUEST, li, is_return=True):
    '''запуск в мультипроцессе'''
    li = li[:15]  # удалить обрезание !!!!!!!!!!!!!!!
    chunk_links = chunks(li, COUNT)

    print(f'chunked li {chunk_links}')
    with Pool(REQUEST) as pool:
        if is_return:
            res = pool.map(func, chunk_links)
            return res
        else:
            pool.map(func, chunk_links)

def unpack_after_multiprocess(puck_li):
    unpack_li = []
    for i in puck_li:
        unpack_li.extend(i)
    return unpack_li


class Main():
    def run(self):
        ACP = AllCategoresParser()
        categories = ACP.run()
        links = multiprocess_parser(func_category_parser, COUNT_CATEGORY_PARSER, REQUETS_CATEGORY_PARSER, categories)
        links = unpack_after_multiprocess(links)
        multiprocess_parser(func_link_parser, COUNT_LINKS_PARSER, REQUETS_LINKS_PARSER, links, is_return=False)



if __name__ == '__main__':
    m = Main()
    m.run()
