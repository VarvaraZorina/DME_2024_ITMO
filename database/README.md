# База данных

В процессе работы была создана база данных PostgreSQL в docker-контейнере, нормализованная по третьей нормальной форме (3НФ).

## 1. Создание таблицы `weather_events`

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

## 2. Заполнение ее данными из CSV

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

```bash
docker cp ..\DME_2024_ITMO\database\dme_backup.sql postgres_db:/dme_backup.sql
```

## 3. Нормализация исходной таблицы по 3НФ

После создания и заполнения таблицы `weather_events`, данные были нормализованы в соответствии с третьей нормальной формой (3НФ). Это включает выделение уникальных событий и регионов в отдельные таблицы.

## 4. Создание новых таблиц

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
    duration INT
);
```

## 5. Заполнение данными

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