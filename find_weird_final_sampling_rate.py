from pathlib import Path
from obspy import read_inventory

nrl = Path('./NRLv2_stationxml/')

equipment_type = 'datalogger'

for path in (nrl / equipment_type).glob('**/*.xml'):
    is_ok = True
    resp = read_inventory(path)[0][0][0].response
    try:
        expected = float(path.name.rsplit('.', 1)[0].split('_FR')[1].split('_')[0])
    except:
        import pdb; pdb.set_trace()
    stage = resp.response_stages[-1]
    try:
        final_sampling_rate = stage.decimation_input_sample_rate / stage.decimation_factor
    except:
        final_sampling_rate = None
    if final_sampling_rate != expected:
        if stage.resource_id == "NRL:DigPAZ_SG1_IUcounts_NZ1_NP1_PHa04897f_AN1_FN1":
            reason = 'PAZunity5Hz'
        elif stage.resource_id == "NRL:AnaPAZ_IUV_NZ1_NP1_PH2579c80_AN1_FN1::NRL:Gain_SG1_FN50":
            reason = 'AnaPAZ'
        elif final_sampling_rate is None:
            reason = 'None'
        else:
            reason = 'UNKOWN'
        print(f'{reason:15s} {str(expected):10s} {str(final_sampling_rate):10s} {str(path)}')
