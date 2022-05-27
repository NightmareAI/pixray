#!/bin/bash
cog build -t pixray-dreamer
docker build . -t us-west1-docker.pkg.dev/nightmarebot-ai/nightmarebot/pixray-dreamer
docker push us-west1-docker.pkg.dev/nightmarebot-ai/nightmarebot/pixray-dreamer
