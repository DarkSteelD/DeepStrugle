import h5py
import os

def list_datasets_in_h5_file(file_path):
    # Expanding the user home directory symbol
    file_path = os.path.expanduser(file_path)
    
    with h5py.File(file_path, 'r') as file:
        print("Datasets in the .h5 file:")
        for name in file:
            print(name)

# Example usage, replace with an actual file path
list_datasets_in_h5_file('~/Documents/GitHub/DeepMedic-Brats2020/archive/BraTS2020_training_data/content/data/volume_321_slice_99.h5')
