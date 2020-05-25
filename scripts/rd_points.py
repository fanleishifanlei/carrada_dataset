import os
import json
from radar_utils import RADAR_HOME, download
from radar_utils.configurable import Configurable
from radar_domain.carrada.annotations.rd_points_generator import RDPointsGenerator

if __name__ == '__main__':
    config_path = os.path.join(RADAR_HOME, 'config.ini')
    config = Configurable(config_path).config
    carrada = download('Canada', os.path.join(config['data']['warehouse'], 'Carrada'))
    with open(os.path.join(carrada, 'data_seq_ref_all_instances.json'), 'r') as fp:
        ref_data = json.load(fp)
    with open(os.path.join(carrada, 'validated_seqs.txt')) as fp:
        seq_names = fp.readlines()
    seq_names = [seq.replace('\n', '') for seq in seq_names]
    seq_names = ['2020-02-28-13-09-58']
    for seq_name in seq_names:
        print('***** Processing sequence {} *****'.format(seq_name))
        instances = ref_data[seq_name]['instances']
        n_points = 1
        time_window = 10
        generator = RDPointsGenerator(seq_name, n_points, instances, time_window)
        _, _ = generator.get_rd_points(save_rd_imgs=True,
                                       save_points=False,
                                       save_points_coordinates=False,
                                       save_world_points=False)
