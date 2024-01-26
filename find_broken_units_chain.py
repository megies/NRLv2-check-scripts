from pathlib import Path
from obspy import read_inventory
from obspy.core.inventory.response import ResponseStage

nrl = Path('./NRLv2_stationxml/')

equipment_types = ['sensor', 'datalogger']
#equipment_types = ['datalogger']

for equipment_type in equipment_types:
    with open(f'broken_units_chain.{equipment_type}.log', 'wt') as fh:
        for path in (nrl / equipment_type).glob('**/*.xml'):
            # if str(path) == "NRLv2_stationxml/datalogger/MagseisFairfield/ZlandGen2_PD6_FR500_FPLP_DF1.xml":
            #     import pdb; pdb.set_trace()
            # else:
            #     continue
            # ignore stage gain only response stages in this one and skip over them
            resp = read_inventory(path)[0][0][0].response
            stages = resp.response_stages
            info = []
            if not stages:
                # skip unity gain polynomial only response
                continue
            last = stages[0]
            # note that units of stage gain only response stages already
            # might've been tinkered with during the obspy read operation
            # internally, so these might show up different in the log then what
            # is in the file, but that should still leave the "real" problems
            # detectable here
            info.append(f'{last.input_units or "NONE"}>{last.output_units or "NONE"}')
            ok = True
            for stage in stages[1:]:
                if type(stage) is ResponseStage:
                    if not stage.input_units and not stage.output_units:
                        # skip gain-only stages without units for now
                        # see above they might still get included here if
                        # changed by obspy already
                        continue
                if stage.input_units != last.output_units:
                    ok = False
                info.append(f'{stage.input_units or "NONE"}>{stage.output_units or "NONE"}')
                last = stage
            info = '|'.join(info)
            fh.write(f'{ok and "ok  " or "bad "} {info:30s} {path}\n')
