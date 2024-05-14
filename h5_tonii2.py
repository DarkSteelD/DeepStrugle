import os
import shutil

def organize_files_for_deepmedic(input_folder, output_base_folder):
    input_folder = os.path.expanduser(input_folder)
    output_base_folder = os.path.expanduser(output_base_folder)
    
    # Ensure the base output folder exists
    if not os.path.exists(output_base_folder):
        os.makedirs(output_base_folder)
        print(f"Created base directory: {output_base_folder}")
    
    # Process each file in the input directory
    for filename in os.listdir(input_folder):
        if filename.endswith('.nii'):
            # Extract patient identifier from the filename
            parts = filename.split('_')
            patient_id = parts[1]  # Assuming the patient ID is always in this position
            patient_folder = os.path.join(output_base_folder, f"patient_{patient_id}")
            
            # Ensure a directory exists for this patient
            if not os.path.exists(patient_folder):
                os.makedirs(patient_folder)
                print(f"Created patient directory: {patient_folder}")
            
            # Move the file to the patient's directory
            src_path = os.path.join(input_folder, filename)
            dst_path = os.path.join(patient_folder, filename)
            shutil.move(src_path, dst_path)
            print(f"Moved {filename} to {patient_folder}")

# Example usage
organize_files_for_deepmedic('~/Documents/GitHub/DeepMedic-Brats2020/archive/BraTS2020_training_data/content/data_nii', '~/Documents/GitHub/DeepMedic-Brats2020/archive/BraTS2020_training_data/content/organized_data')
