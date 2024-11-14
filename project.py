import os
import csv
import json


class PriceMachine():

    def __init__(self):
        self.data = []  # Список для хранения всех данных из прайс-листов
        self.result = ''  # Результат для HTML экспорта
        self.name_length = 0  # Максимальная длина названия для форматирования

    def _search_product_price_weight(self, headers):
        '''
        Возвращает номера столбцов с названием товара, ценой и весом

        Args:
            headers (list): Список заголовков столбцов

        Returns:
            tuple: (индекс_названия, индекс_цены, индекс_веса)
        '''
        product_idx = -1
        price_idx = -1
        weight_idx = -1

        # Приведем заголовки к нижнему регистру для поиска
        headers = [str(h).lower().strip() for h in headers]

        # Ищем индекс названия товара
        product_names = ['название', 'продукт', 'товар', 'наименование']
        for idx, header in enumerate(headers):
            if header in product_names:
                product_idx = idx
                break

        # Ищем индекс цены
        price_names = ['цена', 'розница']
        for idx, header in enumerate(headers):
            if header in price_names:
                price_idx = idx
                break

        # Ищем индекс веса
        weight_names = ['фасовка', 'масса', 'вес']
        for idx, header in enumerate(headers):
            if header in weight_names:
                weight_idx = idx
                break

        return product_idx, price_idx, weight_idx

    def load_prices(self, file_path=''):
        '''
        Сканирует указанный каталог и загружает данные из прайс-листов

        Args:
            file_path (str): Путь к директории с файлами

        Returns:
            list: Список обработанных файлов
        '''
        processed_files = []
        current_dir = file_path if file_path else os.getcwd()

        # Перебираем все файлы в директории
        for filename in os.listdir(current_dir):
            if 'price' in filename.lower() and filename.endswith('.csv'):
                file_path = os.path.join(current_dir, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        csv_reader = csv.reader(file, delimiter=',')
                        headers = next(csv_reader)  # Читаем заголовки

                        # Получаем индексы нужных столбцов
                        prod_idx, price_idx, weight_idx = self._search_product_price_weight(headers)

                        if -1 in (prod_idx, price_idx, weight_idx):
                            print(f"Ошибка: не найдены необходимые столбцы в файле {filename}")
                            continue

                        # Читаем данные
                        for row in csv_reader:
                            if len(row) > max(prod_idx, price_idx, weight_idx):
                                try:
                                    name = row[prod_idx].strip()
                                    if not name:  # Пропускаем пустые строки
                                        continue

                                    price = float(row[price_idx].strip())
                                    weight = float(row[weight_idx].strip())

                                    # Обновляем максимальную длину названия
                                    self.name_length = max(self.name_length, len(name))

                                    # Добавляем данные в общий список
                                    self.data.append({
                                        'name': name,
                                        'price': price,
                                        'weight': weight,
                                        'file': filename,
                                        'price_per_kg': round(price / weight, 2)
                                    })

                                except (ValueError, IndexError) as e:
                                    print(f"Ошибка обработки строки в файле {filename}: {e}")
                                    continue

                        processed_files.append(filename)

                except Exception as e:
                    print(f"Ошибка при обработке файла {filename}: {e}")
                    continue

        return processed_files

    def find_text(self, text):
        '''
        Поиск товаров по фрагменту названия

        Args:
            text (str): Текст для поиска

        Returns:
            list: Отсортированный список найденных товаров
        '''
        if not text:
            return []

        # Ищем товары, содержащие искомый текст
        found_items = [item for item in self.data
                       if text.lower() in item['name'].lower()]

        # Сортируем по цене за килограмм
        found_items.sort(key=lambda x: x['price_per_kg'])

        # Форматируем и выводим результаты
        if found_items:
            print("\n{:<4} {:<30} {:>8} {:>6} {:<12} {:>10}".format(
                "№", "Наименование", "цена", "вес", "файл", "цена за кг."))
            print("-" * 75)

            for i, item in enumerate(found_items, 1):
                print("{:<4} {:<30} {:>8.2f} {:>6.1f} {:<12} {:>10.2f}".format(
                    i,
                    item['name'][:30],
                    item['price'],
                    item['weight'],
                    item['file'],
                    item['price_per_kg']
                ))

        return found_items

    def export_to_html(self, fname='output.html'):
        '''
        Экспортирует все данные в HTML файл

        Args:
            fname (str): Имя выходного файла
        '''
        # Сортируем все данные по цене за килограмм
        sorted_data = sorted(self.data, key=lambda x: x['price_per_kg'])

        html_content = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Позиции продуктов</title>
            <style>
                table { border-collapse: collapse; width: 100%; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
                tr:nth-child(even) { background-color: #f9f9f9; }
            </style>
        </head>
        <body>
            <table>
                <tr>
                    <th>Номер</th>
                    <th>Название</th>
                    <th>Цена</th>
                    <th>Фасовка</th>
                    <th>Файл</th>
                    <th>Цена за кг.</th>
                </tr>
        '''

        for i, item in enumerate(sorted_data, 1):
            html_content += f'''
                <tr>
                    <td>{i}</td>
                    <td>{item['name']}</td>
                    <td>{item['price']:.2f}</td>
                    <td>{item['weight']:.1f}</td>
                    <td>{item['file']}</td>
                    <td>{item['price_per_kg']:.2f}</td>
                </tr>
            '''

        html_content += '''
            </table>
        </body>
        </html>
        '''

        with open(fname, 'w', encoding='utf-8') as f:
            f.write(html_content)

        return html_content


# Основной код программы
if __name__ == "__main__":
    pm = PriceMachine()

    # Загружаем данные
    processed_files = pm.load_prices()
    print(f"Обработано файлов: {len(processed_files)}")

    # Экспортируем данные в HTML
    pm.export_to_html()

    # Основной цикл работы с пользователем
    while True:
        search_text = input("\nВведите текст для поиска (или 'exit' для выхода): ").strip()

        if search_text.lower() == 'exit':
            print("\nРабота программы завершена.")
            break

        found_items = pm.find_text(search_text)
        if not found_items:
            print("Ничего не найдено.")
