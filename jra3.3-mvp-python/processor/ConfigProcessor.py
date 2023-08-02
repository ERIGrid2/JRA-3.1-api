import logging

class ConfigProcessor:
  def __init__(self, config_obj):
    logging.info('instantiated ConfigProcessor')
    self.config_obj=config_obj

  def process(self):
    logging.info('called ConfigProcessor.process')

  def get_local_configs(self):
    logging.info('called ConfigProcessor.get_local_configs')
    return None
