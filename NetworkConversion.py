# -*- coding: utf-8 -*-
"""
Created on Thu May  9 14:02:10 2024

@author: micha
"""

import numpy as np
from PIL import Image

#%%
# Load image
image_path = '230Img0.png'
image = Image.open(image_path).convert('L')
width, height = image.size

#%% 
# Convert image to binary
threshold = 128  # Adjust this threshold based on your image
binary_image = np.array(image) >= threshold  # White pixels are now True (atoms)

#%%
# Find coordinates of white pixels (atoms)
y_indices, x_indices = np.nonzero(binary_image)
num_atoms = len(x_indices)
atom_positions = list(zip(x_indices, y_indices))

# Prepare LAMMPS data file
lammps_data = "LAMMPS Description\n\n"
lammps_data += f"{num_atoms} atoms\n"
lammps_data += "1 atom types\n\n"

# Determine bonds
bonds = []
atom_id_map = {pos: idx for idx, pos in enumerate(atom_positions, start=1)}
bond_id = 1

for i, (x, y) in enumerate(atom_positions):
    # Check right (horizontal) and down (vertical) neighbors
    if (x + 1, y) in atom_id_map:  # Horizontal bond
        bonds.append((bond_id, 1, atom_id_map[(x, y)], atom_id_map[(x + 1, y)]))
        bond_id += 1
    if (x, y + 1) in atom_id_map:  # Vertical bond
        bonds.append((bond_id, 2, atom_id_map[(x, y)], atom_id_map[(x, y + 1)]))
        bond_id += 1

num_bonds = len(bonds)
lammps_data += f"{num_bonds} bonds\n"
lammps_data += "2 bond types\n\n"

lammps_data += f"0 {width} xlo xhi\n"
lammps_data += f"0 {height} ylo yhi\n"
lammps_data += "-0.5 0.5 zlo zhi\n\n"

lammps_data += "Masses\n\n"
lammps_data += "1 1.0\n\n"  # Assuming all atoms have mass of 1

lammps_data += "Atoms # molecular\n\n"
for idx, (x, y) in enumerate(atom_positions, start=1):
    lammps_data += f"{idx} 0 1 {x} {y} 0.0\n"  # Atom ID, molecule ID, type, x, y, z

lammps_data += "\nBonds\n\n"
for bond in bonds:
    bond_id, bond_type, atom1, atom2 = bond
    lammps_data += f"{bond_id} {bond_type} {atom1} {atom2}\n"

# Write to file
with open('lammps_data1.txt', 'w') as file:
    file.write(lammps_data)

print("LAMMPS data file created with one atom type and two bond types.")

