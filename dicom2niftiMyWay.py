import os
import pydicom
import nibabel as nib
import numpy as np

def find_dicom_files(directory):
    """
    Рекурсивно ищет все файлы в директории, пытаясь открыть их как DICOM,
    и возвращает список путей к действительным DICOM файлам.
    """
    dicom_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                _ = pydicom.dcmread(file_path, force=True)
                dicom_files.append(file_path)
            except Exception:
                continue
    return dicom_files

def sort_dicom_series(dicom_files):
    """
    Пытается отсортировать серию DICOM файлов. Сначала пытается использовать 'ImagePositionPatient',
    если доступен, иначе пытается использовать 'InstanceNumber'.
    """
    dicom_data = []
    for f in dicom_files:
        try:
            data = pydicom.dcmread(f, force=True)
            dicom_data.append(data)
        except Exception:
            continue  # Пропускаем файлы, которые не могут быть прочитаны как DICOM
    
    # Попытка сортировки по 'ImagePositionPatient', затем по 'InstanceNumber'
    try:
        dicom_data.sort(key=lambda x: (float(x.ImagePositionPatient[2]) if 'ImagePositionPatient' in x else 0,
                                       x.InstanceNumber if 'InstanceNumber' in x else 0))
    except Exception as e:
        print(f"Ошибка сортировки: {e}")
    
    # Возвращаем отсортированный список путей к файлам
    return [x.filename for x in dicom_data if 'filename' in dir(x)]

# Используйте обновленную функцию сортировки в основной части



def dicom_to_nifti(dicom_dir, output_dir, config_file):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    print(f"Создана директория для вывода: {output_dir}")

    config_lines = []
    print(f"Ищем DICOM файлы в: {dicom_dir}")
    
    patient_dirs = [os.path.join(dicom_dir, d) for d in os.listdir(dicom_dir) if os.path.isdir(os.path.join(dicom_dir, d))]
    
    for patient_dir in patient_dirs:
        dicom_files = find_dicom_files(patient_dir)
        
        if not dicom_files:
            print(f"В директории {patient_dir} DICOM файлы не найдены.")
            continue
        
        print(f"Найдено {len(dicom_files)} DICOM файлов в {patient_dir}. Производится обработка...")
        
        try:
            sorted_files = sort_dicom_series(dicom_files)
            if sorted_files:
                dicom_series = [pydicom.dcmread(f) for f in sorted_files]
                volume = np.stack([s.pixel_array for s in dicom_series])

                nifti_filename = os.path.basename(patient_dir) + '.nii'
                nifti_file_path = os.path.join(output_dir, nifti_filename)
                nib.save(nib.Nifti1Image(volume.astype(np.int16), np.eye(4)), nifti_file_path)

                config_lines.append(nifti_file_path + '\n')
                print(f"Файл {nifti_filename} успешно сохранен.")
            else:
                print(f"Не удалось обработать файлы в {patient_dir}: не найдены подходящие DICOM файлы для сортировки.")
        except Exception as e:
            print(f"Ошибка при обработке {patient_dir}: {e}")
    
    with open(config_file, 'w') as f:
        f.writelines(config_lines)
    print(f"Конфигурационный файл сохранен: {config_file}")

dicom_dir = r"C:\CTAG-2"
output_dir = r"C:\NIFTI_2"
config_file = r"C:\Users\DarkStell\Documents\GitHub\DeepStrugle\config_file.cfg"

dicom_to_nifti(dicom_dir, output_dir, config_file)
