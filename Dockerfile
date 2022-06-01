FROM pixray
RUN pip install basicsr
RUN apt-get update && apt-get install -yy ffmpeg && rm -rf /var/lib/apt/lists/*
CMD ["python", "-m", "pixray-dreamer.py"]
