import glob
import os
import requests
import subprocess
import pixray
from urllib.parse import urlparse

from cloudevents.sdk.event import v1
from dapr.clients import DaprClient
from dapr.ext.grpc import App
import json
import yaml
from types import SimpleNamespace
from minio import Minio

app = App()

client = Minio("dumb.dev", access_key=os.getenv('NIGHTMAREBOT_MINIO_KEY'), secret_key=os.getenv('NIGHTMAREBOT_MINIO_SECRET'))

def upload_local_directory_to_minio(local_path, bucket_name, minio_path):
    assert os.path.isdir(local_path)

    for local_file in glob.glob(local_path + '/**'):
        local_file = local_file.replace(os.sep, "/") # Replace \ with / on Windows
        if not os.path.isfile(local_file):
            upload_local_directory_to_minio(
                local_file, bucket_name, minio_path + "/" + os.path.basename(local_file))
        else:
            content_type = "application/octet-stream"
            if local_file.endswith("png"):
              content_type = "image/png"
            if local_file.endswith("mp4"):
              content_type = "video/mp4"
            if local_file.endswith("jpg"):
              content_type = "image/jpg"
            remote_path = os.path.join(
                minio_path, local_file[1 + len(local_path):])
            remote_path = remote_path.replace(
                os.sep, "/")  # Replace \ with / on Windows
            client.fput_object(bucket_name, remote_path, local_file, content_type=content_type)



@app.subscribe(pubsub_name="jetstream-pubsub", topic='request.pixray')
def dream(event: v1.Event) -> None:
  try:
    data = json.loads(event.Data())
    with DaprClient() as d:
      id = data["id"]
      workdir = os.path.join("/tmp/pixray/", id)
      indir = os.path.join(workdir, "in")
      if os.path.isdir(workdir):
        return
      os.makedirs(indir)

      try:
        request_settings = yaml.safe_load(data["input"]["settings"])
      except yaml.YAMLError as exc:
        print("Problem with settings", exc)
        sys.exit(1)
      
      try:
        if request_settings["init_image"] and not request_settings["init_image"].isspace():
          outfile = os.path.join(workdir, 'init_image.png')
          with requests.get(request_settings["init_image"], stream = True) as r:
            with open(outfile, 'wb') as f:
              for chunk in r.iter_content(chunk_size = 16*1024):
                f.write(chunk)
          request_settings["init_image"] = outfile
      except Exception as e: print(e, flush=True)


#      ix = 0
#      for img in data["input"]["images"]:
#        with requests.get(img, stream = True) as r:
#          u = urlparse(img)
#          fn = f'{ix}_{os.path.basename(u.path)}'
#          with open(os.path.join(indir, fn), 'wb') as f:
#            for chunk in r.iter_content(chunk_size = 16*1024):
#              f.write(chunk)
#        ix = ix+1

      pixray.reset_settings()
      pixray.add_settings(**request_settings)
      pixray.add_settings(outdir=f"{workdir}")
      settings = pixray.apply_settings()
      run_complete = False
      pixray.do_init(settings)
      while run_complete == False:
        run_complete = pixray.do_run(settings, return_display=True)

#      client = Minio("dumb.dev", access_key=os.getenv('NIGHTMAREBOT_MINIO_KEY'), secret_key=os.getenv('NIGHTMAREBOT_MINIO_SECRET'))

      upload_local_directory_to_minio(workdir, "nightmarebot-output", id)

#      for root, dirs, files in os.walk(workdir, topdown=False):
#        for name in files:
#          outfile = os.path.join(root, name)
#          client.fput_object("nightmarebot-output", f"{id}/{name}", outfile)
      d.publish_event(
        pubsub_name="jetstream-pubsub",
        topic_name="response.pixray",
        data=json.dumps({
            "id": data["id"],
            "context": data["context"]}),
        data_content_type="application/json")
  except Exception as e: print(e, flush=True)

app.run(50055)
