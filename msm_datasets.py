#!/usr/bin/env python

__all__ = [
    "datasets", "namekey", "topologies",
    "workflows", "reference", "heavies",
    "protein", "alphies",
]

prot_name = "chignolin"

heavies = "mass > 5"
alphies = "name CA"
protein = "protein"

top_protein = "%s-protein.pdb" % prot_name
top_heavies = "%s-heavy.pdb" % prot_name

topologies = {
    heavies: top_heavies,
    protein: top_protein,
    alphies: None,
}

reference = {heavies: "%s-folded.pdb" % prot_name}


omm = {
    "timestep"  : 0.020,# of saved frames, unit: nanosecond
    "topfile"   : top_protein,
    "selection" : protein,
    "directory" : "./",
    "filename"  : "protein.*-*.dcd",
    "n_trajs"   : 1,# how many per workload?
}

atn = {
    "timestep"  : 0.200,# of saved frames, unit: nanosecond
    "directory" : './',
    "selection" : heavies,
    "topfile"   : top_heavies,
    "filename"  : "%s-anton-fixed-0.dcd" % prot_name,
    "n_trajs"   : 1,# how many per workload?
}

xma_CB = {
    "timestep"  : 0.020,# of saved frames, unit: nanosecond
    "topfile"   : top_protein,
    "directory" : "",
    "filename"  : "cgn-CaBa/trajs/*/protein.dcd",
    "selection" : protein,
    "database"  : 'mongo',
    "projectname": 'cgn-CaBa',
    "n_trajs"   : 24,# how many per workload?
    "first"     : 0,# first traj idx for these workloads
    "last"      : 120,# last  traj idx for these workloads
}

xma_Ca = {
  "timestep"  : 0.020,# of saved frames, unit: nanosecond
  "topfile"   : top_protein,
  "filename"  : "cgn-Ca/trajs/*/protein.dcd",
  "directory" : "",
  "selection" : protein,
  "database"  : 'mongo',
  "projectname": 'cgn-Ca',
  "n_trajs"   : 24,# how many per workload?
  "first"     : 0,# first traj idx for these workloads
  "last"      : 120,# last  traj idx for these workloads
}

umi_Ca = {
  "timestep"  : 0.020,# of saved frames, unit: nanosecond
  "topfile"   : top_protein,
  "filename"  : "cgn-Ca/trajs/*/protein.dcd",
  "directory" : "",
  "selection" : protein,
  "database"  : 'mongo',
  "projectname": 'cgn-Ca',
  "n_trajs"   : 12,# how many per workload?
  "first"     : 120,# first traj idx for these workloads
  #"last"      : 12,# last  traj idx for these workloads
}

umi_CB = {
  "timestep"   : 0.020,# of saved frames, unit: nanosecond
  "topfile"    : top_protein,
  "filename"   : "cgn-CaBa/trajs/*/protein.dcd",
  "directory"  : "",
  "selection"  : protein,
  "database"   : 'mongo',
  "projectname": 'cgn-CaBa',
  "n_trajs"    : 12,# how many per workload?
  "first"      : 120,# first traj idx for these workloads
  #"last"      : 12,# last  traj idx for these workloads
}

workflows = {
    "atn"    : atn,
    "omm"    : omm,
    # Next are from actual workflows
    "xma_Ca" : xma_Ca,
    "xma_CB" : xma_CB,
    "umi_Ca" : umi_Ca,
    "umi_CB" : umi_CB,
}

datasets = {
    # This is the 'reference state'
    "reference"    : reference,
    "topologies"   : topologies,
    # Next 2 are single long trajs
    "workflows"    : workflows,
}

namekey = '-stride-'



# See workup in notebook for how these
# parameters were chosen. After we tune
# up our model-building we save it for
# later use.
anton_model = {
    "directory" : "analysis",
    "steps" : {
        "tica"       : None,
        "clustering" : None,
        "msm"        : None,
        "cgmsm"      : None
    }
}
#    "master_analysis" : {
#        "atomselection"   : "element C or element N or element O or element S",
#        "features"        : "inverse_distances",
#        "topfile"         : at['reference'],
#        "dim_reduction"   : {
#            "tica" : {
#                "lag"    : ticalag, # 200 steps = 40 ns in Anton Frames
#                "stride" : 1,
#                "dim"    : ndim,
#                "reversible": True,
#                #"kinetic_map": True, # Default is True
#                #"commute_map": True, # Default is False
#        }},
#        "clustering"      : {
#            "cluster_kmeans" : {
#                "k"         : clusts,
#                "max_iter"  : 150,
#                "stride"    : 1,
#        }},
#        "msm"      : {
#            #"estimate_markov_model" : {
#            "bayesian_markov_model" : {
#                #"reversible": True,
#                "lag"       : ticalag,
#        }},
#        "cgmsm"      : {
#            "bayesian_hidden_markov_model" : {
#                #"reversible": True,
#                "lag"       : ticalag,
#                #"stride"    : 50,
#        }},
#    },
