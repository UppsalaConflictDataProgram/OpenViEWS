""""""
import os
import sys

import json
import pickle

import pandas as pd
import numpy as np

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib import cm
import matplotlib.image as mpimg
from matplotlib.collections import LineCollection
from matplotlib.patches import Polygon
from mpl_toolkits.basemap import Basemap
from matplotlib.collections import PatchCollection

sys.path.append("../..")
import views_utils.dbutils as dbutils

# Data


class ScalableBox():
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.aspect_ratio = self.w / self.h

    def __str__(self):
        s = "w: {w} \th:{h} \tar:{ar}".format(w=self.w, h=self.h,
                                           ar=self.aspect_ratio)
        return s

    def scale_to_target_w(self, w):
        self.w = w
        self.h = w / self.aspect_ratio

    def scale_to_target_h(self, h):
        self.h = h
        self.w = h * self.aspect_ratio

def create_dirs(dirs):
    """Create a folder in locations supplied by each of the arguments"""
    for d in dirs:
        if not os.path.isdir(d):
            os.makedirs(d)
            print("Created directory", d)

def logit(p):
    return np.log(p/(1-p))

def get_df_actuals_event_coords(df_actuals, df_geo, varname_actual):
    df_actuals = df_actuals[[varname_actual]]
    df_actuals = df_actuals[df_actuals[varname_actual]==1]
    df = df_geo.merge(df_actuals, left_index=True, right_index=True)
    df = df[['longitude', 'latitude']]
    return df

def get_time_limits(df, timevar):
    times = df.index.get_level_values(timevar)
    start = int(times.min())
    end = int(times.max())
    return start, end

def prune_priogrid(df, rmin=110, rmax=256, cmin=324, cmax=464):
    """Defaults are sea-cells closesest to each tip of mainland Africa"""

    df = df[df['row']>= rmin]
    df = df[df['row']<= rmax]
    df = df[df['col']>= cmin]
    df = df[df['col']<= cmax]

    return df

def fetch_df_months(connectstring):
    q_months = """
    SELECT id, month, year_id
    FROM staging.month;
    """
    df_months = dbutils.query_to_df(connectstring, q_months)
    df_months.set_index(['id'], inplace=True)
    return df_months

def fetch_df_geo_pgm(connectstring):
    """Fetch df containing priogrid row/col and their lat/lon for subsetting"""
    schema = "staging"
    table = "priogrid"
    cols = ["gid", "row", "col", "latitude", "longitude", "in_africa"]
    df = dbutils.db_to_df(connectstring, schema, table, cols)
    df['pg_id'] = df['gid']
    del df['gid']
    df.set_index(['pg_id'], inplace=True)
    return df

def fetch_df_geo_c(crop):
    # corners
    if crop == "africa":
        A = {'longitude' : -18.25, 'latitude' : -34.75}
        B = {'longitude' : -18.25, 'latitude' : 37.75}
        C = {'longitude' : 51.75, 'latitude' : 37.75}
        D = {'longitude' : 51.75, 'latitude' : -34.75}
    else:
        A = {'longitude' : -180, 'latitude' : -57}
        B = {'longitude' : -180, 'latitude' : 85}
        C = {'longitude' : 180, 'latitude' : 85}
        D = {'longitude' : 180, 'latitude' : -57}
    df_geo = pd.DataFrame([A,B,C,D])
    return df_geo

def get_events_t(df_event_coords, t):
    df_event_coords_t = df_event_coords.loc[t]
    events_t = [tuple(x) for x in df_event_coords_t.values]
    return events_t

def get_var_bounds(df, varname):
    lower, upper = df[varname].min(), df[varname].max()
    plotvar_bounds = (lower, upper)
    return plotvar_bounds

def match_plotvar_actual(plotvar, verbose=False):
    if "_sb" in plotvar:
        actual = "ged_dummy_sb"
    elif "_ns" in plotvar:
        actual = "ged_dummy_ns"
    elif "_os" in plotvar:
        actual = "ged_dummy_os"
    elif "_pr" in plotvar:
        actual = "acled_dummy_pr"
    else:
        actual = None

    if verbose:
        print("Matched", plotvar, "to", actual)

    return actual

def make_plotjobs_table(connectstring, schema, table,
    schema_actual, table_actual, projection,
    groupvar, timevar, crop, run_id, variable_scale="logodds"):




    plotjobs = []

    varlist = dbutils.get_colnames_table(connectstring, schema, table)

    ids = [timevar, groupvar]

    # Drop the ids from the list of vars to plit
    varlist = [var for var in varlist if not var in ids]

    for plotvar in varlist:
        varname_actual = match_plotvar_actual(plotvar)

        plotjob = {
            "plotvar" : plotvar,
            "varname_actual" : varname_actual,
            "schema_plotvar" : schema,
            "table_plotvar"  : table,
            "schema_actual" : schema_actual,
            "table_actual"  : table_actual,
            "timevar"   : timevar,
            "groupvar"  : groupvar,
            "variable_scale" : variable_scale,
            "projection"     : projection,
            "crop"           : crop,
            "run_id"         : run_id
        }
        plotjobs.append(plotjob.copy())

    return plotjobs

def prob_to_pct(p):
    assert 0<p<1
    pct = p*100
    if pct == int(pct):
        pct = int(pct)
    pct = str(pct)
    pct += "%"
    return pct


# Plotting

def make_collection(map, df_plotvar_t, cmap, tick_values, variable_scale,
    plotvar_bounds, groupvar):
    patches = []
    colors = []

    if variable_scale=="logodds":
        df_plotvar_t = logit(df_plotvar_t)
    else:
        pass

    if groupvar == "country_id":
        for info, shape in zip(map.ID_info, map.ID):
            gid = info['ID']
            if gid in df_plotvar_t.index.values:
                prob = df_plotvar_t.loc[gid]
                patch = Polygon(np.array(shape), True)
                patches.append(patch)
                colors.append(prob)

    elif groupvar == "pg_id":
        for info, shape in zip(map.GID_info, map.GID):
            gid = info['GID']
            if gid in df_plotvar_t.index.values:
                prob = df_plotvar_t.loc[gid]
                patch = Polygon(np.array(shape), True)
                patches.append(patch)
                colors.append(prob)
    else:
        raise NotImplementedError

    collection = PatchCollection(patches, zorder=2)
    collection.set_array(np.array(colors).flatten())
    collection.set_cmap(cmap)


    # If we have custom tick values, set the ticks as the colorlimit
    if tick_values:
        collection.set_clim(np.min(tick_values), np.max(tick_values))
    else:
        collection.set_clim(plotvar_bounds[0], plotvar_bounds[1])

    return collection

def get_basemap_ortho(df_geo):
    longitude_mid = (df_geo.longitude.min() + df_geo.longitude.max()) / 2
    latitude_mid  = (df_geo.latitude.min()  + df_geo.latitude.max())  / 2
    map = Basemap(
        projection='ortho',
        lat_0 = latitude_mid,
        lon_0 = longitude_mid,
        suppress_ticks=True)
    return map

def get_basemap_cyl(df_geo):
    map = Basemap(
        llcrnrlon=df_geo.longitude.min(),
        llcrnrlat=df_geo.latitude.min(),
        urcrnrlon=df_geo.longitude.max(),
        urcrnrlat=df_geo.latitude.max(),
        resolution='i',
        projection='cyl',
        suppress_ticks=True)
    return map

def get_basemap_cyl_world():
    map = Basemap(
        llcrnrlon=-180,
        llcrnrlat=-57, #South tip of South America
        urcrnrlon=180,
        urcrnrlat=85,
        resolution='i',
        projection='cyl',
        suppress_ticks=False)
    return map

def get_basemap(projection, df_geo):
    if projection == "ortho":
        map = get_basemap_ortho(df_geo)
    elif projection == "cyl":
        map = get_basemap_cyl(df_geo)
    else:
        raise NotImplementedError

    return map

def plot_events_on_map(map, events):
    for event in events:
        x,y = map(event[0], event[1])
        map.plot(x, y, marker='.', color='black', label='event', markersize=10)
    return map

def make_ticks(variable_scale):
    def make_ticks_probs():
        ticks_strings = []
        ticks = [
            0.001,  0.01,   0.02,   0.05,
            0.1,    0.2,    0.3,    0.4,
            0.5,    0.6,    0.7,    0.8,
            0.9,    0.99]

        for tick in ticks:
            ticks_strings.append(str(tick))

        return  ticks, ticks_strings

    def make_ticks_logit():
        ticks_logit = []
        ticks_strings = []
        ticks = [
                0.001,   0.002,     0.005,
                0.01,    0.02,      0.05,   0.1,    0.2,
                0.4,     0.6,       0.8,    0.9,
                0.95,    0.99
                ]

        for tick in ticks:
            ticks_logit.append(logit(tick))
            ticks_strings.append(prob_to_pct(tick))

        clip_lower_bound = True
        if clip_lower_bound:
            ticks_strings[0] = "<= " + ticks_strings[0]

        return ticks_logit, ticks_strings


    if variable_scale=="logodds":
        values, labels = make_ticks_logit()
    elif variable_scale=="prob":
        values, labels = make_ticks_probs()
    elif variable_scale=="interval":
        values, labels = None, None
    else:
        msg = "Did you specify variable_scale?"
        raise RuntimeError(msg)

    ticks = {}
    ticks['values'] = values
    ticks['labels'] = labels
    return ticks
""
def month_id_to_datestr(df_months, month_id):
    datestr = str(df_months.loc[month_id]['year_id']) + "-" + str(df_months.loc[month_id]['month'])
    return datestr

def shifted_colormap(cmap, start=0, midpoint=0.5, stop=1.0,
    name='shiftedcmap'):
    '''
    Credit: #https://gist.github.com/phobson/7916777

    Function to offset the "center" of a colormap. Useful for
    data with a negative min and positive max and you want the
    middle of the colormap's dynamic range to be at zero

    Input
    -----
      cmap : The matplotlib colormap to be altered
      start : Offset from lowest point in the colormap's range.
          Defaults to 0.0 (no lower ofset). Should be between
          0.0 and 1.0.
      midpoint : The new center of the colormap. Defaults to
          0.5 (no shift). Should be between 0.0 and 1.0. In
          general, this should be  1 - vmax/(vmax + abs(vmin))
          For example if your data range from -15.0 to +5.0 and
          you want the center of the colormap at 0.0, `midpoint`
          should be set to  1 - 5/(5 + 15)) or 0.75
      stop : Offset from highets point in the colormap's range.
          Defaults to 1.0 (no upper ofset). Should be between
          0.0 and 1.0.
    '''
    cdict = {
        'red': [],
        'green': [],
        'blue': [],
        'alpha': []
    }

    # regular index to compute the colors
    reg_index = np.linspace(start, stop, 257)

    # shifted index to match the data
    shift_index = np.hstack([
        np.linspace(0.0, midpoint, 128, endpoint=False),
        np.linspace(midpoint, 1.0, 129, endpoint=True)
    ])

    for ri, si in zip(reg_index, shift_index):
        r, g, b, a = cmap(ri)

        cdict['red'].append((si, r, r))
        cdict['green'].append((si, g, g))
        cdict['blue'].append((si, b, b))
        cdict['alpha'].append((si, a, a))

    newcmap = matplotlib.colors.LinearSegmentedColormap(name, cdict)
    plt.register_cmap(cmap=newcmap)

    return newcmap

def get_figure_size(df, scale=0.5):
    """scale=0.5 gives 0.5 inches per degree"""
    lon_min = df.longitude.min()
    lon_max = df.longitude.max()
    lat_min = df.latitude.min()
    lat_max = df.latitude.max()
    width = lon_max - lon_min
    height = lat_max - lat_min
    size = (width*scale, height*scale)

    print("lon_min: ", lon_min)
    print("lon_max: ", lon_max)
    print("lat_min: ", lat_min)
    print("lat_max: ", lat_max)

    return size



def get_cmap(variable_scale, dump=False):
    name_cmap="rainbow"
    cmap = plt.get_cmap(name_cmap)

    # Defaults
    start=0.0
    mid=0.5
    stop=1.0

    # If we're using probs set mid of cmap at 1%
    if variable_scale=="prob":
        mid=0.01

    if variable_scale=="logodds":
        mid=0.25

    cmap = plt.get_cmap(name_cmap)
    cmap = shifted_colormap(cmap, start, mid, stop)

    if dump:
        if variable_scale:
            suffix = variable_scale
        else:
            suffix = "interval"
        path = "./cmap_{}.json".format(suffix)
        segmentdata = cmap._segmentdata
        with open(path, 'w') as f:
            json.dump(segmentdata, f)
        print("Wrote", path)


    return cmap

def restrict_prob_lower_bound(df, bound):
    df[df<bound] = bound
    return df

def plot_map_worker(local_settings, plotjob):

    connectstring = local_settings['connectstring']
    dir_plots = local_settings['dir_plots']
    dir_spatial_pgm = local_settings['dir_spatial_pgm']
    dir_spatial_cm = local_settings['dir_spatial_cm']

    plotvar         = plotjob['plotvar']
    varname_actual  = plotjob['varname_actual']
    schema_plotvar  = plotjob['schema_plotvar']
    schema_actual   = plotjob['schema_actual']
    table_plotvar   = plotjob['table_plotvar']
    table_actual    = plotjob['table_actual']
    timevar         = plotjob['timevar']
    groupvar        = plotjob['groupvar']
    variable_scale  = plotjob['variable_scale']
    projection      = plotjob['projection']
    crop            = plotjob['crop']
    run_id          = plotjob['run_id']

    path_shape_pg = dir_spatial_pgm + "/priogrid"
    path_shape_c = dir_spatial_cm + "/country"

    ids = [timevar, groupvar]

    print("Plotting variable {} from table {}.{}".format(plotvar,
        schema_plotvar, table_plotvar))

    print(json.dumps(plotjob, indent=4))

    df_plotvar = dbutils.db_to_df(connectstring, schema_plotvar, table_plotvar,
        [plotvar], ids)

    df_plotvar = restrict_prob_lower_bound(df_plotvar, 0.001)

    time_start, time_end = get_time_limits(df_plotvar, timevar)
    print("time_start:", time_start)
    print("time_end:", time_end)

    have_actual=False
    if varname_actual is not None:
        have_actual=True

    if groupvar == "pg_id":
        df_geo = fetch_df_geo_pgm(connectstring)
        df_geo = prune_priogrid(df_geo)
        size = get_figure_size(df_geo, scale=0.6)

    if have_actual and groupvar == "pg_id":
        df_actuals = dbutils.db_to_df_limited(connectstring, schema_actual,
                                               table_actual, [varname_actual],
                                               timevar, groupvar,
                                               time_start, time_end)

        df_event_coords = get_df_actuals_event_coords(df_actuals, df_geo,
                                                          varname_actual)


    elif groupvar == "country_id":
        df_geo = fetch_df_geo_c(crop)
        size = get_figure_size(df_geo, scale=0.6)

    if timevar == 'month_id':
        df_months = fetch_df_months(connectstring)

    plotvar_bounds = get_var_bounds(df_plotvar, plotvar)
    print("Bounds: ", plotvar_bounds)
    times = range(time_start, time_end+1)

    cmap = get_cmap(variable_scale)


    ticks = make_ticks(variable_scale)

    dir_schema  = dir_plots  + schema_plotvar + "/"
    dir_table   = dir_schema + table_plotvar  + "/"
    dir_plotvar = dir_table  + plotvar        + "/"
    create_dirs([dir_plots, dir_schema, dir_table, dir_plotvar])

    for t in times:
        print("Plotting for {}".format(t))
        df_plotvar_t = df_plotvar.loc[t]

        #fig = plt.figure(figsize = size)
        fig, ax = plt.subplots(figsize = size)

        print("Making basemap")
        map = get_basemap(projection, df_geo)

        print("Reading shape")

        if groupvar == "pg_id":
            map.readshapefile(path_shape_pg, 'GID', drawbounds=False)

        if groupvar == "country_id":
            map.readshapefile(path_shape_c, 'ID', drawbounds=False)

        if groupvar == "pg_id" and have_actual:
            events_t = get_events_t(df_event_coords, t)
            map = plot_events_on_map(map, events_t)

        print("Making collection")
        # Plot the probs
        collection = make_collection(map,
                                     df_plotvar_t,
                                     cmap,
                                     ticks['values'],
                                     variable_scale,
                                     plotvar_bounds,
                                     groupvar)
        ax.add_collection(collection)

        if groupvar == "pg_id":
           # The Africa limited shapefile
            map.readshapefile(path_shape_pg, 'GID', drawbounds=True)


        cbar_fontsize = size[1]/2

        if variable_scale in ["logodds", "prob"]:
            # if we're plotting logodds or probs set custom ticks
            cbar = plt.colorbar(collection,
                                ticks=ticks['values'],
                                fraction=0.046,
                                pad=0.04)
            cbar.ax.set_yticklabels(ticks['labels'], size=cbar_fontsize)
        else:
            # else use default colorbar for interval variables
            cbar = plt.colorbar(collection)

        map.drawmapboundary()

        if groupvar == "pg_id":
            map.readshapefile(path_shape_pg, 'GID', drawbounds=True)
            map.readshapefile(path_shape_c, 'ID', drawbounds=True, color='w',
                linewidth = 2)
            map.readshapefile(path_shape_c, 'ID', drawbounds=True, color='k',
                linewidth = 1)
        elif groupvar == "country_id":
            map.readshapefile(path_shape_c, 'ID', drawbounds=True)


        s_t_plotvar = "{}.{}".format(schema_plotvar, table_plotvar)
        text_box = "Modelname: {}\nRun: {}\nTable: {}".format(plotvar,
                                                                 run_id,
                                                                 s_t_plotvar)
        bbox = {'boxstyle' : 'square',  'facecolor' : "white"}
        lon_min = df_geo['longitude'].min()
        lon_max = df_geo['longitude'].max()
        lat_min = df_geo['latitude'].min()
        lat_max = df_geo['latitude'].max()

        w_eu = 6.705
        h_eu = 4.5
        w_erc = 4.7109375
        h_erc = 4.5
        w_views = w_eu + w_erc + 1
        h_views = 4.024

        lon_start_eu = lon_min + 1
        lon_end_eu = lon_start_eu + w_eu
        lon_start_erc = lon_end_eu + 1
        lon_end_erc = lon_start_erc + w_erc
        lon_start_views = lon_start_eu
        lon_end_views = lon_end_erc

        lat_start_eu = lat_min + 1
        lat_end_eu = lat_start_eu + h_eu
        lat_start_erc = lat_start_eu
        lat_end_erc = lat_start_erc + h_erc
        lat_start_views = lat_end_eu + 1
        lat_end_views = lat_start_views + h_views

        lon_min_textbox = lon_start_views
        lat_min_textbox = lat_end_views + 1

        box_logo_eu     = (lon_start_eu, lon_end_eu,
                           lat_start_eu, lat_end_eu)
        box_logo_erc    = (lon_start_erc, lon_end_erc,
                           lat_start_erc, lat_end_erc)
        box_logo_views  = (lon_start_views, lon_end_views,
                           lat_start_views, lat_end_views)

        plt.text(lon_min_textbox, lat_min_textbox,
                 text_box, bbox=bbox, fontsize=size[1]*0.5)

        logo_eu = mpimg.imread("/storage/static/logos/eu.png")
        logo_erc = mpimg.imread("/storage/static/logos/erc.png")
        logo_views = mpimg.imread("/storage/static/logos/views.png")

        plt.imshow(logo_erc, extent = box_logo_erc)
        plt.imshow(logo_eu, extent = box_logo_eu)
        plt.imshow(logo_views, extent = box_logo_views)

        text_title = "TITLE"
        if timevar == 'month_id':
            text_title = month_id_to_datestr(df_months, t)
        plt.figtext(0.5, 0.85, text_title, fontsize=size[1], ha='center')

        path = dir_plotvar + str(t) + ".png"
        plt.savefig(path, bbox_inches="tight")
        print("wrote", path)
        plt.close()

