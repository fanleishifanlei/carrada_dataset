"""Script to generate centroid for all sequences"""
import os
import json
from radar_utils import RADAR_HOME, download
from radar_utils.configurable import Configurable
from radar_domain.carrada.annotations.centroid_tracking import CentroidTracking

if __name__ == '__main__':
    config_path = os.path.join(RADAR_HOME, 'config.ini')
    config = Configurable(config_path).config
    warehouse = config['data']['warehouse']
    carrada = download('Carrada', os.path.join(warehouse, 'Carrada'))
    with open(os.path.join(carrada, 'data_seq_ref.json'), 'r') as fp:
        ref_data = json.load(fp)
    with open(os.path.join(carrada, 'validated_seqs.txt')) as fp:
        seq_names = fp.readlines()
    seq_names = [seq.replace('\n', '') for seq in seq_names]
    seq_names = ['2020-02-28-13-12-42']
    data_types = ['cluster']
    for seq_name in seq_names:
        print('***** Processing sequence {} *****'.format(seq_name))
        ref_ids = ref_data[seq_name]['ref_frame']
        instances = ref_data[seq_name]['instances']
        min_frame_boundaries = ref_data[seq_name]['min_frame_boundaries']
        max_frame_boundaries = ref_data[seq_name]['max_frame_boundaries']
        """
        ref_ids = [ref_ids[1]]
        instances = [instances[1]]
        min_frame_boundaries = [min_frame_boundaries[1]]
        max_frame_boundaries = [max_frame_boundaries[1]]
        """
        labels = ref_data[seq_name]['labels']
        for data_type in data_types:
            print('===> Generating {} annotations with Jensen-Shannon strategy'.format(data_type))
            CentroidTracking(seq_name, instances, ref_ids, labels, min_frame_boundaries,
                             max_frame_boundaries).create_annotations(save_annotations=True,
                                                                      save_vis_rd=True,
                                                                      save_vis_doa=False,
                                                                      data_type=data_type)
