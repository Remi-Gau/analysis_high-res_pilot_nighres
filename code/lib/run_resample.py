import numpy as np
import nibabel as nb

from nilearn.image import resample_img

from rescale_affine import rescale_affine

from os.path import abspath
from os.path import join

from bidsNighres.bidsNighres.bidsutils import get_bids_filter_config
from bidsNighres.bidsNighres.bidsutils import get_dataset_layout
from bidsNighres.bidsNighres.bidsutils import check_layout
from bidsNighres.bidsNighres.bidsutils import init_derivatives_layout
from bidsNighres.bidsNighres.bidsutils import create_bidsname
from bidsNighres.bidsNighres.utils import print_to_screen
from bidsNighres.bidsNighres.utils import return_path_rel_dataset

from bids import BIDSLayout

# def skullstrip(
#     layout_in, layout_out, this_participant, bids_filter: dict, dry_run=False
# ):


participant_label = "pilot001 pilot004 pilot005"

participant_label = participant_label.split(" ")

input_datasets = "/Users/barilari/data/V5_high-res_pilot001_analyses/analysis_high-res_pilot_nighres/inputs/raw"

output_location = "/Users/barilari/data/V5_high-res_pilot001_analyses/analysis_high-res_pilot_nighres/outputs/derivatives/bidsNighres"

bids_filter_file = "/Users/barilari/data/V5_high-res_pilot001_analyses/analysis_high-res_pilot_nighres/code/bidsNighres/filter_file_resample.json"

images = ["UNIT1", "inv2"]

resampling_factor = 2

dry_run = False

input_datasets = abspath(input_datasets)
print(f"Input dataset: {input_datasets}")

output_location = abspath(output_location)
print(f"Output location: {output_location}")

if bids_filter_file == "":
    bids_filter = get_bids_filter_config()
else:
    bids_filter = get_bids_filter_config(bids_filter_file)

layout_in = get_dataset_layout(input_datasets)
check_layout(layout_in)

layout_out = init_derivatives_layout(output_location)


for participant in participant_label:

    this_participant = participant

    print_to_screen(f"\n[bold]Processing: sub-{this_participant}[/bold]")

    sessions = layout_in.get_sessions(
        subject=this_participant,
        extension="nii",
        regex_search=True,
        **bids_filter["UNIT1"],
    )

    for ses in sessions:

        print_to_screen(f"[bold] Processing: ses-{ses}[/bold]")

        unit1_files = layout_in.get(
            subject=this_participant,
            session=ses,
            extension="nii",
            regex_search=True,
            **bids_filter["UNIT1"],
        )

        for bf in unit1_files:

            # entities = bf.get_entities()

            # TODO make output path generation more flexible
            sub_entity = f"sub-{this_participant}"
            ses_entity = f"ses-{ses}"
            output_dir = join(layout_out.root, sub_entity, ses_entity, "anat")

            # TODO find a way to match the entities between files
            # use filter file to select only lores
            # entities["acquisition"] = "lores"

            UNIT1 = layout_in.get(
                return_type="filename",
                subject=this_participant,
                session=ses,
                extension="nii",
                regex_search=True,
                **bids_filter["UNIT1"],
            )
            print_to_screen(
                f"  t1w image: {return_path_rel_dataset(UNIT1[0], layout_in.root)}"
            )

            inv2 = layout_in.get(
                return_type="filename",
                subject=this_participant,
                session=ses,
                extension="nii",
                regex_search=True,
                **bids_filter["inv2"],
            )
            print_to_screen(
                f"  2nd inversion image: {return_path_rel_dataset(inv2[0], layout_in.root)}"
            )

            layout = BIDSLayout(output_location)

            # UNIT1

            pattern = "sub-{subject}[/ses-{session}]/anat/sub-{subject}[_ses-{session}][_acq-{acquisition}]_UNIT1{extension<.nii|.nii.gz|.json>|.nii.gz}"

            entities = layout.parse_file_entities(UNIT1[0])
            entities["acquisition"] = "r0p375"
            filename = layout.build_path(entities, pattern, validate=False)

            nii = nb.load(UNIT1[0])

            dimensions = nii.header.get_data_shape()
            print(np.multiply(dimensions, 2))

            vox_size = nii.header.get_zooms()
            print(vox_size[1])

            new_voxel_dims = vox_size[1] / 2

            affine = nii.affine

            new_affine = rescale_affine(
                affine,
                voxel_dims=[new_voxel_dims, new_voxel_dims, new_voxel_dims],
            )

            resampled_img = resample_img(
                UNIT1[0],
                target_affine=new_affine,
                target_shape=np.multiply(dimensions, resampling_factor),
            )

            resampled_img.to_filename(filename)

            # inv2

            pattern = "sub-{subject}[/ses-{session}]/anat/sub-{subject}[_ses-{session}][_acq-{acquisition}][_inv-{inv}][_part-{part}]_MP2RAGE{extension<.nii|.nii.gz|.json>|.nii.gz}"

            entities = layout.parse_file_entities(inv2[0])
            entities["acquisition"] = "r0p375"
            filename = layout.build_path(entities, pattern, validate=False)

            nii = nb.load(inv2[0])

            dimensions = nii.header.get_data_shape()
            print(np.multiply(dimensions, 2))

            vox_size = nii.header.get_zooms()
            print(vox_size[1])

            new_voxel_dims = vox_size[1] / 2

            affine = nii.affine

            new_affine = rescale_affine(
                affine,
                voxel_dims=[new_voxel_dims, new_voxel_dims, new_voxel_dims],
            )

            resampled_img = resample_img(
                inv2[0],
                target_affine=new_affine,
                target_shape=np.multiply(dimensions, resampling_factor),
            )

            resampled_img.to_filename(filename)
