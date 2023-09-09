import argparse
import scorer
from basis_space import UpDownBasisSpace, UpMidDownBasisSpace, SymetricUpDownTwo, BasisSpace
import matplotlib.backends.backend_pdf
import csv

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
parser.add_argument("-ao", "--all-one", help="perform the analysis for each basis function in the basis space individually AND put it all in one file", action=argparse.BooleanOptionalAction)
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

    do_all = False
    all_one = False
    if "all_one" in config and config["all_one"] is not None:
        do_all = True
        all_one = True
    elif "all" in config and config["all"] is not None:
        do_all = True
        all_one = False
    else:
        do_all = False
        all_one = False

    if not do_all:
        scorer_obj = scorer.Scorer(config["yml"], basis_space)
        csv_content = scorer.combiner(config["yml"], basis_space, p_thresh=p_thresh, scorer=scorer_obj, output=output)
        write_to_csv(output, csv_content)
    else:
        pdf = None
        csv_content = None
        if all_one:
            pdf = matplotlib.backends.backend_pdf.PdfPages("./" + output + "_all.pdf")

        for basis_function in basis_space.basis_functions:
            temp_basis_space = BasisSpace()
            temp_basis_space.basis_functions = [basis_function]
            logging.info("Using basis function: " + str(basis_function.function_shape))
            temp_output = output + "_b-" + str(basis_function.function_shape)
            scorer_obj = scorer.Scorer(config["yml"], temp_basis_space, force_fit=True)
            csv_content = scorer.combiner(config["yml"], temp_basis_space, p_thresh=p_thresh, scorer=scorer_obj, output=temp_output, all_one=all_one, pdf=pdf, csv_content=csv_content)
            if not all_one:
                write_to_csv(temp_output, csv_content)
        if all_one:
            write_to_csv(output + "_all", csv_content)
            pdf.close()



def write_to_csv(output, csv_content):
    # TODO, try to catch if it is open/protected and suggest to the user to close it
    with open(output + ".csv", 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        rows = zip(*csv_content)
        for row in rows:
            writer.writerow(row)
    logging.info("All data saved to output csv: " + output + ".csv")



if __name__ == "__main__":
    main()