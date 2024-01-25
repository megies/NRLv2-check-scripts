from pathlib import Path
from obspy import read_inventory

nrl = Path('./NRLv2_stationxml/')

equipment_types = ['sensor', 'datalogger']

for equipment_type in equipment_types:
    with open(f'unset_units.{equipment_type}.log', 'wt') as fh:
        for path in (nrl / equipment_type).glob('**/*.xml'):
            resp = read_inventory(path)[0][0][0].response
            errors = set()
            for i, stage in enumerate(resp.response_stages):
                # no unset units, move on
                if stage.input_units not in (None, '') and stage.output_units not in (None, ''):
                    continue
                if i == 0:
                    # unset units in first stage
                    errors.add(0)
                elif i == len(resp.response_stages) - 1:
                    # unset units in last stage
                    errors.add(2)
                else:
                    # unset units in middle stage
                    errors.add(1)
            if errors:
                fh.write(f'{",".join(map(str, sorted(errors))):<5s} {path}\n')
            else:
                fh.write(f'ok {path}\n')
