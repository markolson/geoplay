# Shapely **HAS** to be imported before anything else.
from shapely.geometry import mapping, shape, LineString
from shapely.ops import transform
from shapely.prepared import prep

import geopandas
import pyproj
from functools import partial

# Project configuration code
from geoplay.project import Project
# Data sources
from geoplay.data.ny_zips import NyZips
from geoplay.data.ny_bikes import NyBikes

degrees_to_meter = partial(pyproj.transform,
    pyproj.Proj(init='EPSG:4326'), # degrees
    # pyproj.Proj(init='EPSG:6360')) # feet
    pyproj.Proj(init='EPSG:32633')) # meter

project = Project(
  name="NY Bike Length",
  output_dir='ny-bikes',
  projection='+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')

zcta = project.use(NyZips)
streets = project.use(NyBikes)

wanted_zips = zcta.filterTo(zipCodes=[
  #63108, 63118])
  # 10035])
  10055,10453,10457,10460,10458,10467,10468,10451,10452,10456,10454,10455,10459,10474,10463,10471,10466,10469,10470,10475,10461,10462,10464,10465,10472,10473,11212,11213,11216,11233,11238,11209,11214,11228,11204,11218,11219,11230,11234,11236,11239,11223,11224,11229,11235,11201,11205,11215,11217,11231,11203,11210,11225,11226,11207,11208,11211,11222,11220,11232,11206,11221,11237,10026,10027,10030,10037,10039,10001,10011,10018,10019,10020,10036,10029,10035,10010,10016,10017,10022,10012,10013,10014,10004,10005,10006,10007,10038,10280,10002,10003,10009,10021,10028,10044,10065,10075,10128,10023,10024,10025,10031,10032,10033,10034,10040,11361,11362,11363,11364,11354,11355,11356,11357,11358,11359,11360,11365,11366,11367,11412,11423,11432,11433,11434,11435,11436,11101,11102,11103,11104,11105,11106,11374,11375,11379,11385,11691,11692,11693,11694,11695,11697,11004,11005,11411,11413,11422,11426,11427,11428,11429,11414,11415,11416,11417,11418,11419,11420,11421,11368,11369,11370,11372,11373,11377,11378,10302,10303,10310,10306,10307,10308,10309,10312,.10301,10304,10305,10314])


for zip_area in wanted_zips:
  bounds = prep(shape(zip_area['geometry']).buffer(0.0001))

  streets_2 = list(filter(
    lambda p: bounds.intersects(shape(p['geometry'])),
    streets.shapefile()))

  project.save_layer(
    name=('streets-in-' + zip_area['properties']['ZIPCODE']),
    using_data=streets_2,
    variables={},
    geotype='LineString')

  project.log("Tabulating Lane Length")
  total = 0
  for line in streets_2:
    ls = LineString(line['geometry']['coordinates'])
    total += transform(degrees_to_meter, ls).length
  zip_area['properties']['LENGTH'] = total
  project.log(str(total))

project.save_layer(
  name=('bike-length'),
  using_data=wanted_zips,
  variables={
    'ZIPCODE': {'type': 'str', 'from_data': 'ZIPCODE'},
    'LENGTH': {'type': 'float', 'from_data': 'LENGTH'},
  })