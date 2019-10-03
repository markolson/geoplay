# Helpers
import copy
# Shapely **HAS** to be imported before anything else.
from shapely.geometry import mapping, shape
from shapely.prepared import prep

# Project configuration code
from geoplay.project import Project
# Data sources
from geoplay.data.zcta import ZCTA
from geoplay.data.stl_parks import StlParks

project = Project(
  name="Nearby Parks",
  output_dir='stl-parks',
  projection='+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')

zcta = project.use(ZCTA)
parks = project.use(StlParks)

wanted_zips = zcta.filterTo(zipCodes=[63108, 63118, 63103, 63104, 63110])

for zip_area in wanted_zips:
  # puff the bounds of the zip codes out 0.001 arcradians
  loose_zip_bounds = shape(zip_area['geometry']).buffer(0.001)

  # Make a list of parks that touch our new expanded ZIP
  touching_parks = list(filter(
    lambda p: loose_zip_bounds.intersects(shape(p['geometry'])),
    parks.shapefile()))

  # Update the geometry in the shapefile
  zip_area['geometry'] = mapping(loose_zip_bounds)
  # Write our variables
  zip_area['properties']['PARKCOUNT'] = len(touching_parks)
  zip_area['properties']['PARKNAMES'] = ', '.join([p['properties']['TEXT_'] for p in touching_parks ])

# Write out our final file
project.save_layer(
  name='nearby-park-counts',
  using_data=wanted_zips,
  variables={
    'ZCTA5CE10': {'type': 'str', 'from_data': 'ZCTA5CE10'},
    'PARKCOUNT': {'type': 'int', 'from_data': 'PARKCOUNT'},
    'PARKNAMES': {'type': 'str', 'from_data': 'PARKNAMES'},
  })

project.save_csv(name='zip_parks', using_data=wanted_zips)
