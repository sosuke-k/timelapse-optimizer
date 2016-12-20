# coding=utf-8

import os
import logging
import math
import numpy as np
from scipy import stats
import cv2
from PIL import Image
import imagehash
import seaborn as sns
import moviepy.editor as mp
from progressbar import ProgressBar, Percentage, Bar


class TimelapseOptimizer(object):

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__module__)
        self.logger.debug("Initializing %s" % self.__class__.__name__)

    def optimize(self, clip, t_start=0.0, t_end=None, k1=0.3, k2=1.15, **kwargs):
        self.logger.info("Extracting clip from %s to %s" %
                         (str(t_start), str(t_end)))
        clip = clip.subclip(t_start=t_start, t_end=t_end)
        self.logger.debug("Clip duration : %f" % clip.duration)
        self.logger.debug("Clip fps : %d" % clip.fps)

        hashs = self.hashs(clip, **kwargs)
        values = self.distances(hashs)
        blured_scores, threshold = self.detect(values, fps=clip.fps, **kwargs)

        if kwargs["debug"] and kwargs["debugdir"]:
            self.savefig(kwargs["debugdir"], values, blured_scores, threshold)

        event_flags = (blured_scores < -threshold)
        event_at_start, event_boundaries = self.boundaries(event_flags, fps=clip.fps, **kwargs)

        n = len(event_boundaries)
        subclips = []
        for i in xrange(n - 1):
            start_frame = event_boundaries[i]
            end_frame = event_boundaries[i + 1]
            inside_event = (i % 2 == 0) == event_at_start
            start_frametime = float(start_frame) / clip.fps
            end_frametime = float(end_frame) / clip.fps
            if inside_event:
                self.logger.info("%f - %f" % (start_frametime, end_frametime))

            subclip = clip.subclip(start_frametime, end_frametime)
            if inside_event:

                if kwargs["debug"] and kwargs["debugdir"]:
                    filename = "%d-%d.mp4" % (start_frame, end_frame)
                    subclip.write_videofile(os.path.join(kwargs["debugdir"], filename))

                ratio = float(end_frame - start_frame) / (clip.fps * (1 + k1))
                newclip = subclip.fx(mp.vfx.speedx, ratio)
            else:
                ratio = 1 + (clip.fps) * math.exp(-(1.0 + k2) / clip.duration)
                self.logger.debug("Play %d-%d at %f speed" % (start_frame, end_frame, ratio))
                newclip = subclip.fx(mp.vfx.speedx, ratio)

            subclips.append(newclip)

        last_event_end_frametime = float(event_boundaries[-1]) / clip.fps
        subclip = clip.subclip(t_start=last_event_end_frametime, t_end=None)
        ratio = 1 + (clip.fps) * math.exp(-(1.0 + k2) / clip.duration)
        newclip = subclip.fx(mp.vfx.speedx, ratio)
        subclips.append(newclip)

        optimized_clip = mp.concatenate_videoclips(subclips)
        return optimized_clip

    def savefig(self, debugdir, distances, blured_scores, threshold):

        sns.plt.plot(distances, label="distances")
        sns.plt.legend(loc=2)
        sns.plt.savefig(os.path.join(debugdir, "distances.png"))
        sns.plt.clf()

        sns.plt.plot(distances / np.max(distances), label="normalized distances")
        sns.plt.plot(stats.zscore(distances), label="z scores")
        sns.plt.legend(loc=2)
        sns.plt.savefig(os.path.join(debugdir, "z_scores.png"))
        sns.plt.clf()

        sns.plt.plot(distances / np.max(distances), label="normalized distances")
        sns.plt.plot(blured_scores, label="blured z scores")
        sns.plt.plot([0, len(blured_scores)], [-threshold, -threshold], label="threshold")
        sns.plt.legend(loc=2)
        sns.plt.savefig(os.path.join(debugdir, "blured_z_scores.png"))
        sns.plt.clf()

    def boundaries(self, event_flags, fps=30.0, **kwargs):
        events = []
        inside_event = False
        start_event = 0
        for i, flag in enumerate(event_flags):
            if not inside_event:
                if flag:
                    start_event = i
                    inside_event = True
            else:
                if not flag:
                    events.append((start_event, i))
                    inside_event = False

        min_event_frame = fps / 10.0
        self.logger.debug("Minimun number of event frames : %f" % min_event_frame)
        filtered_events = [(start, end) for (start, end) in events if end - start > min_event_frame]

        event_boundaries = [idx for event in filtered_events for idx in event]

        event_at_start = True
        if event_boundaries[0] != 0:
            event_at_start = False
            event_boundaries = [0] + event_boundaries

        return event_at_start, event_boundaries

    def detect(self, values, fps=30, k=1.0, threshold_proportion=0.05, **kwargs):
        z_scores = stats.zscore(values)
        z2 = np.sqrt(np.power(z_scores, 2))
        msz = np.average(z2)
        self.logger.debug("msz : %f" % msz)

        hw = int(len(values) / (2 * fps))
        if hw % 2 == 0:
            hw = hw + 1
        self.logger.debug("half window : %d" % hw)

        blured = cv2.GaussianBlur(z_scores, (hw, hw), 0)
        blured = [v[0] for v in blured]
        return blured, msz

    def distances(self, hashs):
        n = len(hashs)
        distances = []
        for i in xrange(n - 1):
            distances.append(hashs[i + 1] - hashs[i])
        return np.array(distances, dtype=np.float64)

    def hashs(self, clip, hash_function=imagehash.phash, **kwargs):
        hashs = []

        self.logger.debug("Hashing %.2f clip with %s.%s" %
                          (clip.duration, hash_function.__module__, hash_function.__name__))

        p = ProgressBar(widgets=[Percentage(), Bar()],
                        maxval=int(clip.duration * clip.fps)).start()
        for i, frame in enumerate(clip.iter_frames()):
            p.update(i + 1)
            image = Image.fromarray(frame)
            hashs.append(hash_function(image))
            del image
        p.finish()

        self.logger.debug("Hashed %.2f clip with %s.%s" %
                          (clip.duration, hash_function.__module__, hash_function.__name__))
        return hashs
