import os
import json
import glob
import pytest
import torchvision

from utils import CARRADA_HOME
from utils.configurable import Configurable
from utils.sort import Sort
from annotation_generators.instance_generator import InstanceGenerator, ImageInstances

SEQ_NAME = '2020-02-28-13-09-58'
CONFIG_PATH = os.path.join(CARRADA_HOME, 'config.ini')
CONFIG = Configurable(CONFIG_PATH).config
CARRADA = os.path.join(CONFIG['data']['warehouse'], 'Carrada')

def get_img_points():
    real_data = dict()
    with open(os.path.join(CARRADA, SEQ_NAME, 'points.json'), 'r') as fp:
        real_points = json.load(fp)
    sequence_path = os.path.join(CARRADA, SEQ_NAME)
    img_paths = sorted(glob.glob(os.path.join(sequence_path, 'camera_images', '*.jpg')))
    img_paths = sorted(glob.glob(os.path.join(sequence_path, 'camera_images', '*.jpg')))
    for img_path in img_paths[72:80]:
        img_name = img_path.split('/')[-1].split('.')[0]
        real_data[img_name] = real_points[SEQ_NAME][img_name] # ['001114'][0]
    return real_data

def test_image_instances():
    true_data = get_img_points()
    instance_generator = InstanceGenerator()
    paths = instance_generator.get_paths()
    model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)
    model.eval()
    seq_mot_tracker = Sort()
    sequence_path = os.path.join(CARRADA, SEQ_NAME)
    img_paths = sorted(glob.glob(os.path.join(sequence_path, 'camera_images', '*.jpg')))
    # img_path = img_paths[100]
    n_random_points = 0
    save_instances_masks = False
    for img_path in img_paths[72:80]:
        img_name = img_path.split('/')[-1].split('.')[0]
        # real_img_points = real_points[seq_name][img_name] # ['001114'][0]
        image = ImageInstances(img_path, model, paths, seq_mot_tracker, n_random_points,
                               save_instances_masks)
        image.update_instances()
        predicted_points = image.get_points()[img_name]
        if predicted_points != {}:
            assert list(predicted_points['000001'][0]) == true_data[img_name]['001114'][0]

if __name__ == '__main__':
    test_image_instances()
