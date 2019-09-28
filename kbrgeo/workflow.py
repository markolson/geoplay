import datetime
import fiona
from pathlib import Path

class Workflow:
  def __init__(self, name):
    self.name = name

    self.output_dir = datetime.datetime.now().strftime("%Y.%m.%d-%H%M")
    self._current_step = 0

    self.data = {}

  def load(self, dataType):
    key = dataType.__name__
    self.log("Loading " + key)
    self.data[key] = dataType()
    return self.data[key]

  def clone_shapefile(self, original, to, new_data):
    new_file = fiona.open(to, 'w', driver=original.driver, crs=original.crs, schema=original.schema)
    new_file.writerecords(new_data)
    return new_file

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


