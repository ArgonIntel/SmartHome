# FINALIZIRANO

from weather import Weather
from datetime import datetime, timedelta
from time import sleep
import threading


class Light:
    def __init__(self, light_id) -> None:
        self.on_off = False
        self.auto = False
        self.ovc = False
        self.position = light_id
        self.thread_auto = None
        self.thread_ovc = None
        self.weather = Weather()

    def turn_on_off(self) -> None:
        """manual control of lights
        """
        self.auto = False
        self.ovc = False
        if self.on_off:
            self.on_off = False
        else:
            self.on_off = True

    def auto_on_off(self) -> None:
        while self.auto:
            curr_time = datetime.now()
            now = curr_time.time()
            delta = timedelta(minutes=30)
            now = (datetime.combine(datetime.min, now) + delta).time()
            if self.weather.sunset_time < now or self.weather.sunrise_time > now:
                self.on_off = True
            else:
                self.on_off = False
            sleep(900)

    def light_on_off_overcast(self) -> None:
        """ control lights based on overcast data
        """
        while self.ovc:
            if self.weather.overcast:
                self.on_off = True
            else:
                self.on_off = False
            sleep(900)


    def set_auto(self) -> None:
        """enables automatic/manual light control based
        on day/night
        """
        if self.auto:
            self.auto = False
            if self.thread_auto is not None:
                self.thread_auto.join()
        else:
            self.auto = True
            self.thread_auto = threading.Thread(target=self.auto_on_off)
            self.thread_auto.start()

    
    def overcast_f_on_off(self) -> None:
        """Enables automatic/manual control based on
        overcast data
        """
        if self.ovc:
            self.ovc = False
            if self.thread_ovc is not None:
                self.thread_ovc.join()
        else: 
            self.ovc = True
            self.thread_ovc = threading.Thread(target=self.light_on_off_overcast)
            self.thread_ovc.start()
