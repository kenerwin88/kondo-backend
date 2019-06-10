from kondo.plugin import Plugin

class RoomClass(Plugin):
  def apply():
    print('hi')

  def should_apply(**kwargs):
    return True