import nrrd
import trimesh
from supervisely_lib.io.fs import file_exists, get_file_ext, get_file_name
import supervisely_lib as sly
import numpy as np


stl_extention = '.stl'
logger = sly.logger


def convert_stl_to_nrrd(stl_path: str, nrrd_path: str):

    if not file_exists(stl_path):
        raise ValueError('File at given path {} not exist'.format(stl_path))

    if get_file_ext(stl_path) != stl_extention:
        raise ValueError('File extention must be .stl, not {}'.format(get_file_ext(stl_path)))

    mesh = trimesh.load(stl_path)
    try:
        voxel = mesh.voxelized(pitch=1.0)
        voxel = voxel.fill()
        np_mask = voxel.matrix.astype(int)
        nrrd.write(nrrd_path, np_mask)
    except IndexError:
        logger.warn('Input stl file {} is empty, check your input data'.format(get_file_name(stl_path)))
        np_mask = np.zeros((1, 1, 1))
        nrrd.write(nrrd_path, np_mask)
