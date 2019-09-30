# Shapely **HAS** to be imported before anything else.
from shapely.geometry import mapping, shape
from shapely.prepared import prep
# Project configuration code
from kbrgeo.project import Project
# Data sources
from kbrgeo.data.zcta import ZCTA
from kbrgeo.data.stl_parks import StlParks

project = Project(
  name="Nearby Parks",
  output_dir='stl-parks',
  projection='+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')

zcta = project.use(ZCTA)
parks = project.use(StlParks)

wanted_zips = zcta.filterTo(zipCodes=[63108, 63118, 63103, 63104, 63110])
wanted_zips = helpers.addBufferArea(wanted_zips, buffer=0.001)

for zip_area in wanted_zips:
  touching_parks = helper.nearbyEnoughTo(zip_area, others=parks)
  # Write our variables
  zip_area['properties']['PARKCOUNT'] = len(touching_parks)

# Write out our final file
buffered_zip = project.save_layer(
  name='nearby-park-counts',
  using_data=buffered_zips,
  variables=['ZCTA5CE10','PARKCOUNT'])

