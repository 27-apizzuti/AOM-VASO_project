#
import os
from datetime import datetime

import numpy as np
from psychopy import core, event, gui, logging, visual

import monitor
import tasks
from config import GENERAL_PARAMS, KEY_PARAMS
from stim import CustomDotStim
from utils import flip, log_vals, wait


def open_gui():
    run_choices = ["PRF (309 volumes)",
                   "HRF (105 volumes)"]

    dlg = gui.Dlg(title="PRF experiment")
    dlg.addField("Run", choices=run_choices)
    dlg.addField("TR")
    dlg.addField("Seed")
    dlg.show()

    if not dlg.OK:
        core.quit()

    assert dlg.data[2], "Define seed value!"

    if dlg.data[0] == run_choices[0]:
        GENERAL_PARAMS["task"] = "PRF"
    elif dlg.data[0] == run_choices[1]:
        GENERAL_PARAMS["task"] = "HRF"

    GENERAL_PARAMS["TR"] = float(dlg.data[1])

    GENERAL_PARAMS["random_seed"] = int(dlg.data[2])
    np.random.seed(GENERAL_PARAMS["random_seed"])


def get_fixation_dot(win):
    size = GENERAL_PARAMS["fixation_dot_radius"] * 2

    fixation_dot = CustomDotStim(win=win,
                                 nDots=1,
                                 dotSize=size,
                                 dotLife=-1,
                                 speed=0,
                                 color="black",
                                 autoLog=False)
    return fixation_dot


def get_task_dot(win):
    size = GENERAL_PARAMS["fixation_dot_radius"] * 1.3

    task_dot = CustomDotStim(win=win,
                             nDots=1,
                             dotSize=size,
                             dotLife=-1,
                             speed=0,
                             color="black",
                             autoLog=False)
    return task_dot


def show_loaded_screen(win):
    loaded_screen = visual.TextStim(win=win,
                                    text="Experiment loaded...",
                                    pos=(0.0, 0.0),
                                    height=1.0,
                                    autoLog=False)
    loaded_screen.draw()
    win.flip()


def show_waiting_screen(win):
    waiting_screen = visual.TextStim(win=win,
                                     text="Waiting for trigger...",
                                     pos=(0.0, 0.0),
                                     height=1.0,
                                     autoLog=False)
    waiting_screen.draw()
    win.flip()


def get_log(timer):
    logging.setDefaultClock(timer)
    logging.console.setLevel(logging.WARNING)

    identifier = datetime.now().strftime("%Y%m%d%H%M%S")

    save_path = os.path.dirname(os.path.abspath(__file__))
    save_path += os.path.sep + "logging" + os.path.sep
    save_path += identifier + os.path.sep

    os.makedirs(save_path)

    log = logging.LogFile(save_path + "log.txt",
                          level=logging.INFO)
    return log


def get_drift(log):
    executed = flip.__defaults__[-1]
    desired = wait.__defaults__[-1]

    if len(executed) != 0 and len(desired) != 0:
        desired.insert(0, 0.0)

        drift = np.array(executed) - np.array(desired)

        max_drift = np.around(np.max(drift), 4)
        mean_drift = np.around(np.mean(drift), 4)
        std_drift = np.around(np.std(drift), 4)

        vals = str(max_drift) + "s (max), " + \
               str(mean_drift) + "s (mean), " + \
               str(std_drift) + "s (std)" + "\n"

        log.write("drift: " + vals)


def main():
    open_gui()

    win = monitor.setup(GENERAL_PARAMS["background"])

    fixation_dot = get_fixation_dot(win)
    task_dot = get_task_dot(win)

    timer = core.Clock()
    log = get_log(timer)

    log_vals(log, GENERAL_PARAMS, "general")

    task = getattr(tasks, GENERAL_PARAMS["task"])(win, log, timer,
                                                  fixation_dot, task_dot)
    show_loaded_screen(win)

    event.waitKeys(keyList=[KEY_PARAMS["start"]])

    show_waiting_screen(win)

    event.waitKeys(keyList=[KEY_PARAMS["trigger"]])

    timer.reset()

    logging.exp("start experiment")

    check = task.draw()

    logging.exp("terminated correctly: " + str(check))

    get_drift(log)

    win.close()
    core.quit()


if __name__ == "__main__":
    main()
