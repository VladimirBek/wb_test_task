import concurrent
import os
from concurrent.futures import ProcessPoolExecutor

from core.config import settings


class Runner:
    def __init__(self, parser, request_manager):
        self.parser = parser
        self.request_manager = request_manager

    def get_category_links(self):
        """
          Retrieves the category links from the Wildberries API.
          This function makes a request to the Wildberries API to retrieve the raw category data. It then parses the raw
            category data using the `parse_category_urls` method of the `parser` object. The parsed category links are
            returned as a dictionary.
          Returns:
              dict: A dictionary containing the category links, where the keys are the category names and the values are
               tuples containing the shard identifier and query string.
          """
        with self.request_manager as session:
            if not os.path.exists("results"):
                os.mkdir("results")
            raw_category_data = session.get_request(settings.ROOT_URLS['wildberries'][1]).json()
            category_links = self.parser.parse_category_urls(raw_category_data)
        return category_links

    def get_products(self, cat_name, shard, query, page_num: int, session):
        """
             Retrieves products from a specific category by making multiple requests to the Market.
             Args:
                 cat_name (str): The name of the category.
                 shard (str): The shard identifier.
                 query (str): The query string.
                 page_num (int): The number of pages to retrieve.
                 session (Session): The session object for making API requests.
             Returns:
                 list: A list of lists containing the category name, page number, and products data.
             """
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
        """
        Runs the data collection process for each category.

        This function uses multiprocessing to concurrently collect data from multiple categories.
        It iterates over the category links obtained from the `get_category_links` method and submits
        a `get_products` process for each category to the `ProcessPoolExecutor`. The `get_products`
        process retrieves the products data for the specified category, shard, query, and page range.
        The collected products data is then passed to the `parser.parse_category` method to parse
        and save the data.

        Parameters:
            pages (int, optional): The number of pages to retrieve for each category. Defaults to 1.
            workers (int, optional): The number of worker processes to use for data collection.
                Defaults to 4.

        Returns:
            None
        """
        with self.request_manager as session:  # create session
            with ProcessPoolExecutor(max_workers=workers) as process_executor:  # create process executor
                processes = []  # blank list of processes
                for cat_name, attributes in self.get_category_links().items():
                    if attributes[0] is None or attributes[1] is None:  # check for shard and query in attributes list
                        continue
                    # submit get_data_process for each category
                    get_data_process = process_executor.submit(self.get_products, cat_name=cat_name,
                                                               shard=attributes[0],
                                                               query=attributes[1],
                                                               page_num=pages,
                                                               session=session)
                    processes.append(get_data_process)  # add process to list
                processes_for_save = []
                for process in concurrent.futures.as_completed(processes):  # wait for all processes to complete
                    for cat_name, page, products in process.result():
                        if products is None:
                            continue
                        # submit save_data_process for each result from get_data_process
                        # (futures with json data of products and page number)
                        save_data_process = process_executor.submit(self.parser.parse_category,
                                                                    category_name=cat_name,
                                                                    category_json=products.json(),
                                                                    page_num=page)
                        processes_for_save.append(save_data_process)
                for process in concurrent.futures.as_completed(processes_for_save):
                    # wait for all processes to complete
                    process.result()  # save data
