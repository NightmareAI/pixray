FROM r8.im/pixray/text2image@sha256:5c347a4bfa1d4523a58ae614c2194e15f2ae682b57e3797a5bb468920aa70ebf
RUN pip install basicsr
RUN apt-get update && apt-get install -yy ffmpeg && rm -rf /var/lib/apt/lists/*
COPY pixray-dreamer.py .
CMD ["python", "-m", "pixray-dreamer.py"]
