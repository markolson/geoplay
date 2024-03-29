# Shapely **HAS** to be imported before anything else.
from shapely.geometry import mapping, shape
# Project configuration code
from geoplay.project import Project
# Data sources
from geoplay.data.precise_zcta import PreciseZCTA
from geoplay.data.stl_parks import StlParks

project = Project(
  name="Nearby Parks",
  output_dir='stl-parks',
  projection='+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')

zcta = project.use(PreciseZCTA)
parks = project.use(StlParks)

wanted_zips = zcta.filterTo(zipCodes=[63108, 63118, 63103, 63104, 63110])

# Write out an intermediate file so that we can quickly validate it visually
project.save_layer(
  name='just-stl',
  using_data=wanted_zips,
  variables={
    'ZCTA5CE10': {'type': 'str', 'from_data': 'ZCTA5CE10'},
  })

for zip_area in wanted_zips:
  loose_zip_bounds = shape(zip_area['geometry']).buffer(0.001)

  # Make a list of parks that touch our bulked out ZIP Code
  touching_parks = list(filter(
    lambda p: loose_zip_bounds.intersects(shape(p['geometry'])),
    parks.shapefile()))

  # Update the geometry in the shapefile
  zip_area['geometry'] = mapping(loose_zip_bounds)
  # Write our variables
  zip_area['properties']['PARKCOUNT'] = len(touching_parks)
  zip_area['properties']['PARKNAMES'] = ', '.join([p['properties']['TEXT_'] for p in touching_parks ])

  # Write out intermediate layers for us to validate data with again
  project.save_layer(
    name=('parks-only-in-' + zip_area['properties']['ZCTA5CE10']),
    using_data=touching_parks,
    variables={
      'NAME': {'type': 'str', 'from_data': 'TEXT_'}
    })

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
