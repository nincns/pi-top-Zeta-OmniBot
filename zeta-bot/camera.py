import cv2
import threading
import time
import logging

logger = logging.getLogger(__name__)

class MultiCamera:
    def __init__(self, fps=20, video_sources=[0]):
        logger.info(f"Initializing camera class with {fps} fps and video_sources={video_sources}")
        self.fps = fps
        self.video_sources = video_sources
        self.cameras = {}
        for src in self.video_sources:
            camera = cv2.VideoCapture(src)
            if camera.isOpened():
                self.cameras[src] = camera
                logger.debug(f"Camera {src} successfully opened.")
            else:
                logger.warning(f"Camera {src} failed to open.")
        self.max_frames = 5 * self.fps
        self.frames = {src: [] for src in self.video_sources}
        self.isrunning = False

    def start(self):
        if not self.isrunning:
            self.isrunning = True
            self.thread = threading.Thread(target=self._capture_loop, daemon=True)
            self.thread.start()
            logger.info("Thread started")

    def _capture_loop(self):
        dt = 1 / self.fps
        logger.debug("Observation started")
        while self.isrunning:
            for src, camera in self.cameras.items():
                ret, frame = camera.read()
                if ret:
                    if len(self.frames[src]) == self.max_frames:
                        self.frames[src] = self.frames[src][1:]
                    self.frames[src].append(frame)
            time.sleep(dt)
        logger.info("Thread stopped successfully")

    def stop(self):
        self.isrunning = False

    def get_frame(self, src):
        if src in self.frames and len(self.frames[src]) > 0:
            img = cv2.imencode('.jpg', self.frames[src][-1])[1].tobytes()
        else:
            with open("images/not_found.jpeg", "rb") as f:
                img = f.read()
        return img

    def __exit__(self, exc_type, exc_value, traceback):
        for camera in self.cameras.values():
            camera.release()
        logger.info("Camera released.")
