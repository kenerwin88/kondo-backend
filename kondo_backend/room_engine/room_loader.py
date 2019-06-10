import yaml
import os
import logging
from .required_file import RequiredFile
from .condition import Condition
from .room import Room


def room_loader(path):
    """Parses data and returns a Room object"""
    log = logging.getLogger(__name__)

    # Import kondo.yaml
    with open(path + '/kondo.yml', 'r') as f:
        data = yaml.safe_load(f)
    log.info(data)
    required_files = []
    for req_file in data['required_files']:
        if 'condition_type' in req_file['file'].keys():
            condition = Condition(condition_type=req_file['file']['condition_type'],
                                  condition_value=req_file['file']['condition_value'])
        else:
            condition = False
        required_files.append(RequiredFile(name=req_file['file']['name'],
                                           condition=condition))
    return Room(title=data['title'],
                required_files=required_files,
                rules=False)
