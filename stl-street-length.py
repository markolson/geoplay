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
from geoplay.data.precise_zcta import PreciseZCTA
from geoplay.data.stl_streets import StlStreets

degrees_to_meter = partial(pyproj.transform,
    pyproj.Proj(init='EPSG:4326'), # degrees
    # pyproj.Proj(init='EPSG:6360')) # feet
    pyproj.Proj(init='EPSG:32633')) # meter

project = Project(
  name="Street Length",
  output_dir='stl-streets',
  projection='+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')

zcta = project.use(PreciseZCTA)
streets = project.use(StlStreets)

wanted_zips = zcta.filterTo(zipCodes=[63108, 63118])

for zip_area in wanted_zips:
  bounds = prep(shape(zip_area['geometry']).buffer(0.0001))

  streets_2 = list(filter(
    lambda p: bounds.intersects(shape(p['geometry'])),
    streets.shapefile()))

  project.save_layer(
    name=('streets-in-' + zip_area['properties']['ZCTA5CE10']),
    using_data=streets_2,
    variables={},
    geotype='LineString')

  project.log("Tabulating Road Length")
  total = 0
  for line in streets_2:
    ls = LineString(line['geometry']['coordinates'])
    total += transform(degrees_to_meter, ls).length
  zip_area['properties']['ROADLENGTH'] = total

project.save_layer(
  name=('road-length'),
  using_data=wanted_zips,
  variables={
    'ZCTA5CE10': {'type': 'str', 'from_data': 'ZCTA5CE10'},
    'ROADLENGTH': {'type': 'float', 'from_data': 'ROADLENGTH'},
    'ALAND10': {'type': 'int', 'from_data': 'ALAND10'},
    'AWATER10': {'type': 'int', 'from_data': 'AWATER10'},
  })