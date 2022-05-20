#!/usr/bin/env python3

import korali
import numpy as np
import os

from bridge import run_msolve


def run_model(xcoords, ycoords, ksample):
    generation = int(ksample["Current Generation"])
    sample_id  = int(ksample["Sample Id"])
    theta1, theta2 = ksample["Parameters"]
    parameters = [theta1, theta2]

    x, y, T = run_msolve(xcoords=xcoords,
                         ycoords=ycoords,
                         generation=generation,
                         sample_id=sample_id,
                         parameters=parameters)

    ksample["Evaluations"] = T


def read_temperature(korali_file: str):
    import json

    with open(korali_file, "r") as f:
        doc = json.load(f)

    T = []
    for sample in doc["Samples"]:
        T.append(list(sample["Evaluations"]))

    return np.array(T)


if __name__ == '__main__':

    x = np.array([0.1, 0.4, 0.9])
    y = np.array([0.2, 0.5, 0.6])

    theta1 = np.array([1.0, 0.2])
    theta2 = np.array([0.2, 0.1])

    e = korali.Experiment()

    e["Problem"]["Type"] = "Propagation"
    e["Problem"]["Execution Model"] = lambda ks: run_model(xcoords=x, ycoords=y, ksample=ks)

    e['Solver']['Type'] = 'Executor'
    e['Solver']['Executions Per Generation'] = 2


    e["Variables"][0]["Name"] = "theta1"
    e["Variables"][0]["Precomputed Values"] = theta1.tolist()
    e["Variables"][1]["Name"] = "theta2"
    e["Variables"][1]["Precomputed Values"] = theta2.tolist()

    e['Store Sample Information'] = True

    k = korali.Engine()
    k.run(e)

    Tref = np.array([[0.000167, 0.001144, 0.000864],
                     [0.026306, 0.008453, 0.000962]])
    T = read_temperature(os.path.join("_korali_result", "latest"))

    np.testing.assert_array_almost_equal(T, Tref, decimal=5)
