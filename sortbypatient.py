import pandas as pd
import os
import shutil

def organize_nifti_files(metadata_csv, nifti_dir, output_dir):
    # Load metadata
    df = pd.read_csv(metadata_csv)
    # Assuming 'slice_path' points to original .h5 files, and can be mapped to new NIFTI
    # and 'BraTS2020_subject_ID' gives us the patient mapping
    for idx, row in df.iterrows():
        subject_id = row['BraTS2020_subject_ID']
        modality_path = row['slice_path'].replace('.h5', '_image.nii')  # Construct NIFTI filename based on original path
        modality_name = 'flair'  # Placeholder: Determine modality from additional logic or data in CSV
        
        source_path = os.path.join(nifti_dir, os.path.basename(modality_path))
        target_dir = os.path.join(output_dir, subject_id, modality_name)
        
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        
        target_path = os.path.join(target_dir, os.path.basename(modality_path))
        
        if os.path.exists(source_path):
            shutil.move(source_path, target_path)
            print(f"Moved {source_path} to {target_path}")
        else:
            print(f"File not found: {source_path}")

# Example usage
organize_nifti_files('~/Documents/GitHub/DeepMedic-Brats2020/archive/BraTS20 Training Metadata.csv', '~/Documents/GitHub/DeepMedic-Brats2020/archive/BraTS2020_training_data/content/data_nii', '~/Documents/GitHub/DeepMedic-Brats2020/archive/BraTS2020_training_data/content/')
