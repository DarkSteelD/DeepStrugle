import os
import pandas as pd
import nibabel as nib
import numpy as np
from skimage.draw import ellipse

def create_ellipse_mask_and_modify_image(data, slice_number, center_x, center_y, radius_x, radius_y, flag):
    # Коррекция номера слоя в зависимости от флага
    print(f"Создание маски для слоя {slice_number} с флагом '{flag}'")
    
    print(f"Корректированный номер слоя: {slice_number}")

    # Создание маски в виде элипса
    rr, cc = ellipse(center_y, center_x, r_radius=radius_y, c_radius=radius_x, shape=data.shape[:2])
    mask = np.zeros(data.shape[:2], dtype=bool)
    mask[rr, cc] = 1
    
    # Применение маски к соответствующему слою
    modified_data = data.copy()
    if flag == 'b': 
        modified_data[rr, cc, slice_number-6:slice_number] = 1
    elif flag == 'a':
        modified_data[rr, cc, slice_number:slice_number+6] = 1
     # Поместить маску на слой slice_number
    return modified_data

def find_nifti_file(directory):
    print(f"Поиск NIfTI файла в директории: {directory}")
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.nii') or file.endswith('.nii.gz'):
                print(f"Найден NIfTI файл: {file}")
                return os.path.join(root, file)
    print("NIfTI файл не найден.")
    return None

ods_file_path = os.path.expanduser('~/Downloads/merged_result.ods')
nifti_root_directory = os.path.expanduser('~/Downloads/NIFTI/')

print(f"Путь к ODS файлу: {ods_file_path}")
print(f"Корневая директория NIfTI: {nifti_root_directory}")

try:
    df = pd.read_excel(ods_file_path, engine='odf')
    print("ODS файл успешно прочитан.")
except Exception as e:
    print(f"Ошибка при чтении ODS файла: {e}")
    exit()

for index, row in df.iterrows():
    study_name = row['study']
    folder_path = os.path.join(nifti_root_directory, study_name.strip())
    print(f"Обрабатываем папку: {folder_path}")
    
    nifti_file_path = find_nifti_file(folder_path)
    if nifti_file_path:
        print(f"Обрабатываем файл: {nifti_file_path}")
        nii = nib.load(nifti_file_path)
        data = nii.get_fdata()

        slice_number = int(row['slice'])
        flag = row['flag']
        center_x, center_y = map(float, [row['ROI'],row['F']])
        radius_x, radius_y = map(float, [row['G'], row['H']])
        
        modified_data = create_ellipse_mask_and_modify_image(data, slice_number, center_x, center_y, radius_x, radius_y, flag)
        
        output_filename = f'Modified_{os.path.basename(nifti_file_path)}'
        new_img = nib.Nifti1Image(modified_data, affine=nii.affine)
        output_filepath = os.path.join(folder_path, output_filename)
        nib.save(new_img, output_filepath)
        
        print(f"Измененное изображение сохранено в: {output_filepath}")
    else:
        print(f"Файл NIfTI не найден в папке: {folder_path}")
