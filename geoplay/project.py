from shapely.geometry import mapping, shape
import datetime
import fiona
from pathlib import Path
import csv

class Project:
  def __init__(self, name, output_dir, projection):
    self.name = name
    self.projection = projection or '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs'
    self.output_dir = output_dir or datetime.datetime.now().strftime("%Y.%m.%d-%H%M")

    self.data = {}

  def use(self, dataType):
    key = dataType.__name__
    self.log("Loading " + key)
    self.data[key] = dataType().project_to(self.projection)
    return self.data[key]

  def new_shapefile_from(self, original, named, using_data):
    to = self.path_for(named)
    new_file = fiona.open(to, 'w',
      driver=original.driver,
      crs=original.crs,
      schema=original.schema)
    new_file.writerecords(using_data)
    return new_file

  def save_layer(self, name, using_data, variables=[], geotype='Polygon'):
    to = self.path_for(name)

    new_file = fiona.open(to, 'w',
      driver='ESRI Shapefile',
      crs=fiona.crs.from_string(self.projection),
      schema={
        'geometry': geotype,
        'properties': {k: v['type'] for k, v in variables.items()}
      })

    for record in using_data:
      new_props = {}
      for key, data in variables.items():
        val = data['default'] if ('default' in data) else record['properties'][data['from_data']]
        new_props[key] = val
      record['properties'] = new_props
      new_file.write(record)
    self.log("Writing " + new_file.name)
    return new_file

  def save_csv(self, name, using_data):
    to = self.path_for(name + '.csv')
    self.log("Writing %d records in %s" % (len(using_data), to.name))
    fieldnames = using_data[0]['properties'].keys()
    with open(to, 'w') as f:
      writer = csv.DictWriter(f, fieldnames=fieldnames)
      writer.writeheader()
      for row in using_data:
        writer.writerow(row['properties'])

  def limit(self, bounds, collection, buffer=0.0):
    bounds = shape(bounds['geometry']).buffer(buffer)

    return list(filter(
      lambda p: bounds.intersects(shape(p['geometry'])),
      collection.shapefile()))

  def _output_path(self):
    path = Path('output') / self.output_dir
    if not path.exists():
      self.log("Creating output folder " + path.as_posix())
      path.mkdir(parents=True, exist_ok=True)
    return path

  def path_for(self, name):
    return self._output_path() / name

  def log(self, msg):
    print("[" + self.name + "] " + msg)


