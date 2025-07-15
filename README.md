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

![Агрегация](images/Снимок экрана 2025-07-15 в 03.05.28.png)

</details>

---

###  Комбинированный запрос

```bash
python main.py --file tests/test_data/products.csv --where "brand=apple" --aggregate "price=min"
```

<details>
<summary>Скриншот вывода</summary>

![Комбинированный запрос](images/Снимок экрана 2025-07-15 в 03.05.40.png)

</details>

---

###  Сортировка

```bash
python main.py --file tests/test_data/products.csv --order-by "price=desc"
```

<details>
<summary>Скриншот вывода</summary>

![Сортировка 1 часть](images/Снимок экрана 2025-07-15 в 03.06.40.png)
![Сортировка 2 часть](images/Снимок экрана 2025-07-15 в 03.06.49.png)
</details>

---

###  Фильтрация + сортировка

```bash
python main.py --file tests/test_data/products.csv --where "brand=samsung" --order-by "rating=asc"
```

<details>
<summary>Скриншот вывода</summary>

![Фильтрация + сортировка](images/Снимок экрана 2025-07-15 в 03.07.04.png)

</details>

---

###  Pytest

```bash
pytest tests/ --cov=src --cov-report=term-missing    
```

<details>
<summary>Скриншот вывода</summary>

![pytest 1 часть](images/Снимок экрана 2025-07-15 в 03.07.23.png)
![pytest 2 часть](images/Снимок экрана 2025-07-15 в 03.07.30.png)
</details>

---

###  Docker

```bash
docker build -t processing-csv .
docker-compose up
```

<details>
<summary>Скриншот вывода</summary>

![docker-compose up](images/Снимок экрана 2025-07-15 в 03.03.36.png)
![docker-compose.yml](images/Снимок экрана 2025-07-15 в 03.04.02.png)
</details>

---

##  Аргументы

| Аргумент      | Описание                                                 |
| ------------- | -------------------------------------------------------- |
| `--file`      | Путь к CSV-файлу                                         |
| `--aggregate` | Агрегация данных по колонке (`avg`, `min`, `max`, `sum`) |
| `--where`     | Фильтрация по значению в колонке (`key=value`)           |

