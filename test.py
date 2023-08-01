from  unittest.mock import patch
import unittest.mock

from hospital import Hospital
from commands import Commands
from patient import Patient
from dialogue import Dialogue


class TestHospital(unittest.TestCase):

    def setUp(self):
        self.hospital = Hospital()

    def test_discharge(self):
        patient_id = 1
        self.hospital.discharge(patient_id)
        self.assertNotIn(patient_id, self.hospital.PATIENTS)

    def test_calculate_statistics(self):
        self.assertIsInstance(self.hospital.calculate_statistics(), str)


class TestPatient(unittest.TestCase):

    def setUp(self):
        self.patient = Patient(patient_id= 1)

    def test_init(self):
        self.assertEqual(self.patient.id, 1)
        self.assertEqual(self.patient.status_id, 1)

    def test_status_name(self):
        self.patient.status_id = 0
        self.assertEqual(self.patient.status_name, 'Тяжело болен')

        self.patient.status_id = 1
        self.assertEqual(self.patient.status_name, 'Болен')

        self.patient.status_id = 2
        self.assertEqual(self.patient.status_name, 'Слегка болен')

        self.patient.status_id = 3
        self.assertEqual(self.patient.status_name, 'Готов к выписке')

    def test_status_up(self):
        self.patient.status_id = 0
        for i in range(1, 4):
            self.assertTrue(self.patient.status_up())
            self.assertEqual(self.patient.status_id, i)

        self.patient.status_id = 3
        self.assertFalse(self.patient.status_up())
        self.assertEqual(self.patient.status_id, 3)

    def test_status_down(self):
        self.patient.status_id = 3
        for i in range(4, 1):
            self.assertTrue(self.patient.status_down())
            self.assertEqual(self.patient.status_id, i)

        self.patient.status_id = 0
        self.assertFalse(self.patient.status_down())
        self.assertEqual(self.patient.status_id, 0)


class TestDialogue(unittest.TestCase):

    def setUp(self):
        self.hospital = Hospital()
        self.dialogue = Dialogue(self.hospital)

    @patch('builtins.input', return_value='3')
    def test_user_input_patient_id(self, mock_input):
        patient_id = self.dialogue.user_input_patient_id()
        self.assertIsInstance(patient_id, int)
        self.assertEqual(patient_id, 3)

    @patch('builtins.input', return_value ='status up')
    def test_user_input_main_command(self, mock_input):
        command = self.dialogue.user_input_main_command()
        self.assertIsInstance(command, Commands)
        self.assertTrue(command.is_up_status())

    @patch('builtins.input', return_values='да')
    def test_user_input_need_discharge_patient(self, mock_input):
        need_discharge = self.dialogue.user_input_need_discharge_patient()
        self.assertIsInstance(need_discharge, bool)
        self.assertFalse(need_discharge)
