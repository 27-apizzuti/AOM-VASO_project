import numpy as np
from psychopy import event, visual
from psychopy.tools.monitorunittools import pix2deg

from config import *
from utils import *


class PRF:
    def __init__(self, win, log, timer, fix_dot, task_dot):
        self.win = win
        self.log = log
        self.timer = timer
        self.fix_dot = fix_dot
        self.task_dot = task_dot

        self.tr = GENERAL_PARAMS["TR"]
        self.background = GENERAL_PARAMS["background"]
        self.initial_pause = GENERAL_PARAMS["initial_pause"]
        self.final_pause = GENERAL_PARAMS["final_pause"]

        self.flicker_hz = PRF_PARAMS["flicker_hz"]
        self.coloring = PRF_PARAMS["coloring"]

        self.orientations = [0, 90, 45, -45]
        self.n_positions = 12
        self.n_rm_positions = 2
        self.bar_width = 2
        self.iterations = 6

        self.setup()

    def get_checkerboards(self, win, checker_size, checkers_per_side):
        checkerboards = {}

        checkerboards[0] = checkerboards[90] = get_checkerboard(win, 0,
                                                                checker_size,
                                                                checkers_per_side,
                                                                checkers_per_side)

        checkerboards[45] = checkerboards[-45] = get_checkerboard(win, 45,
                                                                  checker_size,
                                                                  checkers_per_side,
                                                                  checkers_per_side)
        return checkerboards

    def get_bar_aperture(self, win, half_width, half_length):
        rectangle = ((-half_width, -half_length),
                     (-half_width, half_length),
                     (half_width, half_length),
                     (half_width, -half_length))

        bar_aperture = visual.Aperture(win=win,
                                       shape=rectangle,
                                       autoLog=False)
        bar_aperture.disable()

        return bar_aperture

    def get_bar_positions(self, half_bar_width, half_mask_length,
                          iterations, n_positions, n_rm_positions):

        interval = np.linspace(-half_mask_length + half_bar_width,
                               half_mask_length - half_bar_width,
                               n_positions)
        bar_positions = {}

        bar_positions[0] = [(val, 0) for val in interval]
        bar_positions[90] = [(0, val) for val in interval]

        bar_positions[45] = rotate_coordinates(bar_positions[0], -45)
        bar_positions[-45] = rotate_coordinates(bar_positions[0], 45)

        for orientation, candidate_positions in bar_positions.items():
            remove_positions = candidate_positions.copy()
            np.random.shuffle(remove_positions)
            remove_positions = iter(remove_positions)

            positions = []

            for _ in range(iterations):
                new_positions = candidate_positions.copy()

                for _ in range(n_rm_positions):
                    new_positions.remove(next(remove_positions))

                np.random.shuffle(new_positions)

                start_idx = 1 if not positions or positions[-1] is None else 0
                rand_idx = np.random.randint(start_idx, len(new_positions) + 1)

                for shift in range(n_rm_positions):
                    new_positions.insert(rand_idx + shift, None)

                positions += new_positions

            bar_positions[orientation] = iter(positions)

        return bar_positions

    def create_square_mask(self, win, background):
        max_win_size_pix = max(win.size)
        min_win_size_pix = min(win.size)

        max_win_size_deg = pix2deg(max_win_size_pix, win.monitor)

        center_coord = max_win_size_pix / 2
        start = int(center_coord - min_win_size_pix // 2)

        mask = np.ones((max_win_size_pix, max_win_size_pix))

        mask[start: start + min_win_size_pix,
             start: start + min_win_size_pix] = -1

        tex = np.full((16, 16), background)

        square_mask = visual.GratingStim(win=win,
                                         tex=tex,
                                         mask=mask,
                                         size=max_win_size_deg,
                                         autoLog=False)
        return square_mask

    def get_durations_sequence(self):
        initial_pause = self.tr * self.initial_pause
        final_pause = self.tr * self.final_pause

        target_iterations = self.n_positions * \
                            len(self.orientations) * \
                            self.iterations

        real_flicker_hz = self.n_inversions / self.tr

        flicker_durations = np.tile(1 / real_flicker_hz,
                                    self.n_inversions)

        repeated_flicker_durations = np.tile(flicker_durations,
                                             target_iterations)

        durations_seq = np.concatenate(([initial_pause],
                                        repeated_flicker_durations,
                                        [final_pause]))

        durations_seq = np.cumsum(durations_seq)

        return iter(durations_seq)

    def setup(self):
        half_min_win_length = pix2deg(min(self.win.size),
                                      self.win.monitor) / 2

        half_min_win_diag = np.sqrt(2 * half_min_win_length**2)

        n_checkers = self.n_positions * self.bar_width
        self.checker_size = half_min_win_length * 2 / n_checkers
        self.half_bar_width = self.checker_size * self.bar_width / 2

        self.checkers_per_side = int(np.ceil(half_min_win_diag /
                                             self.checker_size))

        self.n_inversions = int(round(self.tr * self.flicker_hz))

        self.orientations_seq = shuffle_sequence(self.orientations,
                                                 self.iterations)

        self.aperture = self.get_bar_aperture(self.win,
                                              self.half_bar_width,
                                              half_min_win_diag)

        self.mask = self.create_square_mask(self.win, self.background)

        self.bar_positions = self.get_bar_positions(self.half_bar_width,
                                                    half_min_win_length,
                                                    self.iterations,
                                                    self.n_positions,
                                                    self.n_rm_positions)

        self.checkerboards = self.get_checkerboards(self.win,
                                                    self.checker_size,
                                                    self.checkers_per_side)

        n_configs = len(self.orientations_seq)
        alternation = get_alternation(self.checkers_per_side,
                                      self.checkers_per_side)

        self.colors = get_colors(alternation, n_configs, self.coloring)

        self.durations_seq = self.get_durations_sequence()

        self.targets = get_target_events(self.durations_seq)

        log_vals(self.log, PRF_PARAMS, "task")
        log_vals(self.log, self.durations_seq, "durations")
        log_vals(self.log, self.targets, "targets")

    def draw(self):
        self.fix_dot.autoDraw = True
        self.task_dot.autoDraw = True
        self.mask.autoDraw = True

        flip(self, ["initial pause"])
        wait(self)

        for orientation in self.orientations_seq:
            self.aperture.ori = orientation

            checkerboard = self.checkerboards[orientation]
            positions = self.bar_positions[orientation]

            color = next(self.colors)

            for _ in range(self.n_positions):
                current_position = next(positions)

                if current_position is not None:
                    self.aperture.pos = current_position

                for _ in range(self.n_inversions):
                    if current_position is not None:
                        checkerboard.colors = next(color)
                    else:
                        checkerboard.colors = [self.background]

                    self.aperture.enable()
                    checkerboard.draw()
                    self.aperture.disable()

                    flip(self, ["color assigned",
                                orientation,
                                current_position])

                    wait(self, [checkerboard])

        flip(self, ["final pause"])
        wait(self)

        flip(self, ["end of experiment"])

        if self.coloring:
            check = termination([self.durations_seq,
                                 self.bar_positions,
                                 self.colors])
        else:
            check = termination([self.durations_seq,
                                 self.bar_positions])
        return check


class HRF:
    def __init__(self, win, log, timer, fix_dot, task_dot):
        self.win = win
        self.log = log
        self.timer = timer
        self.fix_dot = fix_dot
        self.task_dot = task_dot

        self.tr = GENERAL_PARAMS["TR"]
        self.background = GENERAL_PARAMS["background"]
        self.initial_pause = GENERAL_PARAMS["initial_pause"]
        self.final_pause = GENERAL_PARAMS["final_pause"]

        self.flicker_hz = HRF_PARAMS["flicker_hz"]
        self.coloring = HRF_PARAMS["coloring"]

        self.n_positions = 12
        self.bar_width = 2
        self.iterations = 12

        self.setup()

    def get_durations_sequence(self):
        initial_pause = self.tr * self.initial_pause
        final_pause = self.tr * self.final_pause

        real_flicker_hz = self.n_inversions / self.tr

        flicker_durations = np.tile(1 / real_flicker_hz,
                                    self.n_inversions)

        flicker_durations = np.tile(flicker_durations,
                                    (self.iterations, 1))

        multiplier = int(np.ceil(self.iterations / 3))
        pause_choice = [5 * self.tr, 6 * self.tr, 7 * self.tr]

        repeated_pauses = pause_choice * multiplier
        np.random.shuffle(repeated_pauses)

        repeated_pauses = np.reshape(repeated_pauses, (-1, 1))

        trial_duration = np.concatenate([flicker_durations,
                                         repeated_pauses], axis=1)

        trial_duration = trial_duration.flatten()

        durations_seq = np.concatenate(([initial_pause],
                                        trial_duration,
                                        [final_pause]))

        durations_seq = np.cumsum(durations_seq)

        return iter(durations_seq)

    def setup(self):
        half_min_win_length = pix2deg(min(self.win.size),
                                      self.win.monitor) / 2

        n_checkers = self.n_positions * self.bar_width
        self.checker_size = half_min_win_length * 2 / n_checkers

        win_lengths = pix2deg(self.win.size, self.win.monitor)

        n_checkers_x = win_lengths[0] / (self.checker_size * 2)
        n_checkers_x = int(np.ceil(n_checkers_x))

        n_checkers_y = win_lengths[1] / (self.checker_size * 2)
        n_checkers_y = int(np.ceil(n_checkers_y))

        self.n_inversions = int(round(self.tr * self.flicker_hz))

        self.checkerboard = get_checkerboard(self.win, 0, self.checker_size,
                                             n_checkers_x, n_checkers_y)

        alternation = get_alternation(n_checkers_x, n_checkers_y)
        self.colors = get_colors(alternation, self.iterations, self.coloring)

        self.durations_seq = self.get_durations_sequence()

        self.targets = get_target_events(self.durations_seq)

        log_vals(self.log, HRF_PARAMS, "task")
        log_vals(self.log, self.durations_seq, "durations")
        log_vals(self.log, self.targets, "targets")

    def draw(self):
        self.fix_dot.autoDraw = True
        self.task_dot.autoDraw = True

        flip(self, ["initial pause"])
        wait(self)

        checkerboard = self.checkerboard

        for _ in range(self.iterations):
            color = next(self.colors)

            for _ in range(self.n_inversions):
                checkerboard.colors = next(color)

                checkerboard.draw()

                flip(self, ["color assigned"])
                wait(self, [checkerboard])

            flip(self, ["intertrial pause"])
            wait(self)

        flip(self, ["final pause"])
        wait(self)

        flip(self, ["end of experiment"])

        if self.coloring:
            check = termination([self.durations_seq,
                                 self.colors])
        else:
            check = termination([self.durations_seq])

        return check


class TimeResolution:
    def __init__(self, win, log, timer, *_):
        self.win = win
        self.log = log
        self.timer = timer

        self.key = KEY_PARAMS["trigger"]

        self.n = TR_PARAMS["n"]

        self.setup()

    def setup(self):
        log_vals(self.log, TR_PARAMS, "task")

    def draw(self):
        self.win.flip()

        key_presses = []

        while True:
            press = event.waitKeys(keyList=[self.key],
                                   timeStamped=self.timer)

            key_presses.append(press[0][1])

            if len(key_presses) == self.n:
                break

        key_presses = np.array(key_presses)
        trs = key_presses[1:] - key_presses[:-1]

        tr_info = (np.mean(trs), np.std(trs))
        message = "TR: %f (avg), %f (std)" % tr_info

        flip(self, [message])

        return True
