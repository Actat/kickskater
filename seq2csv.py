#!/usr/bin/python3

import sys
import yaml
import csv
import numpy as np
import quaternion

seq_file = 'AISTSimulator-KickSkater.seq'
csv_basename = 'output'
title_row = True

csv_pos = csv_basename + '_pos.csv'
csv_vel = csv_basename + '_vel.csv'

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

title_pos = ['time', 'x', 'y', 'z', 'qw', 'qx', 'qy', 'qz', 'roll', 'pitch', 'yaw']
title_vel = ['time', 'dx', 'dy', 'dz', 'droll', 'dpitch', 'dyaw']
for i in range(seq['components'][1]['num_parts']):
    title_pos.append(str(i))
    title_vel.append('d' + str(i))
print('csv_pos column: ' + str(title_pos))
print('csv_vel column: ' + str(title_vel))

result_pos = []
result_vel = []
if title_row:
    result_pos.append(title_pos)
    result_vel.append(title_vel)

frame_rate = seq['frame_rate']
num_frames = seq['num_frames']
pre = []
for i in range(num_frames):
    # pos
    time = 1. * i / frame_rate

    quat = np.quaternion(
        seq['components'][0]['frames'][i][0][3],
        seq['components'][0]['frames'][i][0][4],
        seq['components'][0]['frames'][i][0][5],
        seq['components'][0]['frames'][i][0][6])
    sy = 2 * quat.w * quat.y - 2 * quat.x * quat.z
    unlocked = sy < 0.999999
    eul = [
        np.arctan2(2 * quat.y * quat.z + 2 * quat.w * quat.x, 2 * quat.w * quat.w + 2 * quat.z * quat.z - 1.) if unlocked else 0,
        np.arcsin(2 * quat.w * quat.y - 2 * quat.x * quat.z),
        np.arctan2(2 * quat.x * quat.y + 2 * quat.w * quat.z, 2 * quat.w * quat.w + 2 *  quat.x * quat.x - 1.) if unlocked else np.arctan2(-2 * quat.x * quat.y + 2 * quat.z * quat.w, 2 * quat.w * quat.w + 2 * quat.y * quat.y - 1.)]

    row = [time, *seq['components'][0]['frames'][i][0], *eul, *seq['components'][1]['frames'][i]]

    result_pos.append(row)

    # vel
    dt = 1. / frame_rate
    now = [seq['components'][0]['frames'][i][0][0],
           seq['components'][0]['frames'][i][0][1],
           seq['components'][0]['frames'][i][0][2],
           *eul,
           *seq['components'][1]['frames'][i]]
    if(i >= 1):
        time = (i - 0.5) / frame_rate
        vel = [((n - p) / dt) for n, p in zip(now, pre)]
        result_vel.append([time, *vel])
    pre = now

print('csv_pos file: ' + csv_pos)
try:
    with open(csv_pos, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(result_pos)
except Exception as e:
    print(e)
    print('Failed to open file (' + csv_pos + ').')
    print('Exit.')
    sys.exit()
print('The csv file is written.')

print('csv_vel file: ' + csv_vel)
try:
    with open(csv_vel, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(result_vel)
except Exception as e:
    print(e)
    print('Failed to open file (' + csv_pos + ').')
    print('Exit.')
    sys.exit()
print('The csv file is written.')
