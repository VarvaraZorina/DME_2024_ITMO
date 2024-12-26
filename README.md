Инжиниринг управления данными

# Анализ частоты и интенсивности погодных явлений, ведущих к экономическим потерям в различных регионах РФ

## Описание проекта
Данный проект направлен на анализ данных о погодных явлениях в России с целью выявления их влияния на экономические потери в различных федеральных округах. В проекте используются данные о погоде, которые позволяют оценить частоту и интенсивность различных явлений, а также выявить регионы и временные периоды, подверженные наибольшим рискам экономических убытков.

## Структура проекта
```
DME_2024_ITMO/
├── database/ 
│   ├── backup_file.backup      # Резервная копия базы данных PostgreSQL, созданная для восстановления данных при необходимости.
│   ├── db_connection.py        # Файл для подключения к базе данных PostgreSQL и выполнения SQL-запросов.
│   └── docker-compose.yml      # Конфигурационный файл для запуска контейнеров PostgreSQL и pgAdmin с помощью Docker.
├── images/                     # Папка с графиками, созданными в процессе анализа данных.
│   └── ...                     # Здесь могут находиться изображения графиков, созданных с использованием библиотек визуализации.
├── app.py                      # Основной файл приложения Streamlit, который объединяет все страницы и визуализации.
├── dataset_input.xlsx          # Исходный файл с данными о погодных явлениях в формате Excel.
├── dataset_output.csv          # Выходной файл с обработанными данными в формате CSV, полученными после анализа и очистки исходных данных.
├── dme_project.ipynb           # Jupyter Notebook с кодом обработки и анализа данных, где проводятся эксперименты и визуализации.
└── requirements.txt            # Файл с зависимостями проекта, необходимыми для установки через pip.
```
## Запуск проекта

Шаг 1: Установка необходимых зависимостей

Перед запуском проекта убедитесь, что у вас установлены все необходимые библиотеки. Вы можете установить их, используя файл `requirements.txt`, который содержит список всех зависимостей.

```bash
pip install -r requirements.txt
```

Шаг 2: Запуск контейнеров с базой данных

Проект использует Docker для управления базой данных PostgreSQL. Для запуска контейнеров выполните следующую команду в директории, где находится файл `docker-compose.yml`:

```bash
docker-compose up -d
```

Эта команда создаст и запустит контейнеры PostgreSQL и pgAdmin в фоновом режиме.

Шаг 3: Загрузка данных с помощью резервной копии

```bash
docker cp /path/to/dme_backup.sql postgres_db:/dme_backup.sql
```

После копирования файла выполните следующие команды внутри контейнера PostgreSQL для восстановления базы данных:

```bash
docker exec -it postgres_db pg_restore -U postgres -d pg_db /backup_file.backup
```

Шаг 4: Запуск приложения Streamlit

```bash
streamlit run app.py
```

Это откроет приложение в браузере по адресу `http://localhost:8501`.


## Основные этапы работы
1. **Загрузка данных**: 
2. **Обработка данных**: 
   - Фильтрация и группировка данных по федеральным округам и годам.
   - Вычисление средней интенсивности и продолжительности погодных явлений.
   - Данные загружаются из файла `dataset_input.xlsx`.
   - Визуализация данных:
      - Построение графиков распределения погодных явлений по федеральным округам.
      - Анализ пар явлений, наблюдаемых одновременно.
   - Обработанные данные сохраняются в файл `dataset_output.csv`.
3. **Интеграция с базой данных PostgreSQL**: Данные загружены в базу данных для дальнейшего хранения и обработки.
4. **Подключение к дэшборду**: Streamlit дэшборды, которые отображают графики и визуализации на основе проанализированных данных.

## База данных

В процессе работы была создана база данных PostgreSQL в docker-контейнере, нормализованная по третьей нормальной форме (3НФ).

### 1. Создание таблицы `weather_events`

Для начала была создана таблица `weather_events`, которая содержит информацию о погодных явлениях:

```sql
CREATE TABLE public.weather_events (
    start_date date,
    end_date date,
    event_name character varying(255),
    event_intensity numeric,
    region character varying(255),
    duration integer,
    federal_district character varying(255)
);
```

### 2. Заполнение ее данными из CSV

Данные для таблицы были подготовлены в формате CSV. Пример данных:

```
Start_Date,End_Date,Event_Name,Event_Intensity,Region,Duration,Federal_District
1991-01-01,1991-01-03,Ветер,26.0,Красноярский край,2,Сибирский
1991-01-01,1991-01-03,Метель,50.0,Красноярский край,2,Сибирский
1991-01-03,1991-01-05,Снег,370.0,Сахалинская область,2,Дальневосточный
1991-01-11,1991-01-12,Ветер,27.0,Республика Башкортостан,1,Приволжский
1991-01-13,1991-01-13,Ветер,29.0,Мурманская область,0,Северо-Западный
```

Для загрузки данных из CSV в таблицу `weather_events` можно использовать следующий SQL-запрос:

```csv
COPY public.weather_events (start_date, end_date, event_name, event_intensity, region, duration, federal_district)
FROM '/path/to/your/file.csv' DELIMITER ',' CSV HEADER;
```

### 3. Нормализация исходной таблицы по 3НФ

После создания и заполнения таблицы `weather_events`, данные были нормализованы в соответствии с третьей нормальной формой (3НФ). Это включает выделение уникальных событий и регионов в отдельные таблицы.

### 4. Создание новых таблиц

Созданы новые таблицы для хранения уникальных событий и регионов:

```sql
-- Таблица для уникальных событий
CREATE TABLE public.weather_events_types (
    event_id SERIAL PRIMARY KEY,
    event_name VARCHAR(255) UNIQUE NOT NULL
);

-- Таблица для уникальных регионов
CREATE TABLE public.weather_regions (
    region_id SERIAL PRIMARY KEY,
    region_name VARCHAR(255) UNIQUE NOT NULL,
    federal_district VARCHAR(255) NOT NULL
);

-- Основная таблица для погодных явлений с новым именем
CREATE TABLE public.normalized_weather_events (
    id SERIAL PRIMARY KEY,
    event_id INT REFERENCES public.weather_events_types(event_id),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    event_intensity NUMERIC,
    region_id INT REFERENCES public.weather_regions(region_id)
);
```

### 5. Заполнение данными

После создания новых таблиц данные были перенесены из исходной таблицы `weather_events`:

```sql
INSERT INTO public.weather_events_types (event_name)
SELECT DISTINCT event_name FROM public.weather_events;

INSERT INTO public.weather_regions (region_name, federal_district)
SELECT DISTINCT region AS region_name, federal_district FROM public.weather_events;

INSERT INTO public.normalized_weather_events (event_id, start_date, end_date, event_intensity, duration)
SELECT e.event_id, w.start_date, w.end_date, w.event_intensity, w.duration
FROM public.weather_events w
JOIN public.weather_events_types e ON w.event_name = e.event_name;
```