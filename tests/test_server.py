from backend import server
import unittest
import os


class TestServer(unittest.TestCase):
    test_tmp_file = "tmp.csv"
    
    def tearDown(self):
        if os.path.isfile(self.test_tmp_file):
            os.unlink(self.test_tmp_file)

    def test_decode(self):
        data = [b'/ISk5AM150-T000\r\n', b'\x020.0.0(73066029)\r\n', b'1.8.0(0008989.442*kWh)\r\n', b'0.2.0(1)\r\n', b'C.1.6(A8D9)\r\n', b'F.F.0(0000000)\r\n', b'!\r\n', b'\x034']
        value = server._parse_meter_reading(data)
        
        self.assertEqual(value, 8989.442)
    
    @unittest.skip
    def test_get_reading(self):
        total, current = server.get_reading()
        
        print("Total: {0}".format(total))
        print("Current: {0}".format(current))
        
    def test_write_csv(self):
        server.file_path = self.test_tmp_file
        server.write_csv(88881.2, 222.2)
        server.write_csv(88881.2, 222.2)
        server.write_csv(88881.2, 222.2)
        
        self.assertTrue(os.path.isfile(self.test_tmp_file))
        