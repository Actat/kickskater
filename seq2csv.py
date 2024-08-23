#!/usr/bin/python3

import sys
import yaml
import csv
import numpy as np
import quaternion

seq_file = 'AISTSimulator-KickSkater.seq'
csv_file = 'output.csv'
title_row = True

print('Load file: ' + seq_file)
try:
    with open(seq_file, 'r') as f:
        seq = yaml.safe_load(f)
except Exception as e:
    print(e)
    print('Failed to load file (' + seq_file + ').')
    print('Exit.')
    sys.exit()
print('The seq file is loaded.')

print('File format check')
try:
    file_type = seq['type']
    file_content = seq['content']
    file_version = seq['format_version']
    if (file_type != 'CompositeSeq'):
        raise ValueError('type is not CompositeSeq (' + file_type + ')')
    if (file_content != 'BodyMotion'):
        raise ValueError('content is not BodyMotion (' + file_content + ')')
    if (file_version != 4):
        raise ValueError('format_version is not 4 (' + str(file_version) + ')')
except Exception as e:
    print(e)
    print('Exit.')
    sys.exit()
print('Format OK.')

title = ['time', 'x', 'y', 'z', 'qw', 'qx', 'qy', 'qz', 'roll', 'pitch', 'yaw']
for i in range(seq['components'][1]['num_parts']):
    title.append(str(i))
print('csv column: ' + str(title))

result = []
if title_row:
    result.append(title)

frame_rate = seq['frame_rate']
num_frames = seq['num_frames']
for i in range(num_frames):
    time = 1. * i / frame_rate

    quat = np.quaternion(
        seq['components'][0]['frames'][i][0][3],
        seq['components'][0]['frames'][i][0][4],
        seq['components'][0]['frames'][i][0][5],
        seq['components'][0]['frames'][i][0][6])
    eul = quaternion.as_euler_angles(quat)

    row = [time, *seq['components'][0]['frames'][i][0], *eul, *seq['components'][1]['frames'][i]]

    result.append(row)

print('CSV file: ' + csv_file)
try:
    with open(csv_file, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(result)
except Exception as e:
    print(e)
    print('Failed to open file (' + csv_file + ').')
    print('Exit.')
    sys.exit()
print('The csv file is written.')
