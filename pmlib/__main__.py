import argparse
import json

from .ResonatorBase import ResonatorBase
from .ResonatorNetwork import ResonatorNetwork
from .Resonator1D import Resonator1D
from .Resonator2D import Resonator2D


parser = argparse.ArgumentParser('pmlib')
parser.add_argument(
    '-s', '--sample-rate', type=int, default=44100,
    help='set sample rate for calculations')
parser.add_argument(
    'input', type=str,
    help='JSON file with network arguments')
parser.add_argument(
    'output', nargs='*', type=str, default=['modal_data.json'],
    help='resulting JSON file with modal data')

args = parser.parse_args()


# Main.
SR = args.sample_rate
network_file = args.input  # Was 'networkArgs.json'
output_file = args.output[0]  # Was 'modalData.json'

with open(network_file) as jsonfile:
    args = json.load(jsonfile)
    resonators = []

    for r in args['resonators']:
        if r['dim'] == 1:
            resonators.append(Resonator1D(
                r['gamma'], r['kappa'],
                r['b1'], r['b2'], r['bc'], SR))
        else:
            resonators.append(Resonator2D(
                r['gamma'], r['kappa'],
                r['b1'], r['b2'], r['bc'],
                r['epsilon'], SR))
    network = ResonatorNetwork(
        resonators,
        args['connPointMatrix'], args['massMatrix'],
        args['excPointMatrix'], args['readoutPointMatrix'], SR)

    network.calc_modes(args['minFreq'], args['maxFreq'], args['minT60'])
    if args['incl'][0] == 'y':
        network.calc_biquad_coefs(args['gain'])

    if 'path' in args:
        output_file = args['path']
    network.save_json(output_file, args['incl'])
