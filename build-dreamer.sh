#!/bin/bash
cog build -t pixray
docker build . -t pixray-dreamer
docker tag pixray-dreamer:latest us-docker.pkg.dev/nightmarebot-ai/nightmarebot/pixray-dreamer:latest
docker tag pixray-dreamer:latest 438969101893.dkr.ecr.us-east-2.amazonaws.com/nightmarebot:latest
docker push us-docker.pkg.dev/nightmarebot-ai/nightmarebot/pixray-dreamer:latest
docker push 438969101893.dkr.ecr.us-east-2.amazonaws.com/nightmarebot:latest
