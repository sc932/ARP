import argparse
import scorer
from basis_space import UpDownBasisSpace, UpMidDownBasisSpace, SymetricUpDownTwo, BasisSpace

import logging

parser = argparse.ArgumentParser(description=
                                 """This will run through the code described in [paper X].\n
                                 For more information see [website Y]."""
                                 )
parser.add_argument("yml", help=".yml file with config values")
parser.add_argument("-p", "--p-threshold", help="p-val threshold for when to print output", default=0.05)
parser.add_argument("-v", "--verbose", help="verbosity of logging [10: Debug, 20: Info <default>, 30: Warning, etc]", default=20)
parser.add_argument("-o", "--output", help="the name of the output file <default: [name of .yml file + _output]>")
parser.add_argument("-b", "--basis", help="which basis space to use (see paper) [UpDown, UpMidDown, SymTwo]", default="SymTwo")
parser.add_argument("-a", "--all", help="perform the analysis for each basis function in the basis space individually", action=argparse.BooleanOptionalAction)
args = parser.parse_args()
config = vars(args)

logging.basicConfig(
    level=int(config["verbose"]),
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

    if "basis" in config and config["basis"] is not None:
        basis = str(config["basis"])
    else:
        basis = "SymTwo"

    if basis == "SymTwo":
        basis_space = SymetricUpDownTwo()
    elif basis == "UpMidDown":
        basis_space = UpMidDownBasisSpace()
    elif basis == "UpDown":
        basis_space = UpDownBasisSpace()
    else:
        logging.error("Could not find basis space: " + str(basis))

    if "all" in config and config["all"] is not None:
        do_all = True
    else:
        do_all = False

    if not do_all:
        scorer_obj = scorer.Scorer(config["yml"], basis_space)
        scorer.combiner(config["yml"], basis_space, p_thresh=p_thresh, scorer=scorer_obj, output=output)
    else:
        for basis_function in basis_space.basis_functions:
            temp_basis_space = BasisSpace()
            temp_basis_space.basis_functions = [basis_function]
            logging.info("Using basis function: " + str(basis_function.function_shape))
            temp_output = output + "_b-" + str(basis_function.function_shape)
            scorer_obj = scorer.Scorer(config["yml"], temp_basis_space, force_fit=True)
            scorer.combiner(config["yml"], temp_basis_space, p_thresh=p_thresh, scorer=scorer_obj, output=temp_output)

            



if __name__ == "__main__":
    main()