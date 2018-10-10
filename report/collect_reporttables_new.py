'''Monthly reporting using template engine
RBJ 20-07-2018
'''

# TO DO
# remove all temporary local, get from storage/current (pipeline)
# add pr for acled 
# documentation, extend comments
# redirect paths to templates

import argparse
import os
import jinja2

latex_jinja_env = jinja2.Environment(
    block_start_string='\BLOCK{',
    block_end_string='}',
    variable_start_string='\VAR{',
    variable_end_string='}',
    comment_start_string='\#{',
    comment_end_string='}',
    line_statement_prefix='%%',
    line_comment_prefix='%#',
    trim_blocks=True,
    autoescape=False,
    loader=jinja2.FileSystemLoader(os.path.abspath('/'))
)

latex_jinja_env.globals.update(zip=zip)

# get current working directory
cwd = os.getcwd()

# argparse runid argument, specify in bash w/ e.g. --run_id "r.2018.07.01"
parser = argparse.ArgumentParser()
parser.add_argument("--run_id", type=str,
                    help="Run ID")

args = parser.parse_args()

runid = args.run_id

# specify directories
source = "/storage/runs/current"
dir_output = ""

# Specify which months to produce in maps
# @ add full month name connection to monthid
fcast_m = 464
decay_m = fcast_m - 2
fcast_m_name = "August 2018"
decay_m_name = "June 2018"

# Open file object to write, ensemble results:
out_ens_cm = open(runid + "/results_ensemble_cm.tex", "w+")
out_ens_pgm = open(runid + "/results_ensemble_pgm.tex", "w+")
out_heat = open(runid + "/results_heatmap.tex", "w+")
out_dec = open(runid + "/decayfunctions.tex", "w+")

# Extended report:
out_cm = open(runid + "/reporttables_cm.tex", "w+")
out_pgm = open(runid + "/reporttables_pgm.tex", "w+")

# Loop elements
mode = ["ds", "osa"] #a
level = ["cm", "pgm"] #b
dat = ["canon", "acled"] #c
ref = ["wcm", "nocm"] #d
frame = ["fcast", "eval"] #e
vtype = ["sb", "ns", "os"] #f
dtype = vtype + ["pr"]
stat = ["logit", "rf"] #g
osa_months = [1, 6, 12, 36]
captions = ["State-based conflict (sb)",
            "Non-state conflict (ns)",
            "One-sided violence (os)"]
dcaptions = captions + ["Protests (pr)"]

# @TODO: redirect paths
subfig_template = '{}/templates/subfig_template.tex'.format(cwd)
decay_template = '{}/templates/decay_template.tex'.format(cwd)
heatmap_template = '{}/templates/heatmap_template.tex'.format(cwd)
extreport_body_template = '{}/templates/extreport_body_template.tex'.format(cwd)
extreport_header_template = '{}/templates/extreport_header_template.tex'.format(cwd)
rf_template = '{}/templates/rf_template.tex'.format(cwd)

# Functions (@TODO merge into one, see previous comment)
# subdirectory as variable as I figured that might be changed 
def writetex_subfig(subdirectory, level):
    '''writes general sb/ns/os maps figures'''
    template = latex_jinja_env.get_template(subfig_template)
    render = template.render(source=source, subdirectory=subdirectory,
                             fcast_m=fcast_m, fcast_m_name=fcast_m_name,
                             level=level, vtype=vtype, captions=captions)
    return render

def writetex_decay(subdirectory):
    '''writes decay function maps (4)'''
    template = latex_jinja_env.get_template(decay_template)
    render = template.render(source=source, subdirectory=subdirectory,
                             decay_m=decay_m, decay_m_name=decay_m_name,
                             level=level, dtype=dtype, captions=dcaptions)
    return render

def writetex_heatmap(subdirectory):
    '''writes heatmap figures sb/ns/os'''
    template = latex_jinja_env.get_template(heatmap_template)
    render = template.render(source=source, subdirectory=subdirectory,
                             fcast_m=fcast_m, fcast_m_name=fcast_m_name,
                             level=level, vtype=vtype, captions=captions)
    return render

def writetex_er_headers(subdirectory, level, osa):
    '''writes headers per subsection extended report.'''
    # breaks for particular cases, figures:
    levelbreak = "base" if level == "cm" else d
    if osa == "logit":
        osabreak = "logit_fullsample_"
    elif osa == "rf":
        osabreak = "rf_downsampled_"
    else:
        osabreak = ""
    template = latex_jinja_env.get_template(extreport_header_template)
    render = template.render(a=a, c=c, g=g, levelbreak=levelbreak,
                             osabreak=osabreak, source=source,
                             subdirectory=subdirectory,
                             fcast_m=fcast_m, fcast_m_name=fcast_m_name,
                             level=level, vtype=vtype, captions=captions)
    return render

def writetex_er_tables(level, osa):
    '''Writes subsections for extended monthly report.'''
    # breaks for particular cases, tables:
    levelbreak = "base" if level == "cm" else d
    osabr1 = "osa" if osa == "logit" or osa == "rf" else ""
    if osa == "logit":
        osabr2 = "logit_fullsample"
        osabr3 = "1_regtab.tex"
    elif osa == "rf":
        osabr2 = "rf_downsampled"
        osabr3 = "featimp.png"
    else:
        osabr2 = ""
        osabr3 = ""
    # subfunction for the rf feature importance plots
    def writetex_rf(subdirectory):
        '''writes rf feature importance plots'''
        template = latex_jinja_env.get_template(rf_template)
        render = template.render(source=source, subdirectory=subdirectory,
                                 level=level,
                                 osa_months=osa_months, c=c, levelbreak=levelbreak,
                                 e=e, osabr2=osabr2, f=f, osabr3=osabr3)
        return render
    # render template
    if osa == "" or osa == "logit":
        template = latex_jinja_env.get_template(extreport_body_template)
        render = template.render(a=a, c=c, g=g, e=e, f=f,
                                 levelbreak=levelbreak, osabr1=osabr1, osabr2=osabr2,
                                 osabr3=osabr3, source=source, fcast_m=fcast_m,
                                 frame=frame, fcast_m_name=fcast_m_name, level=level,
                                 vtype=vtype, captions=captions, osa=osa)
    else:
        render = writetex_rf("/plot/featimps".format(source, a))
    return render


# Write to file @TODO fix subdirectory to something more sensible

# Produce .tex files for monthly report of ensemble results
# country-month
out_ens_cm.write(writetex_subfig(
    "/maps/landed/ensemble_cm_fcast_test/average_", "cm"))
out_ens_cm.close()

# pgm
out_ens_pgm.write(writetex_subfig(
    "/maps/landed/ensemble_pgm_fcast_test/average_calib_select_", "pgm"))
out_ens_pgm.close()

# add heatmaps
out_heat.write(writetex_heatmap("/plot/heatmaps/"))
out_heat.close()

# add decay function maps
out_dec.write(writetex_decay(
    "/maps/launched/transforms_pgm_imp_1/decay_12_cw_ged_dummy_"))
out_dec.close()

# Produce .tex files for monthly extended appendix
# country-month
for a in mode:
    for c in dat:
        if a == "ds":
            g = ""
            out_cm.write(writetex_er_headers("maps/landed/calibrated_cm_fcast_test/",
                                             "cm", ""))
            for e in frame:
                if c == "acled":
                    for f in dtype:
                        out_cm.write(writetex_er_tables("cm", ""))
                else:
                    for f in vtype:
                        out_cm.write(writetex_er_tables("cm", ""))
        else:
            for g in stat:
                if g == "logit":
                    out_cm.write(writetex_er_headers(
                        "maps/landed/calibrated_cm_fcast_test/", "cm", "logit"))
                    for e in frame:
                        if c == "acled":
                            for f in dtype:
                                out_cm.write(writetex_er_tables("cm", "logit"))
                        else: 
                            for f in vtype:
                                out_cm.write(writetex_er_tables("cm", "logit"))
                else:
                    out_cm.write(writetex_er_headers(
                        "maps/landed/calibrated_cm_fcast_test/", "cm", "rf"))
                    for e in frame:
                        if c == "acled":
                            for f in dtype:
                                out_cm.write(writetex_er_tables("cm", "rf"))
                        else: 
                            for f in vtype:
                                out_cm.write(writetex_er_tables("cm", "rf"))
out_cm.close()

# pgm-level
for a in mode:
    for c in dat:
        for d in ref:
            if a == "ds":
                out_pgm.write(writetex_er_headers("maps/landed/calibrated_pgm_fcast_test/", 
                                                  "pgm", ""))
                for e in frame:
                    if c == "acled":
                        for f in dtype:
                            out_pgm.write(writetex_er_tables("pgm", ""))
                    else:
                        for f in vtype:
                            out_pgm.write(writetex_er_tables("pgm", ""))
            else:
                for g in stat:
                    if g == "logit":
                        out_pgm.write(writetex_er_headers(
                            "maps/landed/calibrated_pgm_fcast_test/", "pgm", "logit"))
                        for e in frame:
                            if c == "acled":
                                for f in dtype:
                                    out_pgm.write(writetex_er_tables("pgm", "logit"))
                            else:
                                for f in vtype:
                                    out_pgm.write(writetex_er_tables("pgm", "logit"))
                    else:
                        out_pgm.write(writetex_er_headers(
                            "maps/landed/calibrated_pgm_fcast_test/", "pgm", "rf"))
                        for e in frame:
                            if c == "acled":
                                for f in dtype:
                                    out_pgm.write(writetex_er_tables("pgm", "rf"))
                            else:
                                for f in vtype:
                                    out_pgm.write(writetex_er_tables("pgm", "rf"))
out_pgm.close()
