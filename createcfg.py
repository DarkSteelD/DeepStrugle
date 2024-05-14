import os
import shutil
import random

def create_config_files(base_dir, output_dir, validation_split=0.2):
    base_dir = os.path.expanduser(base_dir)
    output_dir = os.path.expanduser(output_dir)
    
    train_dir = os.path.join(output_dir, 'train')
    val_dir = os.path.join(output_dir, 'val')

    # Create train and validation directories if they don't exist
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(val_dir, exist_ok=True)

    modalities = ['flair', 't1', 't1ce', 't2']
    patients = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]

    print(f"Found {len(patients)} patients in the dataset.")

    # Shuffle and split patients into training and validation sets
    random.shuffle(patients)
    split_index = int(len(patients) * (1 - validation_split))
    train_patients = patients[:split_index]
    val_patients = patients[split_index:]

    print(f"Split dataset into {len(train_patients)} training patients and {len(val_patients)} validation patients.")

    def copy_files(patients, set_dir, set_name):
        for patient in patients:
            patient_dir = os.path.join(base_dir, patient)
            target_dir = os.path.join(set_dir, patient)
            os.makedirs(target_dir, exist_ok=True)
            print(f"Copying {set_name} files for patient {patient} to {target_dir}")
            for modality in modalities:
                nii_file = f"{patient}_{modality}.nii"
                src_file = os.path.join(patient_dir, nii_file)
                if os.path.exists(src_file):
                    shutil.copy(src_file, target_dir)
                    print(f"Copied {src_file} to {target_dir}")
                else:
                    print(f"File not found: {src_file}")
            seg_file = f"{patient}_seg.nii"
            src_seg_file = os.path.join(patient_dir, seg_file)
            if os.path.exists(src_seg_file):
                shutil.copy(src_seg_file, target_dir)
                print(f"Copied {src_seg_file} to {target_dir}")
            else:
                print(f"Segmentation file not found: {src_seg_file}")
            roi_file = f"{patient}_roi.nii"
            src_roi_file = os.path.join(patient_dir, roi_file)
            if os.path.exists(src_roi_file):
                shutil.copy(src_roi_file, target_dir)
                print(f"Copied {src_roi_file} to {target_dir}")
            else:
                print(f"ROI mask file not found: {src_roi_file}")

    def write_config_files(set_dir, set_name):
        for modality in modalities:
            config_path = os.path.join(output_dir, f"{set_name}Channels_{modality}.cfg")
            with open(config_path, 'w') as f:
                for patient in os.listdir(set_dir):
                    nii_file = os.path.join(set_dir, patient, f"{patient}_{modality}.nii")
                    if os.path.exists(nii_file):
                        f.write(nii_file + '\n')
                    else:
                        print(f"File not found: {nii_file}")
            print(f"Written {set_name} configuration file for {modality} at {config_path}")

        gt_config_path = os.path.join(output_dir, f"{set_name}GtLabels.cfg")
        with open(gt_config_path, 'w') as f:
            for patient in os.listdir(set_dir):
                seg_file = os.path.join(set_dir, patient, f"{patient}_seg.nii")
                if os.path.exists(seg_file):
                    f.write(seg_file + '\n')
                else:
                    print(f"Segmentation file not found: {seg_file}")
        print(f"Written {set_name} ground truth configuration file at {gt_config_path}")

        roi_config_path = os.path.join(output_dir, f"{set_name}RoiMasks.cfg")
        with open(roi_config_path, 'w') as f:
            for patient in os.listdir(set_dir):
                roi_file = os.path.join(set_dir, patient, f"{patient}_roi.nii")
                if os.path.exists(roi_file):
                    f.write(roi_file + '\n')
                else:
                    print(f"ROI mask file not found: {roi_file}")
        print(f"Written {set_name} ROI masks configuration file at {roi_config_path}")

    # Copy files to train and validation directories
    copy_files(train_patients, train_dir, 'train')
    copy_files(val_patients, val_dir, 'val')

    # Create configuration files
    write_config_files(train_dir, 'train')
    write_config_files(val_dir, 'val')

    print("Configuration files and directories created successfully.")

# Example usage
create_config_files('~/Documents/GitHub/DeepMedic-Brats2020/BraTS2020_TrainingData/MICCAI_BraTS2020_TrainingData', '~/Documents/GitHub/DeepMedic-Brats2020/Configs')

