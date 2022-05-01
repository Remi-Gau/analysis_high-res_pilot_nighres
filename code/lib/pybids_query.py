
from bidsNighres.bidsutils import get_bids_filter_config



bids_filter_file = '/home/marcobar/Data/analysis_high-res_pilot_nighrescode/bidsNighres/filter_file.json'
layout = BIDSLayout('/home/marcobar/Data/analysis_high-res_pilot_nighres/outputs/derivatives/bidsNighres/')

bids_filter = get_bids_filter_config(bids_filter_file)


skullstripped_UNIT1 = layout.get(
return_type="filename",
subject="pilot001",
session="001",
extension="nii",
description=["skullstripped"],
regex_search=True,
invalid_filters="allow",
**bids_filter["UNIT1"],
)
