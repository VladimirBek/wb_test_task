### **Тестовое задание для Python разработчика**

Запуск парсера происходит через файл [main.py](https://github.com/VladimirBek/wb_test_task/blob/main/main.py) .

В указанном файле также можно выставить количество воркеров (процессов) и количество страниц для парсинга каждой категории.

По окончанию парсинга, результаты окажутся в папке results в корне проекта, где каждая категория будет сохранена в отдельную категорию, а для каждой стрaницы будет создан отдельный json файл.

Не рекомендуется выставлять больше 10 страниц, так как Wildberries начинает отдавать 429 (Too many requests).
 
Для разработки использовался python3.11, иные зависимости указаны в файле [**requirements.txt**](https://github.com/VladimirBek/wb_test_task/blob/main/requirements.txt) .

**Текст технического задания:**

Цель задания:
Разработать парсер для сайта Wildberries с использованием мультипроцессорности.

Требования:

1) Парсер должен собирать информацию о товарах с главной страницы категории на сайте Wildberries.
2) Информация для сбора: название товара, цена, ссылка на товар.
3) Использовать мультипроцессорность для ускорения процесса парсинга.
4) Реализовать обработку возможных исключений и ошибок.

Технические детали:

- Использовать библиотеку requests для HTTP-запросов.
- Для парсинга HTML-контента использовать BeautifulSoup или аналогичную библиотеку.
- Для мультипроцессорности рекомендуется использовать модуль concurrent.futures.
- Результат парсинга сохранить в формате JSON.


Пример структуры JSON:
``` json
[
    {
        "title": "Название товара 1",
        "price": "1000 руб.",
        "link": "https://www.wildberries.ru/product/1"
    },
    {
        "title": "Название товара 2",
        "price": "2000 руб.",
        "link": "https://www.wildberries.ru/product/2"
    },
    ...
]
```

Критерии оценки:

- Качество кода: читаемость, структура, комментарии.
- Эффективность использования мультипроцессорности.
- Обработка ошибок и исключений.
- Возможность расширения функционала парсера (например, добавление дополнительных полей).

Дополнительные задания (необязательно):

- Реализовать возможность парсинга нескольких страниц категории.
- Добавить логирование процесса парсинга.