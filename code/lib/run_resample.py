from resampleNifti import resampleNifti

import os
import subprocess
import click
from os.path import abspath
from os.path import dirname
from os.path import join
from os.path import realpath


from bidsNighres.bidsNighres.bidsutils import get_bids_filter_config
from bidsNighres.bidsNighres.bidsutils import get_dataset_layout
from bidsNighres.bidsNighres.bidsutils import check_layout
from bidsNighres.bidsNighres.bidsutils import init_derivatives_layout
from bidsNighres.bidsNighres.utils import print_to_screen
from bidsNighres.bidsNighres.utils import return_path_rel_dataset

from bids import BIDSLayout

# __version__ = open(join(dirname(realpath(__file__)), "version")).read()


def run_resample(command, env={}):
    merged_env = os.environ
    merged_env.update(env)
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True,
        env=merged_env,
    )
    while True:
        line = process.stdout.readline()
        line = str(line, "utf-8")[:-1]
        print(line)
        if line == "" and process.poll() != None:
            break
    if process.returncode != 0:
        raise Exception("Non zero return code: %d" % process.returncode)


@click.command()
@click.option(
    "--input-datasets",
    help="""
            The directory with the input dataset formatted according to the BIDS standard.
            """,
    type=click.Path(exists=True, dir_okay=True),
    required=True,
)
@click.option(
    "--output-location",
    help="""
            The directory where the output files should be stored.
            If you are running group level analysis this folder should be prepopulated
            with the results of the participant level analysis.
            """,
    type=click.Path(exists=False, dir_okay=True),
    required=True,
)
# @click.option(
#     "--resample-factor",
#     help="""
#             Factor by which the image will be resampled, for example  "2" means double the resoulution.
#             """,
#     type=click.IntRange(min=0.1, max=3, min_open=False, max_open=False, clamp=True),
#     default=2,
#     show_default=True,
# )
@click.option(
    "--participant-label",
    help="""
            The label(s) of the participant(s) that should be analyzed. The label
            corresponds to sub-<participant_label> from the BIDS spec
            (so it does not include "sub-"). If this parameter is not
            provided all subjects should be analyzed. Multiple
            participants can be specified with a space separated list.
            """,  # nargs ?
    required=True,
)
@click.option(
    "--bids-filter-file",
    help="""
            Path to a JSON file to filter input file
            """,
    default="",
    show_default=True,
)
def main(
    input_datasets,
    output_location,
    participant_label,
    bids_filter_file,
):

    resampling_factor = 2

    participant_label = participant_label.split(" ")

    input_datasets = abspath(input_datasets)
    print_to_screen(f"Input dataset: {input_datasets}")

    output_location = abspath(output_location)
    print_to_screen(f"Output location: {output_location}")

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

                T1map = layout_in.get(
                    return_type="filename",
                    subject=this_participant,
                    session=ses,
                    extension="nii",
                    regex_search=True,
                    **bids_filter["T1map"],
                )
                print_to_screen(
                    f"  t1map image: {return_path_rel_dataset(T1map[0], layout_in.root)}"
                )

                layout = BIDSLayout(output_location)

                print("\n")
                print("resampling:")

                # UNIT1

                print("\n")
                print("- UNIT1")

                pattern = "sub-{subject}[/ses-{session}]/anat/sub-{subject}[_ses-{session}][_acq-{acquisition}]_UNIT1{extension<.nii|.nii.gz|.json>|.nii.gz}"

                entities = layout.parse_file_entities(UNIT1[0])
                entities["acquisition"] = "r0p375"
                filename = layout.build_path(entities, pattern, validate=False)

                # resampleNifti(UNIT1[0], resampling_factor, filename)

                print("  done")
                print("\n")

                # inv2

                print("- inv2")

                pattern = "sub-{subject}[/ses-{session}]/anat/sub-{subject}[_ses-{session}][_acq-{acquisition}][_inv-{inv}][_part-{part}]_MP2RAGE{extension<.nii|.nii.gz|.json>|.nii.gz}"

                entities = layout.parse_file_entities(inv2[0])
                entities["acquisition"] = "r0p375"
                filename = layout.build_path(entities, pattern, validate=False)

                # resampleNifti(inv2[0], resampling_factor, filename)

                print("  done")
                print("\n")

                # T1map

                print("- T1map")

                pattern = "sub-{subject}[/ses-{session}]/anat/sub-{subject}[_ses-{session}][_acq-{acquisition}]_T1map{extension<.nii|.nii.gz|.json>|.nii.gz}"

                entities = layout.parse_file_entities(T1map[0])
                entities["acquisition"] = "r0p375"
                filename = layout.build_path(entities, pattern, validate=False)

                # resampleNifti(T1map[0], resampling_factor, filename)

                print("  done")
                print("\n")


if __name__ == "__main__":
    main()
