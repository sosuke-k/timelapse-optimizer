# Timelapse Optimizer

## Dependencies

```
# I'm using pyenv, virtualenv
# anaconda2-4.1.0
conda create -n image matplotlib opencv scipy
pyenv global anaconda2-4.1.0/envs/image
pip install -r requirements.txt
```

## Usage

```
$ python optimize_timelapse.py --help
usage: optimize_timelapse.py [-h] --video-path VIDEO_PATH [--tmp-dir TMP_DIR]
                             --output-path OUTPUT_PATH

optional arguments:
  -h, --help                show this help message and exit
  --video-path VIDEO_PATH   Set path to video file (e.g. './video.mp4')
  --tmp-dir TMP_DIR         Set path to temporally directory for debug (e.g. './tmp')
  --output-path OUTPUT_PATH Set path to output video file (e.g. './optimized_video.mp4')
```

### Example

```
$ python optimize_timelapse.py --video-path ./sample.mp4 --output-path ./out.mp4 --tmp-dir ./tmp
asctime:2016-12-21 02:35:06,116	name:root	level:INFO	message:Video path : ./sample.mp4
asctime:2016-12-21 02:35:06,116	name:root	level:INFO	message:Output path : ./out.mp4
asctime:2016-12-21 02:35:06,352	name:optimizer	level:DEBUG	message:Initializing TimelapseOptimizer
asctime:2016-12-21 02:35:06,352	name:optimizer	level:INFO	message:Extracting clip from 0.0 to None
asctime:2016-12-21 02:35:06,353	name:optimizer	level:DEBUG	message:Clip duration : 100.000000
asctime:2016-12-21 02:35:06,353	name:optimizer	level:DEBUG	message:Clip fps : 30
asctime:2016-12-21 02:35:06,353	name:optimizer	level:DEBUG	message:Hashing 100.00 clip with imagehash.phash
100%|########################################################################################################################################################################################################################################|
asctime:2016-12-21 02:36:35,967	name:optimizer	level:DEBUG	message:Hashed 100.00 clip with imagehash.phash
asctime:2016-12-21 02:36:36,046	name:optimizer	level:DEBUG	message:msz : 0.782214
asctime:2016-12-21 02:36:36,046	name:optimizer	level:DEBUG	message:half window : 49
asctime:2016-12-21 02:36:37,304	name:optimizer	level:DEBUG	message:Minimun number of event frames : 3.000000
asctime:2016-12-21 02:36:37,446	name:optimizer	level:DEBUG	message:Play 0-1029 at 30.361884 speed
asctime:2016-12-21 02:36:37,447	name:optimizer	level:INFO	message:34.300000 - 35.066667
[MoviePy] >>>> Building video ./tmp/1029-1052.mp4
[MoviePy] Writing video ./tmp/1029-1052.mp4
100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 24/24 [00:00<00:00, 34.89it/s]
[MoviePy] Done.
[MoviePy] >>>> Video ready: ./tmp/1029-1052.mp4

asctime:2016-12-21 02:36:41,729	name:optimizer	level:DEBUG	message:Play 1052-2028 at 30.361884 speed
asctime:2016-12-21 02:36:41,730	name:optimizer	level:INFO	message:67.600000 - 69.633333
[MoviePy] >>>> Building video ./tmp/2028-2089.mp4
[MoviePy] Writing video ./tmp/2028-2089.mp4
100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 62/62 [00:02<00:00, 12.06it/s]
[MoviePy] Done.
[MoviePy] >>>> Video ready: ./tmp/2028-2089.mp4

asctime:2016-12-21 02:36:49,005	name:optimizer	level:DEBUG	message:Play 2089-2102 at 30.361884 speed
asctime:2016-12-21 02:36:49,006	name:optimizer	level:INFO	message:70.066667 - 72.233333
[MoviePy] >>>> Building video ./tmp/2102-2167.mp4
[MoviePy] Writing video ./tmp/2102-2167.mp4
100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 66/66 [00:03<00:00, 20.14it/s]
[MoviePy] Done.
[MoviePy] >>>> Video ready: ./tmp/2102-2167.mp4

[MoviePy] >>>> Building video ./tmp/optimized.mp4
[MoviePy] Writing video ./out.mp4
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 211/211 [00:51<00:00,  2.47it/s]
[MoviePy] Done.
[MoviePy] >>>> Video ready: ./out.mp4
```

### Image Sequence

If you have image sequence, you can use `ffmpeg`.

Example:

```
ffmpeg -framerate 30 -start_number 416 -i ./images/DSC%05d.JPG -vframes 3000 -vcodec libx264 -pix_fmt yuv420p -r 30 sample.mp4
```
