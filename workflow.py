import pixray
import yaml
import os

def main(argv):
  os.makedirs('/tmp/pixray')
  request_settings = yaml.safe_loaf(sys.argv[0])
  pixray.reset_settings()
  pixray.add_settings(**request_settings)
  pixray.add_settings(outdir='/tmp/pixray')
  settings = pixray.apply_settings()
  run_complete = False
  while run_complete == False
    run_complete = pixray.do_run(settings, return_display=True)

if __name__ == "__main__":
  main(sys.argv[1:])