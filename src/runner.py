import concurrent
import os
from concurrent.futures import ProcessPoolExecutor

from core.config import settings


class Runner:
    def __init__(self, parser, request_manager):
        self.parser = parser
        self.request_manager = request_manager

    def get_category_links(self):
        with self.request_manager as session:
            if not os.path.exists("results"):
                os.mkdir("results")
            raw_category_data = session.get_request(settings.ROOT_URLS['wildberries'][1]).json()
            category_links = self.parser.parse_category_urls(raw_category_data)
        return category_links

    def get_products(self, cat_name, shard, query, page_num: int, session):
        if '/' in cat_name:
            cat_name = cat_name.split('/')[0]
        if not os.path.exists(os.path.join("results", cat_name)):
            os.mkdir(os.path.join("results", cat_name))

        all_category_products = []
        for page in range(1, page_num + 1):
            products = session.get_products_data(shard, query, page)
            if products is None:
                continue
            all_category_products.append([cat_name, page, products])
        return all_category_products

    def run(self, pages=1, workers=4):
        with self.request_manager as session:
            with ProcessPoolExecutor(max_workers=workers) as process_executor:
                processes = []
                for cat_name, attributes in self.get_category_links().items():
                    if attributes[0] is None or attributes[1] is None:
                        continue
                    get_data_process = process_executor.submit(self.get_products, cat_name=cat_name,
                                                               shard=attributes[0],
                                                               query=attributes[1],
                                                               page_num=pages,
                                                               session=session)
                    processes.append(get_data_process)
                processes_for_save = []
                for process in concurrent.futures.as_completed(processes):
                    for cat_name, page, products in process.result():
                        if products is None:
                            continue
                        save_data_process = process_executor.submit(self.parser.parse_category,
                                                                    category_name=cat_name,
                                                                    category_json=products.json(),
                                                                    page_num=page)
                        processes_for_save.append(save_data_process)
                for process in concurrent.futures.as_completed(processes_for_save):
                    process.result()
