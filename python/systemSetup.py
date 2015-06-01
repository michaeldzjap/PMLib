from ResonatorNetwork import ResonatorNetwork
from Resonator1D import Resonator1D
from Resonator2D import Resonator2D
import json,os
from numpy import asarray

with open(os.path.dirname(os.path.realpath(__file__)) + '/networkArgs.json') as json_data:
    args = json.load(json_data)
    resonators = []
    for r in args['resonators']:
        if r['dim'] == 1:
            resonators.append(Resonator1D(r['gamma'],r['kappa'],r['b1'],r['b2'],r['bc']))
        else:
            resonators.append(Resonator2D(r['gamma'],r['kappa'],r['b1'],r['b2'],r['bc'],r['epsilon']))
    network = ResonatorNetwork(resonators,asarray(args['connPointMatrix']),asarray(args['massMatrix']),\
    asarray(args['excPointMatrix']),asarray(args['readoutPointMatrix']))
    network.calcModes(args['minFreq'],args['maxFreq']);
    if args['incl'][0] == 'y':
        network.calcBiquadCoefs(args['gain'])
    json_data.close()
    network.saveAsJSON(args['path'],args['incl'])
