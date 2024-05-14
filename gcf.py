import os

def create_channel_file(input_folder, output_file, modality_suffix):
    input_folder = os.path.expanduser(input_folder)
    output_file = os.path.expanduser(output_file)

    with open(output_file, 'w') as f:
        for patient_folder in sorted(os.listdir(input_folder)):
            if os.path.isdir(os.path.join(input_folder, patient_folder)):
                modality_file = os.path.join(input_folder, patient_folder, f"{modality_suffix}.nii")
                if os.path.exists(modality_file):
                    f.write(modality_file + '\n')
                else:
                    print(f"File not found: {modality_file}")

# Example usage
create_channel_file('~/Documents/GitHub/DeepMedic-Brats2020/archive/BraTS2020_training_data/content/data_nii', './trainChannels_flair.cfg', 'flair')
create_channel_file('~/Documents/GitHub/DeepMedic-Brats2020/archive/BraTS2020_training_data/content/data_nii', './trainChannels_t1ce.cfg', 't1ce')
create_channel_file('~/Documents/GitHub/DeepMedic-Brats2020/archive/BraTS2020_training_data/content/data_nii', './trainChannels_t1.cfg', 't1')
create_channel_file('~/Documents/GitHub/DeepMedic-Brats2020/archive/BraTS2020_training_data/content/data_nii', './trainChannels_t2.cfg', 't2')
create_channel_file('~/Documents/GitHub/DeepMedic-Brats2020/archive/BraTS2020_training_data/content/data_nii', './trainGtLabels.cfg', 'seg')
