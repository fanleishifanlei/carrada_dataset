"""Test RdPointsGenerator class"""
import os
import json
import pytest
from utils.configurable import Configurable
from annotation_generators.rd_points_generator import RDPointsGenerator

CONFIG_PATH = '../config.ini'
CONFIG = Configurable(CONFIG_PATH).config
# CARRADA = download('Carrada', os.path.join(CONFIG['data']['warehouse'], 'Carrada'))
CARRADA = os.path.join(CONFIG['data']['warehouse'], 'Carrada')

@pytest.fixture
def get_true_data():
    seq_name = '2020-02-28-13-14-35'
    with open(os.path.join(CARRADA, seq_name, 'rd_points.json'), 'r') as fp:
        rd_points = json.load(fp)
    with open(os.path.join(CARRADA, seq_name, 'rd_points_coordinates.json'), 'r') as fp:
        rd_points_coord = json.load(fp)
    return rd_points, rd_points_coord

def test_rd_points_generator(get_true_data):
    with open(os.path.join(CARRADA, 'data_seq_ref_all_instances.json'), 'r') as fp:
        ref_data = json.load(fp)
    seq_name = '2020-02-28-13-14-35'
    instances = ref_data[seq_name]['instances']
    n_points = 1
    time_window = 10
    generator = RDPointsGenerator(seq_name, n_points, instances, time_window)
    test_rd_points, test_rd_points_coord = generator.get_rd_points(save_rd_imgs=False,
                                                                   save_points=False,
                                                                   save_points_coordinates=False,
                                                                   save_world_points=False)
    assert test_rd_points == get_true_data[0]
    assert test_rd_points_coord == get_true_data[1]
