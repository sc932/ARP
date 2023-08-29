import argparse
import scorer
from basis_space import UpDownBasisSpace, UpMidDownBasisSpace
import plotter

import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

parser = argparse.ArgumentParser(description=
                                 """This will run through the code described in [paper X].\n
                                 For more information see [website Y]."""
                                 )
parser.add_argument("yml", help=".yml file with config values")
parser.add_argument("-p", "--p-threshold", help="p-val threshold for when to print output", default=0.05)
args = parser.parse_args()
config = vars(args)
print(config)

def main():
    if "p_threshold" in config:
        p_thresh = float(config["p_threshold"])
    else:
        p_thresh = 0.05

    scorer_obj = scorer.Scorer(config["yml"], UpMidDownBasisSpace())
    assert(False)
    scorer.combiner(config["yml"], UpMidDownBasisSpace(), p_thresh=p_thresh, scorer=scorer_obj)


if __name__ == "__main__":
    main()