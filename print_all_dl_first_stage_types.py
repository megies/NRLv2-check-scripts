from pathlib import Path
from obspy import read_inventory

nrl = Path('./NRLv2_stationxml/')

for path in (nrl / 'datalogger').glob('**/*.xml'):
    resp = read_inventory(path)[0][0][0].response
    print(resp.response_stages[0].__class__.__name__, path)
