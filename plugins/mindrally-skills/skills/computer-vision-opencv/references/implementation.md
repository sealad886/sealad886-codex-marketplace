# Computer Vision and OpenCV Development: implementation guidance

## Image and model contracts

Check imread/VideoCapture success explicitly. OpenCV commonly uses BGR and uint8,
while model inputs may require RGB, float ranges, channel-first tensors, or specific
normalization. Record every conversion. Choose interpolation by scale/content and
validate warp/homography coordinate systems. Match descriptor type to distance
metric (e.g. binary ORB versus float descriptors) and use robust fitting with
sufficient matches/inliers. Confirm detector bounding-box formats and NMS semantics.

## Build and device limits

Feature/tracker APIs may require opencv-contrib; SURF availability/build licensing
must be checked rather than assumed. Standard opencv-python wheels are CPU builds
and do not automatically supply CUDA. PyTorch CUDA/MPS/CPU support is a separate
capability; select and benchmark an actually available backend. Match torchvision
preprocessing to model weights. Video codecs depend on backend/build and deployment,
so verify writer opens and output decodes, handle missing/truncated frames, and
release captures/writers. Keep frame ordering and queue memory bounded when adding
parallel preprocessing. A successful pipeline is not evidence of model accuracy.

## Primary documentation

- [CPU wheel and contrib packaging capabilities](https://github.com/opencv/opencv-python).
- [Image, feature and video API contracts](https://docs.opencv.org/4.x/).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
