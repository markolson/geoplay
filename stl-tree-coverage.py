from kbrgeo.zcta import ZCTA
from kbrgeo.workflow import Workflow
import pprint

project = Workflow("St. Louis Tree Coverage")
project.output_dir = 'stl-tree'

zcta = project.load(ZCTA)
just_cwe = zcta.filterTo(zipCodes=['63108', 63118])
cwe_file = project.path_for('just-cwe')
cwe_shp = project.clone_shapefile(original=zcta.shp(), to=cwe_file, new_data=just_cwe)

# new_trees = project.clone_shapefile(original=stltree.shp(), to='stl-trees', new_data=[])

pprint.pprint(just_cwe)