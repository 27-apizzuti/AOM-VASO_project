from colorsys import hls_to_rgb
from copy import deepcopy
from itertools import cycle

import numpy as np
from psychopy import core, event, logging, visual
from scipy.stats import truncnorm

from config import GENERAL_PARAMS, KEY_PARAMS


def shuffle_sequence(sequence, iterations):
    shuffled_sequence = sequence.copy()
    np.random.shuffle(shuffled_sequence)

    for _ in range(iterations - 1):
        candidate_sequence = sequence.copy()
        np.random.shuffle(candidate_sequence)

        # this makes sure that neighbors have different values
        while shuffled_sequence[-1] == candidate_sequence[0]:
            np.random.shuffle(candidate_sequence)

        shuffled_sequence += candidate_sequence

    return shuffled_sequence


def get_target_events(durations_seq):
    durations = list(deepcopy(durations_seq))

    exp_start = durations[0]
    exp_end = durations[-2]

    exp_duration = exp_end - exp_start

    target_duration = GENERAL_PARAMS["target_duration"]
    last_timepoint = exp_duration - target_duration

    min_target_dist = GENERAL_PARAMS["target_range"][0]
    max_target_dist = GENERAL_PARAMS["target_range"][1]

    target_times = []

    while np.sum(target_times) <= last_timepoint:
        rand_time = np.random.uniform(min_target_dist,
                                      max_target_dist)

        rand_time = np.round(rand_time, 2)
        target_times.append(rand_time)

    target_times.pop()

    target_times_start = np.cumsum(target_times) + exp_start
    target_times_end = target_times_start + target_duration

    target_intervals = list(zip(target_times_start,
                                target_times_end))
    return target_intervals


def rotate_coordinates(coordinates, angle):
    angle = np.radians(angle)

    rotated_coordinates = []

    for pos in coordinates:
        new_pos_x = np.cos(angle) * pos[0] - np.sin(angle) * pos[1]
        new_pos_y = np.sin(angle) * pos[0] + np.cos(angle) * pos[1]

        rotated_coordinates.append((new_pos_x, new_pos_y))

    return rotated_coordinates


def get_checkerboard(win, angle, checker_size,
                     n_checkers_x, n_checkers_y):
    xys = []

    for x in range(-n_checkers_x, n_checkers_x):
        for y in range(-n_checkers_y, n_checkers_y):
            xys.append([(x + 0.5) * checker_size,
                        (y + 0.5) * checker_size])

    xys = sorted(xys)

    xys = rotate_coordinates(xys, angle)

    checkerboard = visual.ElementArrayStim(win=win,
                                           nElements=len(xys),
                                           sizes=checker_size,
                                           elementTex=None,
                                           elementMask=None,
                                           xys=xys,
                                           oris=angle,
                                           autoLog=False)
    return checkerboard


def get_alternation(n_checkers_x, n_checkers_y):
    alternation = np.ones((n_checkers_x * 2,
                           n_checkers_y * 2))

    alternation[::2, ::2] = -1
    alternation[1::2, 1::2] = -1

    alternation = alternation.flatten()

    return alternation


def get_colors(alternation, n_configs, coloring):
    colors = []

    l_mean = 0.8
    l_std = 0.1
    d_mean = 0.2
    d_std = 0.1

    if coloring:
        for _ in range(n_configs):
            lightness_v1 = np.empty((alternation.shape))
            lightness_v2 = np.empty((alternation.shape))

            pos_entries = np.argwhere(alternation == 1).squeeze()
            neg_entries = np.argwhere(alternation == -1).squeeze()

            size = (2, len(pos_entries))

            light_cols = get_truncated_normal(l_mean, l_std, 0.5, 1.0, size)
            dark_cols = get_truncated_normal(d_mean, d_std, 0.0, 0.5, size)

            lightness_v1[pos_entries] = light_cols[0]
            lightness_v1[neg_entries] = dark_cols[0]
            lightness_v2[pos_entries] = dark_cols[1]
            lightness_v2[neg_entries] = light_cols[1]

            hue_v1 = np.linspace(0, 1, len(alternation), endpoint=False)

            np.random.shuffle(hue_v1)
            hue_v2 = (hue_v1 + 0.5) % 1.0

            saturation = np.ones(len(alternation))

            hls_v1 = list(zip(hue_v1, lightness_v1, saturation))
            hls_v2 = list(zip(hue_v2, lightness_v2, saturation))

            rgb_v1 = [list(hls_to_rgb(*vals)) for vals in hls_v1]
            rgb_v1 = [[(val * 2) - 1 for val in triple] for triple in rgb_v1]

            rgb_v2 = [list(hls_to_rgb(*vals)) for vals in hls_v2]
            rgb_v2 = [[(val * 2) - 1 for val in triple] for triple in rgb_v2]

            colors.append(cycle([rgb_v1, rgb_v2]))

        return iter(colors)

    else:
        original = [[val] * 3 for val in alternation]
        inversion = [[-val] * 3 for val in alternation]
        colors.append(cycle([original, inversion]))

        return cycle(colors)


def get_truncated_normal(mean, std, low, high, size):
    eps = np.finfo(np.float32).eps

    a = (low - mean) / (std + eps)
    b = (high - mean) / (std + eps)

    rand_val = truncnorm.rvs(a, b,
                             loc=mean,
                             scale=std,
                             size=size)
    return rand_val


def log_vals(log, vals, name):
    if isinstance(vals, (dict, list)):
        log.write(name + ": " + str(vals) + "\n")
    else:
        vals = list(deepcopy(vals))
        log.write(name + ": " + str(vals) + "\n")


def flip(task, msgs, executed=[]):
    msg = " ".join(str(i) for i in msgs)
    task.win.logOnFlip(level=logging.EXP, msg=msg)

    flip_time = task.win.flip()
    executed.append(flip_time)


def wait(task, stims=[], desired=[]):
    timeout = next(task.durations_seq)

    while task.timer.getTime() < timeout:
        detect_interruption(task)
        show_target(task, stims)

    desired.append(timeout)


def detect_interruption(task):
    key = KEY_PARAMS["interrupt"]
    key_presses = event.getKeys([key])

    if key_presses:
        task.win.close()
        core.quit()


def show_target(task, stims):
    if hasattr(task, "targets"):
        time = task.timer.getTime()

        if task.targets:
            start, end = task.targets[0]
            in_interval = start <= time <= end
            beyond_interval = end < time
        else:
            in_interval = False
            beyond_interval = False

        if in_interval:
            task.task_dot.color = "red"
        else:
            task.task_dot.color = "black"

            if beyond_interval:
                del task.targets[0]

    if hasattr(task, "aperture"):
        task.aperture.enable()

    for stim in stims:
        stim.draw()

    if hasattr(task, "aperture"):
        task.aperture.disable()

    task.win.flip()


def termination(elements):
    end_reached = []

    for element in elements:
        if isinstance(element, dict):
            keys = element.keys()
            for key in keys:
                try:
                    next(element[key])
                except StopIteration:
                    end_reached.append(True)
                else:
                    end_reached.append(False)
        else:
            try:
                next(element)
            except StopIteration:
                end_reached.append(True)
            else:
                end_reached.append(False)

    check = str(all(end_reached))

    return check
