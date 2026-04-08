import geopandas as gpd
import pandas as pd
import folium
import mapclassify
import numpy as np
#from shapely.geometry import Point, LineString, Polygon
import matplotlib.pyplot as plt
import math
import seaborn as sns
import contextily as cx
import matplotlib
import ezdxf
from shapely import from_wkt
from shapely.geometry import box



import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)
def streets_social_sdataset(
    uf,
    streets_m,
    urban_function_id,
    urban_function_type_name,
    morpho_metrics_list_cols,
    functions_subgroup_col_name = None,
    functions_subgroup_col_alias=None,
    save_file = ("csv","geojson", "none"),
    package =["Basic", "Basic_plus", "Advanced", "Advanced_plus", "All"]
    ):

  def richness(group):
    group = group.drop_duplicates(subset=urban_function_id, keep='first')
    return group[urban_function_type_name].nunique()

  def shannon_wiener_diversity(group):
    group = group.drop_duplicates(subset=urban_function_id, keep='first')
    proportions = group[urban_function_type_name].value_counts(normalize=True)
    proportions = proportions[proportions > 0]
    return -np.sum(proportions * np.log(proportions))

  def normalize(data, col):
    data[f"norm_{col}"]= 0
    data[f"norm_{col}"] = data[f"norm_{col}"].astype("float")
    QiM = data[col].max()
    for r in range(len(data)):
      I1 = data.loc[r, col]
      data.loc[r, f"norm_{col}"] =  (I1-data[col].min())/(QiM-data[col].min())
    next
    return data

  #1 data prep
  uf= uf.to_crs(epsg=3857)
  streets_m = streets_m.to_crs(epsg=3857)

  #3_attributing the street-network dataset with diversity scores


  #3_1_specifying the street space area by buffering each street segment
  streets_m["buffer1"] = streets_m.buffer(35)
  streets_diversity = streets_m.set_geometry("buffer1")
  locations_in_buffer = gpd.sjoin(uf, streets_diversity, how='inner', predicate='intersects')

  #3_2_richness index attribution
  richness_pb = locations_in_buffer.groupby('geometry_right').apply(richness)

  if functions_subgroup_col_name == None:
    pass
  else:
    richness_pb_si = locations_in_buffer[locations_in_buffer[functions_subgroup_col_name]==True].groupby('geometry_right').apply(richness)

  #3_3_shannon-wiener index attribution
  shannon_wiener_diversity_pb = locations_in_buffer.groupby('geometry_right').apply(shannon_wiener_diversity)

  if functions_subgroup_col_name == None:
    pass
  else:
    shannon_wiener_diversity_pb_si = locations_in_buffer[locations_in_buffer[functions_subgroup_col_name]==True].groupby('geometry_right').apply(shannon_wiener_diversity)

  #3_4_merging indexes and streets
  streets_diversity = streets_diversity.merge(richness_pb.rename('richness'),  left_on= "geometry", right_on= "geometry_right", how = "left")
  streets_diversity = streets_diversity.merge(shannon_wiener_diversity_pb.rename('sw'), left_on= "geometry", right_on= "geometry_right", how = "left")

  if functions_subgroup_col_alias==None:
    pass
  else:
    streets_diversity = streets_diversity.merge(richness_pb_si.rename(f'r_{functions_subgroup_col_alias}'), left_on= "geometry", right_on= "geometry_right", how = "left")
    streets_diversity = streets_diversity.merge(shannon_wiener_diversity_pb_si.rename(f'sw_{functions_subgroup_col_alias}'), left_on= "geometry", right_on= "geometry_right", how = "left")

  streets_diversity = streets_diversity.set_geometry("geometry")


  #4_normalising values of columns for a comparative analysis
  for i in streets_diversity.select_dtypes(include='number').columns: #streets_diversity["richness", "r_si","s_w","s_w_si"] + morpho_metrics_list_cols:
    normalize(streets_diversity, i)

  #5_filtering the needed columns
  if functions_subgroup_col_alias == None:
    Basic = ["street_name","richness","geometry"] + [f'norm_{i}'for i in morpho_metrics_list_cols]
    Basic_plus = ["street_name","norm_richness"] + Basic
    Advanced = ["street_name","sw", "geometry"] + [f'norm_{i}'for i in morpho_metrics_list_cols]
    Advanced_plus =  ["street_name","norm_sw"] + Advanced
    All = ["street_name","richness","norm_richness","sw","norm_sw","geometry"] + [f'norm_{i}'for i in morpho_metrics_list_cols]
  else:
    Basic = ["street_name","richness", f'r_{functions_subgroup_col_alias}',"geometry"] + [f'norm_{i}'for i in morpho_metrics_list_cols]
    Basic_plus =  ["street_name","norm_richness", f"norm_r_{functions_subgroup_col_alias}"] + Basic
    Advanced = ["street_name","sw",f"sw_{functions_subgroup_col_alias}", "geometry"] + [f'norm_{i}'for i in morpho_metrics_list_cols]
    Advanced_plus =   ["street_name","norm_sw",f"norm_sw_{functions_subgroup_col_alias}"] + Advanced
    All = ["street_name","richness", f'r_{functions_subgroup_col_alias}',"norm_richness", f"norm_r_{functions_subgroup_col_alias}","sw",f"sw_{functions_subgroup_col_alias}","norm_sw",f"norm_sw_{functions_subgroup_col_alias}","geometry"] + [f'norm_{i}'for i in morpho_metrics_list_cols]

  packages = {
        "Basic": Basic,
        "Basic_plus": Basic_plus,
        "Advanced": Advanced,
        "Advanced_plus": Advanced_plus,
        "All": All
    }

  streets_diversity1 = streets_diversity[packages[package]]


  #6_saving
  if save_file == "csv":
    streets_diversity1.to_csv("streets_morphology_functions.csv")
  if save_file == "geojson":
    streets_diversity1.to_file("streets_morphology_functions.geojson")
  if save_file == "none":
    pass


  print(f"The {package} bundle of street space functional diversity metrics is successfully calculated and integrated with street-network morphology." )
  return streets_diversity1


def visuals(data):
  for col in data.select_dtypes(include='number').columns:
      fig, ax = plt.subplots(1, 1, figsize=(15, 12))


      data.plot(
          column=col,
          cmap='magma',
          scheme='NaturalBreaks',
          ax=ax,
          legend=True,
          alpha=1,
          linewidth=1

      )


      cx.add_basemap(ax, crs=data.crs, source=cx.providers.CartoDB.DarkMatterNoLabels)


      ax.set_axis_off()
      ax.set_title(f'Natural Breaks of {col}', fontsize=16, pad=20)

      plt.tight_layout()
     # plt.savefig(f'{col}_Natural_Breaks_basemap.png', dpi=300, bbox_inches='tight',
                #  facecolor='white', edgecolor='none')
      plt.show()


      # for that, normalized metrics are needed
def streets_mismatched(data, functional_metric, int_g,int_l,ch_g,ch_l):

  data = data.reset_index(drop=True)

  #Average mismatch
  data["mismatch_avg"]= 0
  data["mismatch_avg"] = data["mismatch_avg"].astype("float")

  a = float(input("Insert the weight of Integration \n(significance of a to-movement of a street for your request): "))
  b = 1-a

  for row in range(len(data)):
    data.loc[row, "mismatch_avg"] = (a*(data.loc[row, int_g]+ data.loc[row, int_l])/2 + b*(data.loc[row, ch_g]+data.loc[row, ch_l])/2) - data.loc[row, functional_metric]
  next

  #Global mismatch
  data["mismatch_global"]= 0
  data["mismatch_global"] = data["mismatch_global"].astype("float")

  a_g = float(input("Insert the weight of Global Integration \n(significance of a global to-movement of a street for your request): "))
  b_g = 1-a_g

  for row in range(len(data)):
      data.loc[row, "mismatch_global"] = (a_g*(data.loc[row, int_g]) + b*(data.loc[row, ch_g])) - data.loc[row, functional_metric]
  next

  #Local mismatch
  data["mismatch_local"]= 0
  data["mismatch_local"] = data["mismatch_local"].astype("float")

  a_l = float(input("Insert the weight of Local Integration \n(significance of a global to-movement of a street for your request): "))
  b_l = 1-a_l

  for row in range(len(data)):
      data.loc[row, "mismatch_local"] = (a_l*(data.loc[row, int_g]) + b*(data.loc[row, ch_l])) - data.loc[row, functional_metric]
  next


  print(("under [a_avg, a_global, a_local] ="),[a, a_g, a_l]), print(("under [b_avg, b_global, b_local] ="),[b,b_g, b_l])
  print("Where a is the weight of Integration metric and b is the weight of Choice")
  return data

def split_mism(data, col, segment_street=None, save_n = None):
    sm1 = data[data[col]>0]
    sm2 = data[data[col]<0]

    fig, ax = plt.subplots(1, 2, figsize=(25, 25), constrained_layout=True)


    sm1.plot(
            column=col,
            cmap='magma',
            scheme='NaturalBreaks',
            ax=ax[0],
            legend=True,
            alpha=1,
            linewidth=1
        )

    sm2[col] = abs(sm2[col])
    sm2.plot(
            column=col,
            cmap='magma',
            scheme='NaturalBreaks',
            ax=ax[1],
            legend=True,
            alpha=1,
            linewidth=1
        )

    # Zoom to segment
    if segment_street is not None:
        minx, miny, maxx, maxy = segment_street.total_bounds
        ax[0].set_xlim(minx, maxx)
        ax[0].set_ylim(miny, maxy)
        ax[1].set_xlim(minx, maxx)
        ax[1].set_ylim(miny, maxy)

    cx.add_basemap(ax[0], crs=sm1.crs, source=cx.providers.CartoDB.DarkMatter)
    cx.add_basemap(ax[1], crs=sm2.crs, source=cx.providers.CartoDB.DarkMatter)

    # Styling


    if segment_street is not None:
      ax[0].set_axis_off()
      ax[0].set_title(f'Natural breaks of positive {col}', fontsize=20, pad=20)
      ax[1].set_axis_off()
      ax[1].set_title(f'Natural breaks of negative {col}', fontsize=20, pad=20)
    else:
      ax[0].set_axis_off()
      ax[0].set_title(f'Natural breaks of positive {col}', fontsize=30, pad=20)
      ax[1].set_axis_off()
      ax[1].set_title(f'Natural breaks of negative {col}', fontsize=30, pad=20)

    plt.tight_layout()
    if save_n == None:
      pass
    else:
      plt.savefig(f"{save_n}_mismathes_Natural_Breaks_basemap.png", dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    fig.set_tight_layout("tight")
    plt.show()