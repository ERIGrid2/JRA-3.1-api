import logging
from processor.ConfigProcessor import ConfigProcessor

def parse_global_config(filename):
  #does nothing yet
  return 0

def serialize_local_configs(lconfs):
  # does nothing yet
  return

if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(levelname)s:%(name)s:%(message)s')
  config=parse_global_config('../config_mgmt/Global_Configuration_mvp.yaml')
  processor=ConfigProcessor(config)
  processor.process()
  local_configs=processor.get_local_configs()
  serialize_local_configs(local_configs)
