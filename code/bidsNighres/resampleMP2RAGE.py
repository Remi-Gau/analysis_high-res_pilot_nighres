from nilearn.image import resample_img
from rescale_affine import rescale_affine
import numpy as np
import nibabel as nb

img = "/Users/barilari/Desktop/sub-pilot001_ses-001_acq-r0p75_UNIT1.nii"

# RESAMPLE INV2 TOO

resampling_factor = 2

nii = nb.load(img)

dimensions = nii.header.get_data_shape()
print(np.multiply(dimensions, 2))

vox_size = nii.header.get_zooms()
print(vox_size[1])

new_voxel_dims = vox_size[1] / 2

affine = nii.affine

print(affine)

new_affine = rescale_affine(affine, voxel_dims=[0.375, 0.375, 0.375])
print(new_affine)

resampled_MP2RAGE = resample_img(
    img,
    target_affine=new_affine,
    target_shape=np.multiply(dimensions, resampling_factor),
)
resampled_MP2RAGE.to_filename(
    "/Users/barilari/Desktop/sub-pilot001_ses-001_acq-r0p4_UNIT1.nii"
)
