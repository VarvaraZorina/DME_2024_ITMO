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

**Шаг 1:** Установка необходимых зависимостей

Перед запуском проекта убедитесь, что у вас установлены все необходимые библиотеки. Вы можете установить их, используя файл `requirements.txt`, который содержит список всех зависимостей.

```bash
pip install -r requirements.txt
```

**Шаг 2:** Запуск контейнеров с базой данных

Проект использует Docker для управления базой данных PostgreSQL. Для запуска контейнеров выполните следующую команду в директории, где находится файл `docker-compose.yml`:

```bash
docker-compose up -d
```

Эта команда создаст и запустит контейнеры PostgreSQL и pgAdmin в фоновом режиме.

**Шаг 3:** Загрузка данных с помощью резервной копии

```bash
docker cp /path/to/dme_backup.sql postgres_db:/dme_backup.sql
```

После копирования файла выполните следующие команды внутри контейнера PostgreSQL для восстановления базы данных:

```bash
docker exec -it postgres_db pg_restore -U postgres -d pg_db /backup_file.backup
```

**Шаг 4:** Запуск приложения Streamlit

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

# Отчет

## Часть 1

### 1.Введение

#### 1.1 Цель проекта

<h4>
    Данный проект направлен на анализ данных о погодных явлениях в Роcсии с целью выявления их влияния на экономические потери в различных федеральных округах. В проекте используются данные о погоде, которые позволяют оценить частоту и интенсивность различных явлений, а также выявить регионы и временные периоды, подверженные наибольшим рискам экономических убытков.
</h4>

#### 1.2 Задачи проекта

1. Сбор данных о неблагоприятных погодных явлениях, ведущих к экономическим потерям.

2. Предобработка данных: очистка, нормализация и устранение выбросов.

3. Проведение исследовательского анализа данных (EDA) для выявления закономерностей и взаимосвязей.

4. Определение регионов и временных периодов с наибольшими рисками.

5. Подготовка промежуточных и финальных выводов, а также рекомендаций.

### 2.Выбор задачи и данных

#### 2.1 Выбор задачи

Анализ влияния неблагоприятных погодных явлений на экономические риски является актуальной задачей, поскольку данные явления оказывают значительное влияние на инфраструктуру, сельское хозяйство, транспорт и другие сферы экономики. В рамках проекта мы сосредоточились на оценке:

- Частоты возникновения погодных явлений;

- Интенсивности и продолжительности явлений;

- Географической распределенности явлений.

#### 2.2 Выбор данных

Для анализа использовался массив данных о неблагоприятных погодных явлениях, доступный на сайте ВНИИГМИ-МЦД (Всероссийский научно-исследовательский институт гидрометеорологической информации – Мировой центр данных). Данные включают сведения о явлениях, наблюдавшихся на территории субъектов Российской Федерации, за период с 1991 по 2023 годы.

Каждая запись в массиве данных содержит следующую информацию:

1. Порядковый номер явления.

2. Дата начала и окончания явления.

3. Количество опасных явлений.

4. Заблаговременность предупреждения.

5. Название явления.

6. Интенсивность явления.

7. Субъект Российской Федерации.

8. Дополнительная информация о территории.

### 3 Сбор и предобработка данных

#### 3.1 Сбор данных

Данные были загружены с официального сайта ВНИИГМИ-МЦД. Работа с данными велась в Google Colab.

#### 3.2 Обработка данных

1. Загрузка данных: данные загружаются из файла ``dataset_input.xlsx``.

2. Обработка данных:

- Фильтрация и группировка данных по федеральным округам и годам.

- Вычисление средней интенсивности и продолжительности погодных явлений.

3. Визуализация данных:

- Построение графиков распределения погодных явлений по федеральным округам.

- Анализ пар явлений, наблюдаемых одновременно.
  
4. Экспортданных:обработанные данные сохраняются в файл ``dataset_output.csv``.

### 4.Исследовательский анализ данных (EDA)

#### 4.1 Знакомство с данными

Набор данных состоит из 3 категориальных, 2 временных и 2 числовых признаков.

Это включает в себя такие параметры, как ``Event_Name`` (например, "Ветер", "Метель", "Снег"), ``Region`` (например, "Красноярский край", "Сахалинская область"), ``Federal_District``(например, "Сибирский", "Дальневосточный"), ``Start_Date`` и ``End_Date``, которые представляют собой даты начала и конца события, а также ``Event_Intensity`` и ``Duration``, которые являются числовыми признаками, отражающими интенсивность и продолжительность события соответственно.

#### 4.2 Числовые признаки

**4.2.1 Распределение и статистические характеристики**

Таблица 1 - Распределение и статистические характеристики

| Параметр          | Event_Intensity         | Duration               |
|-------------------|-------------------------|------------------------|
| Среднее значение   | 58.39                   | 2.16                   |
| Стандартное отклонение | 118.94              | 8.44                   |
| Минимальное значение | -65                   | 0                      |
| Максимальное значение | 1244                 | 367                    |
| 25-й процентиль   | 25                      | 0                      |
| Медиана           | 31                      | 1                      |
| 75-й процентиль   | 50                      | 2                      |

``Event_Intensity`` имеет очень большое стандартное отклонение, что указывает на сильную дисперсию данных. Это может быть связано с наличием экстремальных значений (максимальное значение 1244).

``Duration`` также имеет значительное стандартное отклонение, что говорит о вариативности продолжительности событий.

Медиана ``Event_Intensity`` (31) значительно ниже среднего значения (58.39), что может указывать на асимметрию распределения из-за экстремальных значений.

Для ``Duration`` медиана (1) близка к среднему значению (2.16), что говорит о более симметричном распределении.

<p align="center">
<img width="677" alt="Снимок экрана 2024-12-26 в 14 05 50" src="https://github.com/user-attachments/assets/3f5c6555-ad16-4100-9bb2-b295487e16a1" />
</p>
<p align="center">
Рис.1 - Графики плотности распределений для числовых признаков
</p>

**4.2.2 Выбросы**

Для выявления выбросов в числовых признаках были построены графики ``boxplots``. Эти графики показывают, что в данных присутствуют выбросы, особенно в столбце ``Event_Intensity``, что может указывать на экстремальные значения интенсивности событий.

<p align="center">
<img width="677" alt="Снимок экрана 2024-12-26 в 14 05 30" src="https://github.com/user-attachments/assets/7cf2e5c6-de80-4a93-a69c-c0cd8822b6bb" />
</p>
<p align="center">
Рис.2 - Графики выбросов в числовых признаках
</p>

**4.2.3 Ковариация**

Ковариация между числовыми признаками ``94.897204``. Это означает, что существует положительная связь между интенсивностью событий ``Event_Intensity`` и их продолжительностью ``Duration``. Когда интенсивность событий увеличивается, продолжительность также, как правило, увеличивается. Однако величина ковариации относительно небольшая по сравнению с дисперсией каждой переменной, что указывает на то, что связь между ними не очень сильна.

Таблица 2 - Ковариация числовых признаков

| Параметр          | Значение        |
|-------------------|-----------------|
| EventIntensity   | 14146.32        |
| EventIntensity   | 94.90           |
| Duration          | 94.90           |
| Duration          | 71.17           |

#### 4.3 Временные признаки

Набор данных содержит два временных признака: ``Start_Date`` и ``End_Date``, которые представляют собой даты начала и конца погодных явлений соответственно.

**4.3.1 Распределение и статистические характеристики**

Таблица 3 - Распределение и статистические характеристики

| Параметр            | StartDate                       | EndDate                         |
|---------------------|----------------------------------|----------------------------------|
| Среднее значение     | 2009-04-20 20:45:59              | 2009-04-23 00:39:43             |
| Минимальное значение | 1991-01-01 00:00:00              | 1991-01-03 00:00:00             |
| 25-й процентиль     | 2002-06-30 00:00:00              | 2002-06-30 06:00:00             |
| Медиана             | 2010-03-18 00:00:00              | 2010-03-19 00:00:00             |
| 75-й процентиль     | 2016-12-09 00:00:00              | 2016-12-10 18:00:00             |
| Максимальное значение| 2023-12-31 00:00:00              | 2024-01-08 00:00:00             |

Период наблюдения: 

Данные охватывают период с 1991 по 2024 год, что позволяет анализировать долгосрочные тенденции и закономерности в погодных явлениях.

Сезонные тренды:

Квартили и медиана указывают на то, что большинство событий происходит в весенне-летний период, что может быть связано с природными циклами и сезонными изменениями в погоде.

Распределение дат: 

Даты начала и конца событий имеют схожие статистические характеристики, что говорит о том, что продолжительность событий относительно коротка и не сильно варьируется.

#### 4.4 Категориальные признаки

Набор данных содержит три категориальных признака: ``Event_Name``, ``Region`` и ``Federal_District``. Эти признаки представляют собой название погодного явления, регион и федеральный округ соответственно.

**4.4.1 Распределение и статистические характеристики**

``Event_Name``:

Количество уникальных значений: 27.

Наиболее частое значение: "Ветер" (встречается 3239 раз).

``Region``:

Количество уникальных значений: 82.

Наиболее частое значение: "Краснодарский край" (встречается 490 раз).

``Federal_District``:

Количество уникальных значений: 8.

Наиболее частое значение: "Сибирский" (встречается 2533 раза).

``Event_Name``: 

Наиболее распространенным типом погодного явления является "Ветер", что может указывать на то, что ветер является наиболее частым или значимым погодным явлением в данных.

``Region``: 

Краснодарский край является наиболее часто встречающимся регионом, что может быть связано с географическими особенностями или частотой погодных явлений в этом регионе.

``Federal_District``:

Сибирский федеральный округ является наиболее представленным, что может быть связано с его большим размером или географическим положением.

#### 4.5 Корреляция

**4.5.1 Корреляция Пирсона**

<p align="center">
<img width="459" alt="Снимок экрана 2024-12-26 в 14 03 44" src="https://github.com/user-attachments/assets/756ad709-d2be-406e-9362-2ddc52edd513" />
</p>
<p align="center">
Рис.3 - Тепловая карта корреляции Пирсона
</p>

*Корреляция Пирсона используется для оценки линейной связи между переменными.*

Результаты корреляции Пирсона показывают:

Сильная положительная корреляция между ``Start_Date`` и ``End_Date`` (0.999985), что ожидаемо, поскольку эти даты тесно связаны.

Слабая положительная корреляция между ``Event_Intensity`` и ``Duration`` (0.094575), что указывает на то, что более интенсивные события могут иметь слегка большую продолжительность.

Слабая отрицательная корреляция между ``Event_Name`` и ``Event_Intensity`` (-0.095480), что может указывать на то, что некоторые типы событий имеют тенденцию быть менее интенсивными.

**4.5.2 Корреляция Спирмена**

<p align="center">
<img width="459" alt="Снимок экрана 2024-12-26 в 14 02 49" src="https://github.com/user-attachments/assets/ac188b8e-fa8a-4d20-836e-b485a223361a" />
</p>
<p align="center">
Рис.4 - Тепловая карта корреляции Спирмена
</p>

*Корреляция Спирмена используется для оценки монотонной связи между переменными.*

Результаты корреляции Спирмена показывают:

Сильная положительная корреляция между ``Event_Name`` и ``Event_Intensity`` (0.347744), что указывает на то, что определенные типы событий имеют тенденцию быть более интенсивными.

Слабая отрицательная корреляция между ``Event_Intensity`` и ``Duration`` (-0.097664), что может указывать на то, что более интенсивные события не обязательно имеют большую продолжительность.

**4.5.3 Phik**

<p align="center">
<img width="459" alt="Снимок экрана 2024-12-26 в 14 01 51" src="https://github.com/user-attachments/assets/34dcbeef-45aa-458d-900e-e42d01d4dae7" />
</p>
<p align="center">
Рис. 5 - Тепловая карта Phik
</p>

*Phik — это метрика корреляции, которая может обнаруживать нелинейные связи.*

Результаты Phik показывают:

Очень сильная положительная корреляция между ``Start_Date`` и ``End_Date`` (1.000000), что ожидаемо, поскольку эти даты тесно связаны.

Сильная положительная корреляция между ``Event_Name`` и ``Event_Intensity`` (0.785173), что указывает на то, что определенные типы событий имеют тенденцию быть более интенсивными.

Сильная положительная корреляция между ``Region`` и ``Federal_District`` (1.000000), что ожидаемо, поскольку эти признаки тесно связаны.

**4.5.4 Выводы**

**Линейная связь**: Корреляция Пирсона показывает слабую связь между интенсивностью и продолжительностью событий, что может указывать на то, что более интенсивные события не обязательно имеют большую продолжительность.

**Монотонная связь**: Корреляция Спирмена выявляет более сильную связь между типом события и его интенсивностью, что может быть полезно для прогнозирования.

**Нелинейная связь**: Phik показывает очень сильную связь между датами начала и конца событий, что ожидаемо, а также сильную связь между типом события и его интенсивностью.

#### 4.6 Анализ средней интенсивности и продолжительности погодных явлений по федеральным округам

Цель анализа: Оценить как интенсивность, так и продолжительность погодных явлений в различных федеральных округах России.

Для анализа средней интенсивности и продолжительности погодных явлений были использованы следующие шаги:
Группировка данных: Данные были сгруппированы по названиям событий (``Event_Name``) и федеральным округам (``Federal_District``).

Расчет средней интенсивности и продолжительности: Для каждой группы была рассчитана средняя интенсивность (``Event_Intensity``) и продолжительность (``Duration``) событий.

Выводы:

Региональные различия: Средняя продолжительность событий значительно варьируется между федеральными округами. Например, аномально-жаркая погода имеет самую большую среднюю продолжительность в Центральном округе (26.65 дней), а в Дальневосточном округе она составляет всего 6.75 дней.

Тип события: Различные типы событий имеют разную среднюю продолжительность. Например, метель имеет относительно большую продолжительность в Сибирском округе (1.33 дня), а в Северо-Западном округе она составляет 0.60 дня.

Сезонные тренды: Данные могут указывать на сезонные тренды в продолжительности событий, что может быть связано с природными циклами и географическими особенностями регионов.

#### 4.7 Анализ экономических рисков от погодных явлений по федеральным округам и временным периодам

Цель анализа: Оценить влияние погодных явлений на различные федеральные округа России и выявить регионы с повышенными рисками.

Для анализа экономических рисков от погодных явлений по федеральным округам и временным периодам были использованы следующие шаги:

Группировка данных: Данные были сгруппированы по федеральным округам (``Federal_District``) и годам (``Year``).

Расчет количества событий: Для каждой группы была подсчитана общая частота погодных явлений (``Event_Count``).

Определение регионов с высоким риском: Регионы с количеством событий выше среднего были определены как имеющие высокий риск.

Результаты анализа показывают, что некоторые федеральные округа демонстрируют более высокую частоту погодных явлений в определенные годы, что может указывать на повышенные экономические риски.

Регионы с высоким риском:

1. Дальневосточный округ: В 2005, 2009, 2018 и 2023 годах количество событий было выше среднего, что может указывать на повышенную частоту погодных явлений в эти годы.

2. Приволжский округ: В 1998, 2007, 2010 и 2015 годах наблюдалось увеличение количества событий, что может быть связано с географическими особенностями или климатическими условиями.

3. Северо-Кавказский округ: В 2004, 2012 и 2023 годах количество событий было выше среднего, что может быть связано с природными условиями или географическим положением.

4. Сибирский округ: В 1993, 1998, 2005 и 2015 годах наблюдалось значительное увеличение количества событий, что может быть связано с климатическими условиями или географическими особенностями.

5. Центральный округ: В 1991 и 2010 годах количество событий было выше среднего, что может быть связано с погодными условиями или экономической активностью.

6. Южный округ: В 2016 и 2021 годах наблюдалось увеличение количества событий, что может быть связано с климатическими изменениями или региональными особенностями.

Выводы:

Региональные различия: Различные федеральные округа демонстрируют разную частоту погодных явлений в зависимости от года, что может быть связано с географическими, климатическими или экономическими факторами.

Сезонные тренды: Данные могут указывать на сезонные тренды в частоте событий, что может быть связано с природными циклами или региональными особенностями.
Экономические риски: Регионы с высоким риском могут требовать дополнительных мер по управлению рисками и подготовке к потенциальным последствиям погодных явлений.

#### 4.8 Определение пар явлений, которые чаще всего наблюдаются одновременно

Цель анализа: Выявить сочетания погодных явлений, которые происходят одновременно, что может быть полезно для оценки рисков и подготовки к потенциальным последствиям.

Для определения пар явлений, которые чаще всего наблюдаются одновременно, были использованы следующие шаги:

Группировка данных: Данные были сгруппированы по дате начала (``Start_Date``), собирая все названия событий, которые произошли в один и тот же день.
Поиск пар явлений: Для каждой даты были созданы все возможные пары из уникальных названий событий.

Подсчет частоты пар: Был подсчитан общий счет каждой пары, что позволило определить, какие сочетания погодных явлений наблюдаются чаще всего.

Результаты анализа показывают, что наиболее частые пары погодных явлений включают:

- Ветер и Дождь: 264 раза.

- Ветер и Метель: 252 раза.

- Ветер и Град: 230 раз.

- Дождь и Ливень: 189 раз.

- Град и Дождь: 170 раз.

Выводы:

Частые пары: Наиболее частые пары включают "Ветер" и "Дождь", что может указывать на то, что эти явления часто происходят одновременно.

Региональные различия: Данные могут указывать на региональные различия в частоте пар событий, что может быть связано с географическими или климатическими особенностями.

Экономические риски: Выявление частых пар событий может помочь в оценке экономических рисков и подготовке к потенциальным последствиям, особенно в регионах с высокой частотой таких пар.

### 5. Промежуточные и финальные выводы**

#### 5.1 Промежуточные выводы

На основе проведенного анализа можно выделить следующие наблюдения:

- Региональные риски: регионы, наиболее подверженные экстремальным погодным явлениям, включают Сибирь, Урал и Северный Кавказ. Эти регионы демонстрируют высокую частоту явлений, таких как сильные ветры, изменения температуры и осадки.

- Средняя продолжительность явлений может значительно различаться между федеральными округами, что важно для оценки потенциальных экономических потерь.

- Временные риски: погодные явления чаще всего происходят в зимние месяцы, но лето также связано с определенными рисками из-за высокой интенсивности явлений. Построенные распределения по годам показывают, что наиболее рискованные периоды связаны с резкими изменениями температуры и осадками в зимнее время.

#### 5.2 Финальные выводы и рекомендации

Рекомендации:
    
- Для снижения экономических потерь рекомендуется усилить системы предупреждения о экстремальных погодных явлениях, особенно в регионах с высоким риском, таких как Сибирь и Северный Кавказ.
  
- Анализ сочетаний явлений, которые часто наблюдаются одновременно, позволит улучшить целенаправленные меры для уменьшения ущерба, особенно в уязвимых регионах.

## Часть 2

### 6. База данных

В процессе работы была создана база данных PostgreSQL в docker-контейнере, нормализованная по третьей нормальной форме (3НФ).

#### 6.1 Создание таблицы `weather_events`

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

#### 6.2 Заполнение ее данными из CSV

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

#### 6.3 Нормализация исходной таблицы по 3НФ

После создания и заполнения таблицы `weather_events`, данные были нормализованы в соответствии с третьей нормальной формой (3НФ). Это включает выделение уникальных событий и регионов в отдельные таблицы.

#### 6.4 Создание новых таблиц

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

-- Основная таблица для погодных явлений
CREATE TABLE public.normalized_weather_events (
    id SERIAL PRIMARY KEY,
    event_id INT REFERENCES public.weather_events_types(event_id),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    event_intensity NUMERIC,
    region_id INT REFERENCES public.weather_regions(region_id)
);
```

#### 6.5 Заполнение данными

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

### 7. Дэшборды

#### 7.1 Общие показатели

Дэшборд "Общие показатели" предоставляет пользователям возможность анализа погодных явлений в целом, а не только тех, которые приводят к экономическим потерям.

- **Выбор события**: Пользователи могут выбрать конкретное погодное явление из выпадающего списка.
- **Выбор года**: Доступен выбор года, чтобы сосредоточиться на данных за определенный период.
- **Максимальная и минимальная интенсивность**: На странице отображаются максимальные и минимальные значения интенсивности и продолжительности выбранного события.
- **График зависимости**: Визуализируется зависимость между интенсивностью и продолжительностью событий с помощью пузырьковой диаграммы, где размер пузырька соответствует интенсивности.

![ScreenRecorderProject21-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/7a6b3f63-ca51-4c53-897f-ee572a6fa628)

#### 7.2 Федеральные округа

Дэшборд "Федеральные округа" позволяет пользователям анализировать данные о погодных явлениях по федеральным округам.

- **Выбор погодного явления**: Пользователи могут выбрать конкретное явление для анализа.
- **График средней интенсивности**: Отображается график средней интенсивности выбранного события по федеральным округам.
- **Таблица данных**: Отображается таблица с данными о погодных явлениях, отсортированная по дате начала, без столбца региона.
- **График распределения событий**: Пользователи могут видеть распределение погодных явлений по годам для выбранного федерального округа.
- **Кольцевая диаграмма**: Визуализация распределения событий по типам в виде кольцевой диаграммы.

![ScreenRecorderProject22-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/bd892dc6-e0c2-49e9-b72d-4201bf2026db)

#### 7.3 Регионы

Дэшборд "Регионы" предоставляет возможность анализа данных о погодных явлениях на уровне регионов.

- **Выбор погодного явления**: Как и на странице федеральных округов, пользователи могут выбрать конкретное явление для анализа.
- **График средней интенсивности**: Отображается график средней интенсивности выбранного события по регионам.
- **Таблица данных**: Представляет собой таблицу с данными о погодных явлениях, отсортированную по дате начала, без столбца федерального округа.
- **График распределения событий**: Аналогично предыдущим страницам, пользователи могут видеть распределение погодных явлений по годам для выбранного региона.
- **Кольцевая диаграмма**: Визуализация распределения событий по типам в виде кольцевой диаграммы.

![ScreenRecorderProject23-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/4d71aa4a-4d60-4620-bad0-483e232b3a71)
