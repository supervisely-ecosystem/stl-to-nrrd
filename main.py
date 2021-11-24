import nrrd
import trimesh
from supervisely_lib.io.fs import file_exists, get_file_ext


stl_extention = '.stl'


def convert_stl_to_nrrd(stl_path: str, nrrd_path: str):

    if not file_exists(stl_path):
        raise ValueError('File at given path {} not exist'.format(stl_path))

    if get_file_ext(stl_path) != stl_extention:
        raise ValueError('File extention must be .stl, not {}'.format(get_file_ext(stl_path)))

    mesh = trimesh.load(stl_path)
    voxel = mesh.voxelized(pitch=1.0)
    voxel = voxel.fill()
    np_mask = voxel.matrix.astype(int)
    nrrd.write(nrrd_path, np_mask)
