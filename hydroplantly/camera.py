import os
import glob
import re
import logging
from datetime import datetime, timedelta
from picamera import PiCamera
import boto3
from botocore.exceptions import ClientError
from model import CameraSettings
from time_interval import TimeInterval

class Camera:

    def __init__(self, settings: CameraSettings, active_time: TimeInterval) -> None:
        self.__enabled = settings.enabled
        self.__local_path = settings.local_path
        self.__s3_path = settings.s3_path
        self.__s3 = boto3.client('s3')
        self.__cleanup_interval = settings.cleanup_interval
        self.__interval = settings.interval

        self.__last_photo = datetime(1990, 1, 1)
        self.__active_time = active_time

        if self.__enabled:
            self.enable()

    def enable(self):
        self.__camera = PiCamera()
        self.__enabled = True
        

    def photo(self, ts = datetime.now()):
        try: 
            epoch = ts.strftime('%s')
            file_name = f'shot_{epoch}.jpg'
            local_file = os.path.join(self.__local_path, file_name)
            s3_file = os.path.join(self.__s3_path, file_name)

            logging.info("Capturing image.")
            self.__camera.capture(local_file, resize=(1920, 1080))
            logging.info("Uploading image.")
            self.__s3.upload_file(local_file, 'hydroplantly', s3_file)
        except ClientError as e:
            logging.warning(f"Couldn't upload image due to {e.response}.")

    def cleanup(self):
        """
        Cleanup every day images that are older then 3 days
        """
        past = datetime.now() - self.__cleanup_interval
        past_ts = past.strftime("%s")

        files = glob.glob('images/*.jpg')
        filtered = filter(lambda f: int(re.search(r'shot_(\d+).jpg', f).group(1)) < 1649780865, files)

        for file in filtered:
            os.remove(file)
            

    def update(self):
        now = datetime.now()
        if  now - self.__last_photo > self.__interval \
            and self.__active_time.isInDatetime(now) \
            and self.__enabled:
            self.photo(now)
            self.__last_photo = now

        # do the clean up during the sleep time.
        if not self.__active_time.isInDatetime(now):
            self.cleanup()