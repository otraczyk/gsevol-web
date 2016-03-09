# -*- coding: utf-8 -*
"""
Parse csv with option list and populate database table `styling_options`.

This script is meant for (mostly) dev environment runs, patching
would be necessary in case of errors.
"""
import csv
from styling.models import Option

def fix_bool_values(val_dict):
    for key in ["gene", "species", "mapping", "scenario", "diagram"]:
        val_dict[key] = bool(int(val_dict[key]))

def run(*args, **kwargs):
    with open("styling/scripts/variables-clean.csv") as opt_file:
        opt_list = csv.DictReader(opt_file, delimiter='\t', quotechar="'",
                                  restval='')
        for values in opt_list:
            try:
                fix_bool_values(values)
                opt = Option.objects.create(**values)
            except Exception as e:
                import ipdb; ipdb.set_trace()

