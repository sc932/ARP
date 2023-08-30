import argparse
import scorer
from basis_space import UpDownBasisSpace, UpMidDownBasisSpace

import logging

parser = argparse.ArgumentParser(description=
                                 """This will run through the code described in [paper X].\n
                                 For more information see [website Y]."""
                                 )
parser.add_argument("yml", help=".yml file with config values")
parser.add_argument("-p", "--p-threshold", help="p-val threshold for when to print output", default=0.05)
parser.add_argument("-v", "--verbose", help="verbosity of logging [10: Debug, 20: Info <default>, 30: Warning, etc]", default=20)
parser.add_argument("-o", "--output", help="the name of the output file <default: [name of .yml file + _output]>")
args = parser.parse_args()
config = vars(args)

logging.basicConfig(
    level=config["verbose"],
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

logging.info("Configs: " + str(config))

def main():
    if "p_threshold" in config:
        p_thresh = float(config["p_threshold"])
    else:
        p_thresh = 0.05

    if "output" in config and config["output"] is not None:
        output = str(config["output"])
    else:
        output = str(config["yml"])[:-4] + "_output"

    scorer_obj = scorer.Scorer(config["yml"], UpMidDownBasisSpace())
    scorer.combiner(config["yml"], UpMidDownBasisSpace(), p_thresh=p_thresh, scorer=scorer_obj, output=output)


if __name__ == "__main__":
    main()