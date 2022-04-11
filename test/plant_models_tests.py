from unittest import TestCase
from hydroplantly.plant import MoistureSettings, PumpSettings, WateringSettings


class TestMoistureSettings(TestCase):

    def test_channel_validation(self):
        with self.assertRaises(ValueError):
            MoistureSettings(channel=0)

        with self.assertRaises(ValueError):
            MoistureSettings(channel=4)

        try:
            MoistureSettings(channel=1)
            MoistureSettings(channel=2)
            MoistureSettings(channel=3)
        except ValueError:
            self.fail("False positive on channel validation.")


class TestWateringSettings(TestCase):

    def test_channel_validation(self):
        p = PumpSettings()
        m = MoistureSettings(channel=1)

        with self.assertRaises(ValueError):
            WateringSettings(
                pump_channel=0, moisture_setting=m, pump_settings=p)

        with self.assertRaises(ValueError):
            WateringSettings(
                pump_channel=4, moisture_setting=m, pump_settings=p)

        try:
            WateringSettings(
                pump_channel=1, moisture_setting=m, pump_settings=p)
            WateringSettings(
                pump_channel=2, moisture_setting=m, pump_settings=p)
            WateringSettings(
                pump_channel=3, moisture_setting=m, pump_settings=p)
        except ValueError:
            self.fail("False positive on channel validation.")
