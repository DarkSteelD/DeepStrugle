import h5py
import numpy as np
import nibabel as nib
import os

def h5_to_nifti(input_folder, output_folder):
    # Expanding the user home directory symbol
    input_folder = os.path.expanduser(input_folder)
    output_folder = os.path.expanduser(output_folder)

    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output directory: {output_folder}")

    # Process each .h5 file in the input directory
    for filename in os.listdir(input_folder):
        if filename.endswith('.h5'):
            file_path = os.path.join(input_folder, filename)
            print(f"Processing file: {file_path}")

            try:
                with h5py.File(file_path, 'r') as h5_file:
                    # Accessing the 'image' and 'mask' datasets
                    if 'image' in h5_file and 'mask' in h5_file:
                        image_data = h5_file['image'][:]
                        mask_data = h5_file['mask'][:]
                        print(f"Successfully read datasets from {filename}")
                    else:
                        print(f"Datasets 'image' or 'mask' not found in {filename}")
                        continue

                # Creating NIFTI files from the numpy arrays
                image_nifti = nib.Nifti1Image(image_data, np.eye(4))  # Using an identity matrix for the affine
                mask_nifti = nib.Nifti1Image(mask_data, np.eye(4))    # Using an identity matrix for the affine
                
                # Saving NIFTI files, distinguishing images and masks
                image_nifti_path = os.path.join(output_folder, filename.replace('.h5', '_image.nii'))
                mask_nifti_path = os.path.join(output_folder, filename.replace('.h5', '_mask.nii'))
                
                nib.save(image_nifti, image_nifti_path)
                nib.save(mask_nifti, mask_nifti_path)

                print(f"Saved NIFTI files: {image_nifti_path} and {mask_nifti_path}")
            
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

# Example usage
h5_to_nifti('~/Documents/GitHub/DeepMedic-Brats2020/archive/BraTS2020_training_data/content/data', '~/Documents/GitHub/DeepMedic-Brats2020/archive/BraTS2020_training_data/content/data_nii')
