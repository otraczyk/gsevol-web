"""Collection of 'core functions' to be run inside celery tasks (or from views).
"""
from bindings import gsevol as Gse
from bindings import urec as Urec


def draw_gene_species_mapping(gene, species):
    gtree, stree, mapping = Gse.draw_trees(gene, species)
    return {"gene": gtree, "species": stree, "mapping": mapping}

def all_scenarios(gene, species):
    return {"scenarios": Gse.scenarios(gene, species)}

def opt_scen(gene, species):
    optimal = Gse.optscen(gene, species)
    return {
        "optscen": {
            'scen': optimal,
            'pic': Gse.draw_embedding(species, optimal)
            }
        }
