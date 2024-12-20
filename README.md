# **"Анализатор прайс-листов"**

## **Описание**

Имеется несколько файлов, содержащих прайс-листы от разных поставщиков. Количество и название файлов заранее неизвестно, однако точно известно, что в названии файлов прайс-листов есть слово "price". Файлы, не содержащие слово "price" игнорируются.
Программа загружает данные из всех прайс-листов и предоставляет интерфейс для поиска товара по фрагменту названия с сорторовкой по цене за килогорамм. Интерфейс для поиска реализован через консоль, циклически получая информацию от пользователя.
Если введено слово "exit", то цикл обмена с пользователем завершается, программа выводит сообщение о том, что работа закончена и завершает свою работу. В противном случае введенный текст считается текстом для поиска. Программа выводит список найденных позиций в виде таблицы, список отсортирован по возрастанию стоимости за килограмм.
Предусмотрен вывод массива данных в текстовый файл: output, в формате html.
То есть пользователю достаточно ввести название продукта и он получает полный список этого продукта из всех прайс-листов, отсортированный по возрастанию стоимости.

## **В файле "project.py" реализован полный функционал, основные особенности реализации:**

### **1. Метод "load_prices":**
   - Сканирует директорию и находит файлы со словом "price"
   - Определяет нужные столбцы по их названиям
   - Загружает данные с проверкой корректности
   - Рассчитывает цену за килограмм

### **2. Метод "_search_product_price_weight":**
   - Вспомогательный метод для поиска нужных столбцов. Цель этого метода - найти индексы столбцов для названия,
     цены и веса продукта в данных CSV. Он инициализирует три переменные - product_idx, price_idx и weight_idx - значением -1.
     В них будут храниться индексы столбцов, которые мы ищем. Метод возвращает кортеж, если ни один из них не может быть найден,
     соответствующий индекс будет равен -1, для проверки, были ли найдены нужные столбцы в CSV файле.
     Значение -1 используется как флаг-индикатор.

   - Учитывает все возможные варианты названий. Он преобразует все заголовки столбцов в нижний регистр и удаляет все начальные
     и конечные пробелы. Это повышает надежность сопоставления заголовков. Затем он проверяет заголовки на наличие общих ключевых слов.
     
### **3. Метод "find_text":**
   - Ищет товары по фрагменту названия
   - Сортирует результаты по цене за килограмм
   - Форматирует вывод в виде таблицы

### **4. Метод "export_to_html":**

Создает HTML файл со всеми данными, а если он уже существовал в данной директории, файл будет полностью перезаписан.
После выполнения кода мы получаем обновленный файл output.html, который можно открыть в любом браузере.
Файл будет содержать актуальные данные, отсортированные по цене за килограмм,
с форматированной таблицей и чередующимися цветами строк для удобства чтения.
   - Добавляет базовые стили для таблицы. Базовые стили включают:
     
    - "border-collapse: collapse" - убирает двойные границы между ячейками
    - "width: 100%" - таблица занимает всю ширину страницы
    - "border: 1px solid #ddd" - серые границы ячеек
    - "padding: 8px" - отступы внутри ячеек
    - "background-color: #f2f2f2" - серый фон заголовков
    - "tr:nth-child(even)" - чередующийся цвет строк для лучшей читаемости
    
   - Сортирует данные по цене за килограмм: **"sorted_data = sorted(self.data, key=lambda x: x['price_per_kg'])".**
     
     Где функция сортировки по ключу: **"lambda x: x['price_per_kg']"**
    
   - Формирует таблицы:
     
     **for i, item in enumerate(sorted_data, 1):**
     
     html_content += f'''<tr> <td>{i}</td> <td>{item['name']}</td> <td>{item['price']:.2f}</td> <td>{item['weight']:.1f}
     </td> <td>{item['file']}</td><td>{item['price_per_kg']:.2f}</td></tr>'''.
     
     Где каждый товар добавляется как новая строка таблицы, ":.2f" форматирует числа с двумя знаками после запятой,
     "enumerate(sorted_data, 1)" начинает нумерацию с 1
     

### **5. Основной код программы:**
   - Загружает данные при старте
   - Реализует циклический интерфейс для поиска
   - Обрабатывает команду "exit"

### **Программа обрабатывает возможные ошибки:**
- Отсутствующие файлы
- Некорректные данные в CSV
- Отсутствующие столбцы
- Пустые строки

