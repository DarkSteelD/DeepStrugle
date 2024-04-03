import os
import pandas as pd
import nibabel as nib
from scipy.ndimage import zoom
from skimage.draw import ellipse
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

def normalize_intensity(image_path, mask_path):
    image = nib.load(image_path)
    mask = nib.load(mask_path)
    image_data = image.get_fdata()
    mask_data = mask.get_fdata()
    
    masked_image = np.where(mask_data>0, image_data, np.nan)
    mean = np.nanmean(masked_image)
    std = np.nanstd(masked_image)
    
    normalized_image = np.where(mask_data>0, (image_data - mean) / std, image_data)
    return nib.Nifti1Image(normalized_image, affine=image.affine)

def reindex_labels(labels_path):
    labels_img = nib.load(labels_path)
    labels_data = labels_img.get_fdata()
    
    unique_labels = np.unique(labels_data)
    reindexed_labels = np.zeros_like(labels_data)
    for i, label in enumerate(unique_labels):
        reindexed_labels[labels_data == label] = i
        
    return nib.Nifti1Image(reindexed_labels, affine=labels_img.affine)

ods_file_path = os.path.expanduser('~/Downloads/merged_result.ods')
nifti_root_directory = os.path.expanduser('~/Downloads/NIFTI/')
output_directory = os.path.expanduser('~/Downloads/NIFTI_2/')

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

df = pd.read_excel(ods_file_path, engine='odf')
print("Скрипт завершил работу.")
for index, row in df.iterrows():
    study_name = row['study']
    study_path = os.path.join(nifti_root_directory, study_name)
    output_study_path = os.path.join(output_directory, study_name)
    if not os.path.exists(output_study_path):
        os.makedirs(output_study_path)
    print(f"Processing study: {study_name}")
    found_files = False
    for file in os.listdir(study_path):
        print(f"Found and will process file: {file}")

        if file.endswith('.nii') or file.endswith('.nii.gz'):
            # Resample Image
            print(f"Found and will process file: {file}")
            image_path = os.path.join(study_path, file)
            resampled_img = resample_image(image_path)
            resampled_img.to_filename(os.path.join(output_study_path, 'resampled_' + file))
            
            # Normalize intensity within ROI, assuming ROI file matches 'roi_' prefix
            if 'roi_' in file:
                normalized_img = normalize_intensity(image_path, os.path.join(study_path, file))
                normalized_img.to_filename(os.path.join(output_study_path, 'normalized_' + file.replace('roi_', '')))
            
            # Reindex labels, assuming label file matches 'labels_' prefix
            if 'labels_' in file:
                reindexed_labels_img = reindex_labels(os.path.join(study_path, file))
                reindexed_labels_img.to_filename(os.path.join(output_study_path, 'reindexed_' + file.replace('labels_', '')))
    if not found_files:
        print(f"No suitable files found in {study_path}")
    print(f"Processed study: {study_name}")
