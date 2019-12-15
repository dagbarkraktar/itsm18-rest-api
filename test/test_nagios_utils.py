import unittest
from datetime import datetime

from app.resources import nagios_utils


class TestNagiosUtils(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parse_nagios_time(self):
        """ Testing Nagios timestamp parsing - must return GMT - 3 hours """
        res = nagios_utils.parse_nagios_time("1546289999000")
        test_time = datetime.utcfromtimestamp(1546300799)
        self.assertEqual(res, test_time)

    def test_parse_hdd_perf_data_wrong_input(self):
        """ Testing HDD wrong input - must return 0,0 """
        res1, res2 = nagios_utils.parse_hdd_perf_data("some=wrong;string")
        self.assertEqual((res1, res2), (0, 0))

    def test_parse_hdd_perf_data(self):
        """ Testing HDD regular input - must return two of float """
        res1, res2 = nagios_utils.parse_hdd_perf_data("'c:\\ Used Space'=32.52Gb;79.92;89.91;0.00;99.90")
        self.assertEqual((res1, res2), (99.9, 32.52))

    def test_parse_ping_perf_data(self):
        """ Testing PING regular input - must return two of float """
        res1, res2 = nagios_utils.parse_ping_perf_data("rta=0.528000ms;100.000000;500.000000;0.000000 pl=10%;20;60;0")
        self.assertEqual((res1, res2), (0.528, 10.0))

    def test_parse_ping_perf_data_wrong_input(self):
        """ Testing PING wrong input - must return 0,0 """
        res1, res2 = nagios_utils.parse_ping_perf_data("some=wrong;string")
        self.assertEqual((res1, res2), (0.0, 0.0))

    def test_parse_mem_use_perf_data(self):
        """ Testing Memory Usage regular input - must return two of float """
        res1, res2 = nagios_utils.parse_mem_use_perf_data("'Memory usage'=1178.88MB;2750.08;3093.84;0.00;3437.60")
        self.assertEqual((res1, res2), (3437.6, 1178.88))

    def test_parse_mem_use_perf_data_wrong_input(self):
        """ Testing Memory Usage wrong input - must return 0,0 """
        res1, res2 = nagios_utils.parse_mem_use_perf_data("some=wrong;string")
        self.assertEqual((res1, res2), (0.0, 0.0))

    def test_parse_cpu_load_perf_data(self):
        """ Testing CPU Load regular input - must return load in percent """
        res = nagios_utils.parse_cpu_load_perf_data("'5 min avg Load'=7%;80;90;0;100")
        self.assertEqual(res, 7)

    def test_parse_cpu_load_perf_data_wrong_input(self):
        """ Testing CPU Load wrong input - must return 0 """
        res = nagios_utils.parse_cpu_load_perf_data("some=wrong;string")
        self.assertEqual(res, 0)

    def test_parse_uptime_perf_data(self):
        """ Testing Uptime regular input - must return uptime in hours """
        res = nagios_utils.parse_uptime_perf_data("uptime=25052")
        self.assertEqual(res, 25052)

    def test_parse_uptime_perf_data_wrong_input(self):
        """ Testing Uptime wrong input - must return 0 """
        res = nagios_utils.parse_uptime_perf_data("")
        self.assertEqual(res, 0)
