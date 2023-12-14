"""
Script that reads configuration in yaml format from config.yml file
config.yml - file that might be changed during building stage
"""
import os
import yaml


with open(os.environ.get('ANSIBLE_RUNNER_CONFIG_PASS', './config.yml'), 'r') as file:
    GLOBAL_CONFIG = yaml.safe_load(file)
