import os
import pandas as pd
from fuzzywuzzy import process
# Загрузка данных из ODS файлов
combined_path = os.path.expanduser('~/Downloads/combined.ods')
result_1_path = os.path.expanduser('~/Downloads/result_1.ods')

combined_df = pd.read_excel(combined_path, engine='odf')
result_1_df = pd.read_excel(result_1_path, engine='odf')

# Предварительная обработка и нормализация имен исследований, если это необходимо
# Пример: приведение всех имен к верхнему регистру
def find_best_match(name, target_df, threshold=80):
    result = process.extractOne(name, target_df['Study'].tolist())
    if result:
        best_match, best_score = result
        if best_score >= threshold:
            return best_match
    return None

# Загрузка данных
combined_df['normalized_name'] = combined_df['study'].str.upper()
result_1_df['normalized_name'] = result_1_df['Study'].str.upper()

# Применение функции поиска соответствия для каждого имени
combined_df['best_match'] = combined_df['normalized_name'].apply(lambda x: find_best_match(x, result_1_df))

# Объединение DataFrame на основе найденных соответствий
merged_df = pd.merge(combined_df, result_1_df, left_on='best_match', right_on='normalized_name', how='inner')

# Сохранение объединенных данных в новый ODS файл
output_path = os.path.expanduser('~/Downloads/merged_result.ods')
merged_df.to_excel(output_path, index=False, engine='odf')

print("Объединение завершено. Результат сохранен в", output_path)
