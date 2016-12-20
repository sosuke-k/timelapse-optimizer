# coding=utf-8

import sys
import os
import logging
import argparse
import moviepy.editor as mp

from optimizer import TimelapseOptimizer


def main(**kwargs):
    logging.info("Video path : %s" % kwargs["video_path"])
    logging.info("Output path : %s" % kwargs["output_path"])
    clip = mp.VideoFileClip(kwargs["video_path"])
    optimized_clip = TimelapseOptimizer().optimize(clip, **kwargs)
    optimized_clip.write_videofile(kwargs["output_path"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video-path",
                        type=str,
                        required=True,
                        help="Set path to video file (e.g. './video.mp4')")
    parser.add_argument("--tmp-dir",
                        type=str,
                        default=None,
                        help="Set path to temporally directory for debug (e.g. './tmp')")
    parser.add_argument("--output-path",
                        type=str,
                        required=True,
                        help="Set path to output video file (e.g. './optimized_video.mp4')")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG,
                        format="asctime:%(asctime)s\tname:%(name)s\tlevel:%(levelname)s\tmessage:%(message)s")

    if not os.path.isfile(args.video_path):
        sys.exit("No such a file as %s" % args.video_path)

    debug = False
    debugdir = ""
    if args.tmp_dir:
        if not os.path.isdir(args.tmp_dir):
            sys.exit("No such a directory as %s" % args.tmp_dir)
        debug = True
        debugdir = args.tmp_dir

    main(video_path=args.video_path, output_path=args.output_path, debug=debug, debugdir=debugdir)
