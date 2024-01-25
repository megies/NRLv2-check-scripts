from pathlib import Path
from obspy import read_inventory

nrl = Path('./NRLv2_stationxml/')

equipment_type = 'datalogger'

for path in (nrl / equipment_type).glob('**/*.xml'):
    resp = read_inventory(path)[0][0][0].response
    units = set()
    units.add(resp.instrument_sensitivity.input_units)
    units.add(resp.instrument_sensitivity.output_units)
    for i, stage in enumerate(resp.response_stages):
        units.add(stage.input_units)
        units.add(stage.output_units)
    units = [u.lower() if u else u for u in units]
    if "count" in units and "counts" in units:
        print(str(path))
