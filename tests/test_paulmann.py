import unittest
from unittest.mock import patch
import pygatt
from paulmann.paulmann import Paulmann
from paulmann.models import State, Info
from .mocks import MockAdapter, MockDevice

MAC = "AA:AA:AA:AA:AA:AA"
PWD = "1234"

class PaulmannTestCase(unittest.TestCase):
    _light: Paulmann = None

    def setUpReal(self):
        self._light = Paulmann(MAC, PWD, pygatt.backends.GATTToolBackend())

    @patch('pygatt.backends.GATTToolBackend')
    def setUpMock(self, adapter):
        self._light = Paulmann(MAC, PWD, adapter=adapter)

        def new_connect(mac:str):
            return MockDevice(adapter)
        adapter.connect = new_connect


    def setUp(self):
        self.setUpReal()
        #self.setUpMock()

    def tearDown(self):
        self._light.disconnect()

    @patch('pygatt.backends.GATTToolBackend')
    def test_connect_and_authenticate(self, adapter):
        p:Paulmann = Paulmann(MAC, PWD, adapter=adapter)
        
        d = p.get_device()
        
        adapter.start.assert_called()
        adapter.connect.assert_called_with(MAC)
        self.assertIsNot(d, None)

    def test_set_and_get_state(self):
        self._light.set_state(on=True, brightness=70, color=200)
        s:State = self._light.get_state()

        self.assertEqual(s.on, True)
        self.assertEqual(s.brightness, 70)
        self.assertEqual(s.color, 200)

    def test_switch(self):
        self._light.switch(False)
        self.assertFalse(self._light.is_on())
        self._light.switch(True)
        self.assertTrue(self._light.is_on())

    def test_toggle(self):        
        self._light.switch(False)
        self._light.toggle()
        self.assertTrue(self._light.is_on())
        self._light.toggle()
        self.assertFalse(self._light.is_on())

    def test_brightness(self):        
        self._light.brightness(40)
        self.assertEqual(self._light.get_brightness(), 40)
        self._light.brightness(-5)
        self.assertEqual(self._light.get_brightness(), 0)
        self._light.brightness(150)
        self.assertEqual(self._light.get_brightness(), 100)

    def test_color(self):        
        self._light.color(250)
        self.assertEqual(self._light.get_color(), 250)
        self._light.color(100)
        self.assertEqual(self._light.get_color(), 153)
        self._light.color(400)
        self.assertEqual(self._light.get_color(), 370)

    def test_all(self):
        #p = Paulmann(MAC, PWD)
        #info = p.get_info()
        #print(info)

        """state = p.get_state()
        print(state)

        p.switch(True)
        print("Light is " + str(p.is_on()))
        sleep(1)
        p.switch(False)
        print("Light is " + str(p.is_on()))
        sleep(1)

        p.toggle()
        print("Light is " + str(p.is_on()))
        sleep(1)

        p.switch(False)
        sleep(1)
        p.brightness(10)
        print("Dimm is " + str(p.get_brightness()))
        p.switch(True)
        sleep(1)
        p.brightness(30)
        print("Dimm is " + str(p.get_brightness()))
        sleep(1)
        p.brightness(50)
        print("Dimm is " + str(p.get_brightness()))
        sleep(1)
        p.brightness(70)
        print("Dimm is " + str(p.get_brightness()))
        sleep(1)
        p.brightness(100)
        print("Dimm is " + str(p.get_brightness()))
        sleep(1)
        print("Dimm is " + str(p.get_brightness()))
        sleep(1)
        p.color(2700)
        print("Color is " + str(p.get_color()))
        sleep(1)
        p.color(3500)
        print("Color is " + str(p.get_color()))
        sleep(1)
        p.color(5000)
        print("Color is " + str(p.get_color()))
        sleep(1)
        p.color(6500)
        print("Color is " + str(p.get_color()))
        sleep(1)
"""