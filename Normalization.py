import os
import pandas as pd
import nibabel as nib
from scipy.ndimage import zoom
import numpy as np

print("Начало работы скрипта...")

def resample_image(image_path, new_voxel_size=(1.0, 1.0, 1.0)):
    img = nib.load(image_path)
    data = img.get_fdata()
    header = img.header
    current_voxel_size = header.get_zooms()
    scale_factors = [current/new for current, new in zip(current_voxel_size, new_voxel_size)]
    resampled_data = zoom(data, scale_factors, order=3)
    new_affine = np.dot(img.affine, np.diag([1./s for s in scale_factors] + [1]))
    return nib.Nifti1Image(resampled_data, affine=new_affine)

def determine_modality(file_name):
    if "FLAIR" in file_name.upper():
        return "FLAIR"
    elif "T1C" in file_name.upper() or "T1_CONTRAST" in file_name.upper():
        return "T1c"
    elif "T2" in file_name.upper():
        return "T2"
    else:
        return "Unknown"

ods_file_path = os.path.expanduser('~/Downloads/merged_result.ods')
nifti_root_directory = os.path.expanduser('~/Downloads/NIFTI/')
output_directory = os.path.expanduser('~/Downloads/NIFTI_2/')

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

df = pd.read_excel(ods_file_path, engine='odf')

for index, row in df.iterrows():
    study_name = row['study']
    study_path = os.path.join(nifti_root_directory, study_name)
    output_study_path = os.path.join(output_directory, study_name)
    if not os.path.exists(output_study_path):
        os.makedirs(output_study_path)
    
    for file in os.listdir(study_path):
        if file.endswith('.nii') or file.endswith('.nii.gz'):
            modality = determine_modality(file)  # Определяем модальность файла
            image_path = os.path.join(study_path, file)
            resampled_img = resample_image(image_path)
            # Формируем имя выходного файла с обозначением модальности
            output_filename = f'resampled_{modality}_{file}' if modality != 'Unknown' else f'resampled_{file}'
            resampled_img.to_filename(os.path.join(output_study_path, output_filename))

print("Скрипт завершил работу.")

