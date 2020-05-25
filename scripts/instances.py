import os
from radar_utils import RADAR_HOME, download
from radar_domain.canada.annotation_transfer.baseline.instance_generator import InstanceGenerator

if __name__ == '__main__':
    config_path = os.path.join(RADAR_HOME, 'config.ini')
    carrada_path = os.path.join(download('Carrada'), 'L5_Test_Track')
    baseline_path = os.path.join(canada_path, 'baseline_data')
    with open(os.path.join(baseline_path, 'validated_seqs.txt')) as fp:
        sequence_names = fp.readlines()
    sequence_names = [seq.replace('\n', '') for seq in sequence_names]
    for seq_name in sequence_names:
        InstanceGenerator(config_path).process_sequence(seq_name, 0, save_boxes=False,
                                                        save_masks=False, save_labels=True)
