# Helpers
import pprint
import random
import copy
# Shapely **HAS** to be imported before anything else.
from shapely.geometry import mapping, shape
from shapely.prepared import prep

# Project configuration code
from kbrgeo.project import Project
# Data sources
from kbrgeo.data.zcta import ZCTA
from kbrgeo.data.stl_parks import StlParks

project = Project(
  name="St. Louis Parks",
  output_dir='stl-parks',
  projection='+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')

zcta = project.use(ZCTA)
parks = project.use(StlParks)

wanted_zips = zcta.filterTo(zipCodes=[63108, 63118, 63103, 63104, 63110])

stl_shp = project.new_shapefile(
  name='just-stl',
  using_data=wanted_zips,
  variables={
    'ZCTA5CE10': {'type': 'str', 'from_data': 'ZCTA5CE10'},
    'PARKCOUNT': {'type': 'int', 'default': 0},
    'PARKNAMES': {'type': 'str', 'default': ''},
  })

# now expand the bounds of the zip code a tiny bit to account for
# adjacent parks that might just be across the streets.
# shape() converts the polygon into a datatype `Shapely` can use, then we tell
# Shapely to add a buffer, and then use `mapping` to convert it back to a series
# of points
buffered_zips = copy.deepcopy(wanted_zips)
[bounds.update({'geometry': mapping(shape(bounds['geometry']).buffer(0.001))}) for bounds in buffered_zips]

for zip_area in buffered_zips:
  zip_bounds = shape(zip_area['geometry'])

  touching_parks = list(filter(
    lambda p: zip_bounds.intersects(shape(p['geometry'])),
    parks.shapefile()))

  zip_area['properties']['PARKCOUNT'] = len(touching_parks)
  zip_area['properties']['PARKNAMES'] = ', '.join([p['properties']['TEXT_'] for p in touching_parks ])

  project.new_shapefile(
    name=('parks-only-in-' + zip_area['properties']['ZCTA5CE10']),
    using_data=touching_parks,
    variables={
      'NAME': {'type': 'str', 'from_data': 'TEXT_'}
    })

buffered_zip = project.new_shapefile(
  name='buffered-stl',
  using_data=buffered_zips,
  variables={
    'ZCTA5CE10': {'type': 'str', 'from_data': 'ZCTA5CE10'},
    'PARKCOUNT': {'type': 'int', 'from_data': 'PARKCOUNT'},
    'PARKNAMES': {'type': 'str', 'from_data': 'PARKNAMES'},
  })

