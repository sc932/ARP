import numpy
import matplotlib.pyplot as plt
import statsmodels.api as sm
import re
from operator import itemgetter

def plot_basis_space(basis_space):
    for basis_function in basis_space.basis_functions:
        plot_basis(basis_function)
    plt.show()

def plot_basis(basis_function):
    fig = plt.figure(figsize=(12,3))
    ax1 = plt.subplot(131)
    ax2 = plt.subplot(132, projection='polar')
    ax3 = plt.subplot(133)
    basis_function.plot(ax1, ax2, ax3)

def plot_basis_with_pairwise_data(basis_function, dataset, a1, a2):
    fig = plt.figure(figsize=(12,3))
    ax1 = plt.subplot(131)
    ax2 = plt.subplot(132, projection='polar')
    ax3 = plt.subplot(133)
    attribute_pair_thetas, attribute_pair_rs = dataset.get_pairwise_attributes_polar_values(a1, a2)
    ax2.scatter(attribute_pair_thetas, attribute_pair_rs, c='orange', alpha=0.1)
    basis_function.plot(ax1, ax2, ax3, attribute_pair=[a1, a2])

def plot_full_analysis(scorer, target_var, a1, a2, p_thresh=0.1, pdf=None):
    fig = plt.figure(figsize=(12,12))
    fig.suptitle("Pairwise analysis\n" + scorer.dataset.dataset_config['csv_file_name'] + "\n(" + a1 + ", " + a2 + ") -> " + target_var + "")
    ax1 = plt.subplot2grid((4, 3), (0, 0))
    ax2 = plt.subplot2grid((4, 3), (0, 1), projection='polar')
    ax3 = plt.subplot2grid((4, 3), (0, 2))
    attribute_pair_thetas, attribute_pair_rs = scorer.dataset.get_pairwise_attributes_polar_values(a1, a2)
    ax2.scatter(attribute_pair_thetas, attribute_pair_rs, c='orange', alpha=0.1)

    [p_val, r_sq, basis_function, target_scores, basis_scores] = scorer.best_score_data[target_var][(a1, a2)][0]
    basis_function.plot(ax1, ax2, ax3, attribute_pair=[a1, a2])

    ax3.text(0, .4, "p-val: " + str(p_val))
    ax3.text(0, .3, "r-sq: " + str(r_sq))
    ax3.text(0, .2, "mass vector angle(s): " + str(basis_function.get_function_mass_angles()))
    ax3.text(0, .1, "basis area: " + str(basis_function.get_function_area()[0]))

    ax4 = plt.subplot2grid((4, 3), (1, 0), colspan=3)
    plot_fit(basis_scores, target_scores, title="", ax=ax4)

    ax5 = plt.subplot2grid((4, 3), (2, 0))
    ax6 = plt.subplot2grid((4, 3), (2, 1))
    ax7 = plt.subplot2grid((4, 3), (2, 2))

    plot_rp_map(scorer, target_var, a1, a2, ax=ax5)
    plot_p_mass_vec_map(scorer, target_var, a1, a2, ax=ax6)
    plot_p_area_map(scorer, target_var, a1, a2, ax=ax7)

    ax8 = plt.subplot2grid((4, 3), (3, 0), colspan=3)

    plot_basis_info_under_threshold(scorer, target_var, a1, a2, ax8, p_thresh=p_thresh)

    if pdf is None:
        fig_str = "Pairwise analysis - " + scorer.dataset.dataset_config['csv_file_name'][:-4] + " - (" + a1 + ", " + a2 + ") to " + target_var + ".pdf"

        fig.savefig(fig_str)
    else:
        pdf.savefig(fig)

    #plt.show()

def plot_basis_info_under_threshold(scorer, target_var, a1, a2, ax0, p_thresh=0.1):
    ax0.text(0, .8, "All Basis Functions with p-val < " + str(p_thresh))
    data = scorer.full_score_data[target_var][(a1, a2)]

    sorted_data = sorted(data, key=itemgetter(0))

    for i, [p_val, r_sq, basis_function, target_scores, basis_scores] in enumerate(sorted_data):
        y_cord = 0.6 - 0.1*i
        if p_val > p_thresh:
            break
        if i > 6:
            ax0.text(0, y_cord, "Too many to print...")
            break
        ax0.text(0, y_cord, "p-val: " + str(p_val) + ", r-sq: " + str(r_sq) + ", basis-function: " + str(basis_function.function_shape))



    ps = []
    rs = []
    for [p_val, r_sq, basis_function, target_scores, basis_scores] in data:
        ps.append(p_val)
        rs.append(r_sq)

    ax0.grid(False)
    ax0.axis("off")


def plot_fit(basis_scores, target_scores, title="", ax=None, pdf=None):
    if ax is None:
        fig = plt.figure(figsize=(12,6))
        fig.suptitle(title)
        ax0 = plt.subplot(111)
    else:
        ax0 = ax
    coef = numpy.polyfit(basis_scores, target_scores, 1)
    poly1d_fn = numpy.poly1d(coef)

    ax0.scatter(basis_scores, target_scores)
    ax0.plot(basis_scores, poly1d_fn(basis_scores), '--k')

    X = sm.add_constant(basis_scores)
    est = sm.OLS(target_scores, X)
    est2 = est.fit()

    p_val = est2.f_pvalue
    r_sq = est2.rsquared

    ax0.set_xlabel("r^2: " + str(r_sq) + ", p-val: " + str(p_val))

    if pdf is not None:
        pdf.savefig(fig)

    

def plot_rp_map(scorer, target_var, a1, a2, ax=None):
    data = scorer.full_score_data[target_var][(a1, a2)]
    ps = []
    rs = []
    
    for [p_val, r_sq, basis_function, target_scores, basis_scores] in data:
        ps.append(p_val)
        rs.append(r_sq)
    if ax is None:
        fig = plt.figure()
        ax0 = plt.subplot(111)
    else:
        ax0 = ax
    ax0.scatter(rs, ps)
    ax0.plot([0, numpy.max(rs)], [0.05, 0.05], '--k')
    ax0.set_xlabel("r-squared")
    ax0.set_ylabel("p-val (all basis functions)")
    ax0.set_ylim(0, 0.2)

def plot_p_mass_vec_map(scorer, target_var, a1, a2, ax=None):
    data = scorer.full_score_data[target_var][(a1, a2)]
    ps = []
    mvs = []
    for [p_val, r_sq, basis_function, target_scores, basis_scores] in data:
        mass_vecs = basis_function.get_function_mass_angles()
        if mass_vecs is not None:
            for vec in mass_vecs:
                mvs.append(vec)
                ps.append(p_val)
    if ax is None:
        fig = plt.figure()
        ax0 = plt.subplot(111)
    else:
        ax0 = ax
    ax0.scatter(mvs, ps)
    ax0.plot([0, numpy.pi*2], [0.05, 0.05], '--k')
    ax0.set_xlabel("mass vector")
    ax0.set_ylim(0, 0.2)

def plot_p_area_map(scorer, target_var, a1, a2, ax=None):
    data = scorer.full_score_data[target_var][(a1, a2)]
    ps = []
    areas = []
    for [p_val, r_sq, basis_function, target_scores, basis_scores] in data:
        area = basis_function.get_function_area()
        areas.append(area[0])
        ps.append(p_val)
    if ax is None:
        fig = plt.figure()
        ax0 = plt.subplot(111)
    else:
        ax0 = ax
    ax0.scatter(areas, ps)
    ax0.plot([0, numpy.pi*4], [0.05, 0.05], '--k')
    ax0.set_xlabel("basis area")
    ax0.set_ylim(0, 0.2)

def plot_basis_with_pairwise_data_and_fit(basis_function, dataset, a1, a2, basis_scores, target_scores, title=""):
    fig = plt.figure(figsize=(12,6))
    fig.suptitle(title)
    ax0 = plt.subplot(212)
    coef = numpy.polyfit(basis_scores, target_scores, 1)
    poly1d_fn = numpy.poly1d(coef)

    ax0.scatter(basis_scores, target_scores)
    ax0.plot(basis_scores, poly1d_fn(basis_scores), '--k')

    X = sm.add_constant(basis_scores)
    est = sm.OLS(target_scores, X)
    est2 = est.fit()

    p_val = est2.f_pvalue
    r_sq = est2.rsquared

    ax0.set_xlabel("r^2: " + str(r_sq) + ", p-val: " + str(p_val))

    ax1 = plt.subplot(231)
    ax2 = plt.subplot(232, projection='polar')
    ax3 = plt.subplot(233)

    attribute_pair_thetas, attribute_pair_rs = dataset.get_pairwise_attributes_polar_values(a1, a2)
    ax2.scatter(attribute_pair_thetas, attribute_pair_rs, c='orange', alpha=0.1)

    basis_function.plot(ax1, ax2, ax3, attribute_pair=[a1, a2])

def plot_attribute_score_by_row(dataset, attr):
    y = list(dataset.full_orig_dataframe[attr])
    print(y)
    x = range(len(y))
    ry = []
    rx = []
    for i, yi in enumerate(y):
        if not re.match('\s+', str(yi)) and float(yi) > 0:
            ry.append(float(yi))
            rx.append(x[i])
    fig = plt.figure()
    fig.suptitle(attr)
    ax = plt.subplot(111)
    ax.plot(rx, ry, 'o')

def plot_all_targets_by_row(dataset):
    for target in dataset.target_vars:
        plot_attribute_score_by_row(dataset, target)