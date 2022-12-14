# import metabots

# tk = metabots.timekeeper()

from metabots.timekeeper import Timekeeper
from metabots.metabolism import Metabolism, Android, Potato
import metabots.logger as Logger

tk = Timekeeper()
m = Metabolism()
a = Android()
p = Potato()

tk.track_metabolism(m)
tk.track_metabolism(a)
tk.track_metabolism(p)

tk.tick()

Logger.info(tk.time)

Logger.show()