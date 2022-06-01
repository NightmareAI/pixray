import pixray
import yaml
import os
import sys

def main(argv):
  with open('/tmp/pixray/input.yaml', 'r') as config:
    request_settings = yaml.safe_load(config)

  pixray.reset_settings()
  pixray.add_settings(**request_settings)
  pixray.add_settings(outdir='/tmp/pixray')
  settings = pixray.apply_settings()
  run_complete = False
  while run_complete == False:
    run_complete = pixray.do_run(settings, return_display=True)

if __name__ == "__main__":
  main(sys.argv[1:])
