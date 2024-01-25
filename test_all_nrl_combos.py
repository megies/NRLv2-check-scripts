from copy import deepcopy
import numpy as np
from obspy import read_inventory
from obspy.clients.nrl import NRL
from obspy.clients.nrl.client import NRLDict

nrl = NRL('./NRLv2_stationxml')


def recurse_sensors(node):
    sensors = []
    for key in node:
        item = node[key]
        if isinstance(item, NRLDict):
            sensors += recurse_sensors(item)
        elif isinstance(item, tuple):
            description, path, resp_type = item
            resp = read_inventory(path, resp_type)[0][0][0].response
            if not resp.response_stages:
                print(f'Skipping sensor response without response stages '
                      f'(not implemented): {path}')
                continue
            sensors.append((description, path, resp_type, resp))
    return sensors


def recurse_dataloggers(node, sensors, fh):
    for key in node:
        item = node[key]
        if isinstance(item, NRLDict):
            recurse_dataloggers(item, sensors, fh)
        elif isinstance(item, tuple):
            description, path, resp_type = item
            resp = read_inventory(path, resp_type)[0][0][0].response
            for _, sensor_path, _, sensor in sensors:
                combined = nrl._combine_sensor_datalogger(deepcopy(sensor), deepcopy(resp))
                units_ok = units_sanity_check(combined)
                # sensitivity_ok = sensitivity_check(combined)
                sensitivity_overall = combined.instrument_sensitivity.value
                sensitivity_product = np.product(list(
                    stage.stage_gain for stage in combined.response_stages))
                reldiff = abs(sensitivity_overall - sensitivity_product) / sensitivity_overall
                sensitivity_ok = reldiff < 0.01
                info = f'{units_ok:d} {sensitivity_ok:d} {path} {sensor_path} {sensitivity_overall:.2g} {sensitivity_product:.2g} {reldiff:.2g}'
                print(info, file=fh)
    return


def units_sanity_check(resp):
    sens = resp.instrument_sensitivity
    first = resp.response_stages[0]
    last = resp.response_stages[-1]
    try:
        assert sens.input_units is not None
        assert sens.output_units is not None
        for stage in resp.response_stages:
            assert stage.input_units is not None
            assert stage.output_units is not None
        assert sens.input_units.lower() == first.input_units.lower()
        assert sens.output_units.lower() == last.input_units.lower()
        for stage1, stage2 in zip(resp.response_stages,
                                  resp.response_stages[1:]):
            assert stage1.output_units.lower() == stage2.input_units.lower()
    except AssertionError:
        return False
    return True


# def sensitivity_check(resp):
#     sens = resp.instrument_sensitivity
#     try:
#         sensitivity = np.product(list(
#             stage.stage_gain for stage in resp.response_stages))
#         assert abs(sens.value - sensitivity) / sens.value < 0.01
#     except AssertionError:
#         return False
#     return True


sensors = recurse_sensors(nrl.sensors)

with open('output.log', 'wt', encoding='UTF-8') as fh:
    recurse_dataloggers(nrl.dataloggers, sensors, fh)

#all_sensors = recurse_sensors(nrl.sensors)
#sensors = []
#for key in nrl.sensors:
#    _recurse()
#
