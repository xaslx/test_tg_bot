from pathlib import Path
import csv
from datetime import datetime


def save_application(data: dict):
    csv_file = Path('db/applications.csv')
    file_exists = csv_file.exists()
    
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        
        if not file_exists:
            writer.writerow([
                'Дата', 'Имя', 'Телефон', 'Тип дома', 
                'Участок', 'Бюджет', 'Сроки', 'Комментарий'
            ])
            
        writer.writerow([
            datetime.now().strftime('%d.%m.%Y %H:%M:%S'),
            data.get('name', ''),
            data.get('phone', ''),
            data.get('house_type_ru', ''),
            data.get('plot_ru', ''),
            data.get('budget_ru', ''),
            data.get('timing_ru', ''),
            data.get('comment', '')
        ])