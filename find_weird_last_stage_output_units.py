from pathlib import Path
from obspy import read_inventory

nrl = Path('./NRLv2_stationxml/')

equipment_type = 'datalogger'

ok = ("counts", "count", "COUNTS", "COUNT")

for path in (nrl / equipment_type).glob('**/*.xml'):
    resp = read_inventory(path)[0][0][0].response
    if resp.instrument_sensitivity.output_units.lower() not in ok or \
            resp.response_stages[-1].output_units not in ok:
        print(f'{resp.instrument_sensitivity.output_units:10s} {resp.response_stages[-1].output_units:10s} {str(path)}')
