import pytest

from dialogue import Dialogue
from hospital import Hospital
from commands import Commands


def test_user_input_patient_id(monkeypatch):
    hospital = Hospital()
    dialogue = Dialogue(hospital)
    monkeypatch.setattr('builtins.input', lambda _: "3")
    patient_id = dialogue.user_input_patient_id()
    assert isinstance(patient_id, int)
    assert patient_id == 3


def test_negative_user_input_patient_id(monkeypatch):
    hospital = Hospital()
    dialogue = Dialogue(hospital)
    monkeypatch.setattr('builtins.input', lambda _: "abc")
    patient_id = dialogue.user_input_patient_id()
    assert patient_id == None


@pytest.mark.parametrize("input_command, expected_command", [
    ('get status', Commands.GET_STATUS),
    ('status up', Commands.STATUS_UP),
    ('status down', Commands.STATUS_DOWN),
    ('discharge', Commands.DISCHARGE),
    ('calculate statistic', Commands.CALCULATE_STATISTICS),
    ('stop', Commands.STOP),
])
def test_user_input_main_command(monkeypatch, input_command, expected_command):
    hospital = Hospital()
    dialogue = Dialogue(hospital)
    monkeypatch.setattr('builtins.input', lambda _: input_command)
    command = dialogue.user_input_main_command()
    assert isinstance(command, Commands)
    assert input_command in expected_command


def test_user_input_need_discharge_patient(monkeypatch):
    hospital = Hospital()
    dialogue = Dialogue(hospital)
    monkeypatch.setattr('builtins.input', lambda _: "да")
    need_discharge = dialogue.user_input_need_discharge_patient()
    assert isinstance(need_discharge, bool)
    assert need_discharge
