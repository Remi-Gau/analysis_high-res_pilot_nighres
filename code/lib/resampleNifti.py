import numpy as np
import nibabel as nb

from nilearn.image import resample_img


def resampleNifti(img, resampling_factor, filename):

    nii = nb.load(img)

    dimensions = nii.header.get_data_shape()

    vox_size = nii.header.get_zooms()

    new_voxel_size = vox_size[1] / resampling_factor

    affine = nii.affine

    new_affine = rescale_affine(
        affine,
        voxel_dims=[new_voxel_size, new_voxel_size, new_voxel_size],
    )

    resampled_img = resample_img(
        img,
        target_affine=new_affine,
        target_shape=np.multiply(dimensions, resampling_factor),
    )

    resampled_img.to_filename(filename)


def rescale_affine(input_affine, voxel_dims=[1, 1, 1], target_center_coords=None):
    """
    This function uses a generic approach to rescaling an affine to arbitrary
    voxel dimensions. It allows for affines with off-diagonal elements by
    decomposing the affine matrix into u,s,v (or rather the numpy equivalents)
    and applying the scaling to the scaling matrix (s).

    Parameters
    ----------
    input_affine : np.array of shape 4,4
        Result of nibabel.nifti1.Nifti1Image.affine
    voxel_dims : list
        Length in mm for x,y, and z dimensions of each voxel.
    target_center_coords: list of float
        3 numbers to specify the translation part of the affine if not using the same as the input_affine.

    Returns
    -------
    target_affine : 4x4matrix
        The resampled image.
    """

    # Initialize target_affine
    target_affine = input_affine.copy()
    # Decompose the image affine to allow scaling
    u, s, v = np.linalg.svd(target_affine[:3, :3], full_matrices=False)

    # Rescale the image to the appropriate voxel dimensions
    s = voxel_dims

    # Reconstruct the affine
    target_affine[:3, :3] = u @ np.diag(s) @ v

    # Set the translation component of the affine computed from the input
    # image affine if coordinates are specified by the user.
    if target_center_coords is not None:
        target_affine[:3, 3] = target_center_coords
    return target_affine
