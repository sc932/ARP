import pandas as pd
import numpy
import re
from collections import defaultdict
import pprint
import matplotlib.pyplot as plt

import yaml
import logging

import utils

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

class Dataset(object):
  def __init__(self, dataset_yml):
    logging.info("Loading config file from: " + dataset_yml)
    with open(dataset_yml, 'r') as file:
      self.dataset_config = yaml.safe_load(file)
      logging.info("Config file loaded from: " + dataset_yml)

    self.csv_file_name = self.dataset_config['csv_file_name']
    logging.info("Loading dataset from: " + self.csv_file_name)
    self.full_orig_dataframe = pd.read_csv(self.csv_file_name)
    logging.info("Dataset loaded from: " + self.csv_file_name)

    self.team_idx_name = self.dataset_config['team_index']
    self.target_vars = list(self.dataset_config['target_vars'])

    self.load_attr_lists()
    self.clean_out_blanks()
    self.normalize_data()

  def get_team_ids(self):
    return list(set(self.normalized_dataframe[self.team_idx_name]))
  
  def get_team_ids_with_target(self, target_var):
    team_ids = []
    for team_id in self.get_team_ids():
      if self.get_member_attributes_by_team_id(team_id, target_var) is not None:
        team_ids.append(team_id)
    return team_ids
  
  def get_member_attributes_by_team_id(self, team_id, attr):
    members = self.normalized_dataframe.loc[self.normalized_dataframe[self.team_idx_name] == team_id]
    
    if self.dataset_config['missing_values']['spaces']:
      for member_val in members[attr]:
        if re.match('\s+', str(member_val)):
          # invalidate team, doesn't have the target var for at least one member
          return None
    return list(members[attr])

  def get_pairwise_attributes_polar_values(self, a1, a2):
    attribute_pair_thetas = []
    attribute_pair_rs = []
    team_ids = self.get_team_ids()
    for team_id in team_ids:
      attr1_vals = self.get_member_attributes_by_team_id(team_id, a1)
      attr2_vals = self.get_member_attributes_by_team_id(team_id, a2)
      for i in range(len(attr1_vals)):
        x = attr1_vals[i]
        y = attr2_vals[i]
        r, theta = utils.polar_from_x_y(x, y, x_offset=self.attr_means[a1], y_offset=self.attr_means[a2])
        attribute_pair_thetas.append(theta)
        attribute_pair_rs.append(r)
    return attribute_pair_thetas, attribute_pair_rs

  def load_attr_lists(self):
    self.combined_attr_list = []

    self.big_five_mapping = dict(self.dataset_config['big_five'])
    self.big_five_reverse_mapping = {v: k for k, v in self.big_five_mapping.items()}
    self.big_five_attr_list = list(self.big_five_mapping.values())
    self.combined_attr_list.extend(self.big_five_attr_list)

    self.pos_attr_list = self.dataset_config['pos_attrs']
    self.combined_attr_list.extend(self.pos_attr_list)

    self.neg_attr_list = self.dataset_config['neg_attrs']
    self.combined_attr_list.extend(self.neg_attr_list)

    self.neutral_attr_list = self.dataset_config['neutral_attrs']
    self.combined_attr_list.extend(self.neutral_attr_list)

    self.cog_attr_list = self.dataset_config['cog_attrs']
    self.combined_attr_list.extend(self.cog_attr_list)

    logging.debug("Loaded the following attrs: " + str(self.combined_attr_list))


  def normalize_data(self):
    self.attr_means = {}
    self.attr_medians = {}
    self.drop_rows = []
    self.normalized_dataframe = self.clean_dataframe.copy()
    for attr in self.combined_attr_list:
      self.normalized_dataframe[attr] = self.clean_dataframe[attr].astype(float)
      max = -numpy.inf
      min = numpy.inf
      running_values = []
      for i, member in self.normalized_dataframe.iterrows():
        #logging.debug(member[attr])
        attr_val = float(member[attr])
        if not attr_val < 0:
          if attr_val < min:
            min = attr_val
          if attr_val > max:
            max = attr_val
        elif attr in self.cog_attr_list:
          logging.warning("Found negative attribute, dropping row: " + str(i))
          self.drop_rows.append(i)
      
      for i, member in self.normalized_dataframe.iterrows():
          attr_val = float(member[attr])
          if not attr_val < 0:
            # TODO LOOK BACK AT THIS
            #if attr == self.big_five_mapping['Neurotic']:
            #  attr_val = max - attr_val
            remapped_attr_val = (attr_val - min)/(max - min)
            self.normalized_dataframe.loc[i, attr] = remapped_attr_val
            running_values.append(remapped_attr_val)
          elif attr in self.cog_attr_list:
            logging.warning("Found negative attribute, dropping row: " + str(i))
            self.drop_rows.append(i)

      self.attr_means[attr] = numpy.mean(numpy.array(running_values))
      self.attr_medians[attr] = numpy.median(numpy.array(running_values))
      logging.debug("Normalized attribute: " + attr + " mean: " + str(self.attr_means[attr]) + " median: " + str(self.attr_medians[attr]))

    logging.info("Normalized all attributes")

    self.goal_means = {}
    self.goal_medians = {}
    for target in self.target_vars:
      running_values = []
      for i, member in self.normalized_dataframe.iterrows():
        if isinstance(member[target], str):
          goal = float(member[target].zfill(10))
        else:
          goal = float(member[target])
        if not goal < 0:
          running_values.append(goal)
        else:
          # remove unscored teams
          self.drop_rows.append(i)
          logging.warning("Found negative attribute, dropping row: " + str(i))
        #self.normalized_dataframe[target][i] = goal
        self.normalized_dataframe.loc[i, target] = goal

      if len(self.drop_rows) > 0:
        logging.warning("Found bad goal value, dropping row: " + str(self.drop_rows))
        self.normalized_dataframe = self.normalized_dataframe.drop(self.normalized_dataframe.index[self.drop_rows])

      running_values = numpy.array(running_values)
      min_goal = numpy.min(running_values)
      max_goal = numpy.max(running_values)
      remapped_goal_val = (self.normalized_dataframe[target] - min_goal) / (max_goal - min_goal)
      self.normalized_dataframe[target] = remapped_goal_val
      mean = numpy.mean(self.normalized_dataframe[target])
      median = numpy.median(self.normalized_dataframe[target])
      self.goal_means[target] = mean
      self.goal_medians[target] = median
      logging.debug("Normalized target variable: " + target + " mean: " + str(mean) + " median: " + str(median))

    logging.info("Normalized all target variables")

  def clean_out_blanks(self, spaces=None, cog_attr_vals=None, other_vals=None):
    if spaces == None:
      spaces = self.dataset_config['missing_values']['spaces']
    else:
      spaces = False
    logging.debug("Looking for spaces: " + str(spaces))

    if cog_attr_vals == None:
      cog_attr_vals = self.dataset_config['missing_values']['cog_attr_vals']
    else:
      cog_attr_vals = []
    logging.debug("Removing these cog_attr_vals: " + str(cog_attr_vals))

    if other_vals == None:
      other_vals = self.dataset_config['missing_values']['other_vals']
    else:
      other_vals = []
    logging.debug("Removing these other vals: " + str(other_vals))

    self.team_diqualifications_by_attr = defaultdict(list)
    self.member_diqualifications_by_attr = defaultdict(list)

    teams_to_delete = []

    for i, member in self.full_orig_dataframe.iterrows():
      logging.debug("Reviewing member: " + str(i))
      logging.debug(str(member))
      if 'team_index_cap' in self.dataset_config:
        if int(member[self.team_idx_name]) > self.dataset_config['team_index_cap']:
          teams_to_delete.append(member[self.team_idx_name])
          continue
      for attr in self.combined_attr_list:
        if numpy.isnan(member[attr]):
          self.team_diqualifications_by_attr[attr].append(member[self.team_idx_name])
          self.member_diqualifications_by_attr[attr].append(i)
          self.full_orig_dataframe[attr][i] = -1
          teams_to_delete.append(member[self.team_idx_name])
        if spaces and re.match('\s+', str(member[attr])):
          self.team_diqualifications_by_attr[attr].append(member[self.team_idx_name])
          self.member_diqualifications_by_attr[attr].append(i)
          self.full_orig_dataframe[attr][i] = -1
          teams_to_delete.append(member[self.team_idx_name])
        for bad_val in other_vals:
          if float(bad_val) == member[attr]:
            self.team_diqualifications_by_attr[attr].append(member[self.team_idx_name])
            self.member_diqualifications_by_attr[attr].append(i)
            self.full_orig_dataframe[attr][i] = -1
            teams_to_delete.append(member[self.team_idx_name])
        for cog_attr_val in cog_attr_vals:
          if attr in self.cog_attr_list and str(member[attr]) == cog_attr_val:
            self.team_diqualifications_by_attr[attr].append(member[self.team_idx_name])
            self.member_diqualifications_by_attr[attr].append(i)
            self.full_orig_dataframe[attr][i] = -1
            teams_to_delete.append(member[self.team_idx_name])

    if len(teams_to_delete) > 0:
      logging.debug("DISQUALIFIED TEAMS")
      logging.debug(teams_to_delete)

      self.drop_rows = []
      for i, member in self.full_orig_dataframe.iterrows():
        if member[self.team_idx_name] in teams_to_delete:
          self.drop_rows.append(i)

      self.clean_dataframe = self.full_orig_dataframe.drop(self.full_orig_dataframe.index[self.drop_rows])
    else:
      self.clean_dataframe = self.full_orig_dataframe.copy()

    logging.info("Cleaned out " + str(len(teams_to_delete)) + " teams")