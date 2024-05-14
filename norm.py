import nibabel as nib
import numpy as np
import os

def normalize_nifti(input_folder):
    input_folder = os.path.expanduser(input_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('_image.nii'):
            filepath = os.path.join(input_folder, filename)
            nii = nib.load(filepath)
            data = nii.get_fdata()
            
            # Normalizing the data
            mean = np.mean(data[data > 0])  # Mean of non-zero elements, assuming background is zero
            std = np.std(data[data > 0])
            normalized_data = (data - mean) / std
            
            # Save the normalized data back to NIFTI
            normalized_nii = nib.Nifti1Image(normalized_data, nii.affine)
            nib.save(normalized_nii, filepath)
            print(f"Normalized and saved: {filepath}")

# Example usage
normalize_nifti('~/Documents/GitHub/DeepMedic-Brats2020/archive/BraTS2020_training_data/content/data_nii')
