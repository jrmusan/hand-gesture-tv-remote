# Hand gesture based TV remote
This repo pulls together other folks incredable work to control my Samsung TV using hand gestures! Currently a WIP with a basic working demo of opening the TV menu and scrolling around. I've got an end goal of making some app or deployable image to run of Raspberry pi's.

## Gesture mappings

The table below shows the gestures currently mapped to TV shortcut methods (these live in `app.py` as `command_map`).

| Gesture | Mapped TV action | tv.shortcuts() method | Notes |
|---:|:---|:---|:---|
| Close | home | `tv.shortcuts().home()` | Return to Home/Menu |
| Open | enter | `tv.shortcuts().enter()` | Select / Enter |
| PointRight | right | `tv.shortcuts().right()` | Navigate right |
| PointDown | down | `tv.shortcuts().down()` | Navigate down |
| PointCenter | power | `tv.shortcuts().power()` | Toggle power |

Notes:
- The app only sends a command when the gesture is stable for a couple consecutive frames (debounce). See `_tv_command_state` in `app.py` to tune sensitivity.
- To change a mapping, edit the `command_map` dictionary in `app.py` — the value must be a method name present on the object returned by `tv.shortcuts()`.

# Reference
* [marysieek/samsung-tv-api](https://github.com/marysieek/samsung-tv-api/tree/master)
* [Kazuhito00/mediapipe-python-sample](https://github.com/Kazuhito00/mediapipe-python-sample)
* [MediaPipe](https://mediapipe.dev/)

# License
hand-gesture-recognition-using-mediapipe is under [Apache v2 license](LICENSE).
