## ️Использование

###  Фильтрация

```bash
python main.py --file tests/test_data/products.csv --where "price>500"
```

<details>
<summary>Скриншот вывода</summary>

![Фильтрация](https://github.com/averageencoreenjoer/processing-csv/raw/main/images/1.png)

</details>

---

###  Агрегация

```bash
python main.py --file tests/test_data/products.csv --aggregate "rating=avg"
```

<details>
<summary>Скриншот вывода</summary>

![Агрегация](https://github.com/averageencoreenjoer/processing-csv/raw/main/images/2.png)

</details>

---

###  Комбинированный запрос

```bash
python main.py --file tests/test_data/products.csv --where "brand=apple" --aggregate "price=min"
```

<details>
<summary>Скриншот вывода</summary>

![Комбинированный запрос](https://github.com/averageencoreenjoer/processing-csv/raw/main/images/3.png)

</details>

---

###  Сортировка

```bash
python main.py --file tests/test_data/products.csv --order-by "price=desc"
```

<details>
<summary>Скриншот вывода</summary>

![Сортировка 1 часть](https://github.com/averageencoreenjoer/processing-csv/raw/main/images/4.png)
![Сортировка 2 часть](https://github.com/averageencoreenjoer/processing-csv/raw/main/images/5.png)
</details>

---

###  Фильтрация + сортировка

```bash
python main.py --file tests/test_data/products.csv --where "brand=samsung" --order-by "rating=asc"
```

<details>
<summary>Скриншот вывода</summary>

![Фильтрация + сортировка](https://github.com/averageencoreenjoer/processing-csv/raw/main/images/6.png)

</details>

---

###  Pytest

```bash
pytest tests/ --cov=src --cov-report=term-missing    
```

<details>
<summary>Скриншот вывода</summary>

![pytest 1 часть](https://github.com/averageencoreenjoer/processing-csv/raw/main/images/7.png)
![pytest 2 часть](https://github.com/averageencoreenjoer/processing-csv/raw/main/images/8.png)
</details>

---

###  Docker

```bash
docker build -t processing-csv .
docker-compose up
```

<details>
<summary>Скриншот вывода</summary>

![docker-compose up](https://github.com/averageencoreenjoer/processing-csv/raw/main/images/9.png)
![docker-compose.yml](https://github.com/averageencoreenjoer/processing-csv/raw/main/images/10.png)
</details>

---

##  Аргументы

| Аргумент      | Описание                                                 |
| ------------- | -------------------------------------------------------- |
| `--file`      | Путь к CSV-файлу                                         |
| `--aggregate` | Агрегация данных по колонке (`avg`, `min`, `max`, `sum`) |
| `--where`     | Фильтрация по значению в колонке (`key=value`)           |

