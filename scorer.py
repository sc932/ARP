from basis_space import UpDownBasisSpace, UpMidDownBasisSpace
from dataset import Dataset

import numpy
import statsmodels.api as sm
import matplotlib.pyplot as plt
import plotter
import utils
import matplotlib.backends.backend_pdf


import logging

logger = logging.getLogger(__name__)

def csv_safe_pair_txt(pair):
    txt = "(" + pair[0] + ";" + pair[1] + ")"
    return txt

def combiner(dataset_yml, basis_space_to_use, p_thresh=0.05, scorer=None, output="output", pdf=None, csv_content=None, all_one=False):
    if pdf == None:
        pdf = matplotlib.backends.backend_pdf.PdfPages("./" + output + ".pdf")
    if csv_content == None:
        csv_content = []

    if scorer is None:
        scorer = Scorer(dataset_yml, basis_space_to_use)

    if len(csv_content) == 0:
        content = [scorer.dataset.team_idx_name]
        content.extend(scorer.dataset.get_team_ids())
        csv_content.append(content)
    else:
        content = []

    for target_var in scorer.dataset.target_vars:
        
        best_basis_functions = {}
        overall_target_score = None
        
        for pair, fits in scorer.full_score_data[target_var].items():
            best_p_val = 1
            best_basis_function = None
            for [p_val, r_sq, basis_function, target_scores, basis_scores] in fits:
                overall_target_score = target_scores
                if p_val <= best_p_val:
                    best_p_val = p_val
                    best_basis_function = basis_function
                    
            if best_basis_function is not None and best_p_val < p_thresh:
                best_basis_functions[pair] = [basis_scores, best_basis_function, p_val, r_sq]
        
        #print(best_basis_functions)
        running_score = numpy.zeros(len(overall_target_score))
        for pair, [basis_scores, best_basis_function, p_val, r_sq] in best_basis_functions.items():
            logging.debug(target_var)
            logging.debug(pair)
            logging.debug(best_basis_function.function_shape)
            logging.debug(len(basis_scores))
            logging.debug(p_val)
            logging.debug(r_sq)
            logging.info("Combined: " + csv_safe_pair_txt(pair))
            running_score += numpy.array(basis_scores)
            if not all_one:
                content = [csv_safe_pair_txt(pair)]
            else:
                content = [csv_safe_pair_txt(pair) + "_b-" + str(basis_function.csv_safe_shape())]
            content.extend(basis_scores)
            csv_content.append(content)

        if False:
            if sum(running_score) > 0:
                plotter.plot_fit(running_score, overall_target_score, target_var, pdf=pdf)
                content = ["combined"]
                content.extend(running_score)
                csv_content.append(content)

        # PLOT SUM HERE
        plotter.plot_full_analysis_for_sum(scorer, target_var, best_basis_functions, p_thresh=p_thresh*2, pdf=pdf)

        for pair, [basis_scores, best_basis_function, p_val, r_sq] in best_basis_functions.items():
            plotter.plot_full_analysis(scorer, target_var, pair[0], pair[1], p_thresh=p_thresh*2, pdf=pdf)

    #plt.show()

    if not all_one:
        pdf.close()
    logging.info("All plots saved to output pdf: " + output + ".pdf")
    return csv_content
    
 
class Scorer(object):
    def __init__(self, dataset_yml, basis_space_to_use, force_fit=False):
        self.dataset = Dataset(dataset_yml)
        self.basis = basis_space_to_use

        logging.info("Initializing Scorer...")

        self.full_score_data = {}
        self.best_score_data = {}

        attr_pairs = []
        for i in range(len(self.dataset.combined_attr_list)):
            for j in range(i+1, len(self.dataset.combined_attr_list)):
                attr_pairs.append([self.dataset.combined_attr_list[i], self.dataset.combined_attr_list[j]])

        team_ids = self.dataset.get_team_ids()
        logging.debug("Scoring teams: " + str(team_ids))

        for target_var in self.dataset.target_vars:
            logging.info("Scoring target variable " + target_var + "...")
            
            self.full_score_data[target_var] = {}
            self.best_score_data[target_var] = {}
            for [a1, a2] in attr_pairs:
                self.full_score_data[target_var][(a1, a2)] = []
                self.best_score_data[target_var][(a1, a2)] = []
                best_basis = None
                best_p_val = 1
                for basis_function in self.basis.basis_functions:
                    target_scores = []
                    basis_scores = []
                    for team_id in team_ids:
                        targets = self.dataset.get_member_attributes_by_team_id(team_id, target_var)
                        #logging.debug("targets:" + str(targets))
                        if targets is None:
                            logging.info("TEAM " + str(team_id) + ": at least one team member did not have the target var assigned")
                            continue # at least one team member did not have the target var assigned
                        target_score = numpy.mean(targets)
                        attr1_vals = self.dataset.get_member_attributes_by_team_id(team_id, a1)
                        attr2_vals = self.dataset.get_member_attributes_by_team_id(team_id, a2)
                        basis_score = 0
                        for i in range(len(attr1_vals)):
                            x = attr1_vals[i]
                            y = attr2_vals[i]
                            r, theta = utils.polar_from_x_y(x, y, x_offset=self.dataset.attr_means[a1], y_offset=self.dataset.attr_means[a2])
                            bs = basis_function.eval(theta)
                            basis_score += r*bs
                        target_scores.append(target_score)
                        basis_scores.append(basis_score)
                    # now we have all the scores for this basis func

                    X = sm.add_constant(basis_scores)
                    est = sm.OLS(target_scores, X)
                    est2 = est.fit()

                    p_val = est2.f_pvalue
                    r_sq = est2.rsquared

                    coef = numpy.polyfit(target_scores, basis_scores, 1)

                    #logging.info("p " + str(p_val) + " r2 " + str(r_sq) + " b " + str(basis_function.function_shape))

                    if p_val < best_p_val and (coef[0] > 0 or force_fit):
                        best_p_val = p_val
                        best_basis = [basis_function, target_scores, basis_scores, p_val, r_sq]

                    if coef[0] > 0 or force_fit:
                        self.full_score_data[target_var][(a1, a2)].append([
                            p_val,
                            r_sq,
                            basis_function,
                            target_scores,
                            basis_scores,
                        ])


                    
                    
                if best_basis is not None:
                    [basis_function, target_scores, basis_scores, p_val, r_sq] = best_basis
                    self.best_score_data[target_var][(a1, a2)].append([
                        p_val,
                        r_sq,
                        basis_function,
                        target_scores,
                        basis_scores,
                    ])
                    #plotter.plot_basis_with_pairwise_data_and_fit(basis_function, self.dataset, a1, a2, basis_scores, target_scores, title=target_var)
                else:
                    logging.info("Could not find basis function for (" + a1 + ", " + a2 + ") -> " + target_var)