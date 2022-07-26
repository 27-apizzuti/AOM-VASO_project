import os

from psychopy import monitors, visual


def setup(background_color):
    save_path = os.path.dirname(os.path.abspath(__file__))
    save_path += os.path.sep + "monitors" + os.path.sep

    monitors.calibTools.monitorFolder = save_path
    os.makedirs(save_path, exist_ok=True)

    mon = monitors.Monitor(name="testMonitor",
                           width=30.0,
                           distance=99.0)

    mon.setCalibDate()
    mon.setSizePix([1920, 1200])
    mon.save()

    win = visual.Window(size=mon.getSizePix(),
                        color=background_color,
                        fullscr=True,
                        allowGUI=False,
                        monitor=mon,
                        winType="pyglet",
                        units="deg",
                        screen=0,
                        waitBlanking=True,
                        allowStencil=True,
                        multiSample=False,
                        numSamples=2)
    return win
