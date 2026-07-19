import unittest

from skills import DisparoDeBalin


class DummyCharacter:
    def __init__(self, level=1, sp=100):
        self.level = level
        self.sp = sp
        self.sp_max = 100


class SkillStatusTests(unittest.TestCase):
    def test_reports_available_when_skill_is_ready(self):
        skill = DisparoDeBalin()
        skill.last_used = -skill.cooldown
        self.assertEqual(skill.get_status_label(1, DummyCharacter()), "Disponible")

    def test_reports_turns_remaining_when_skill_is_on_cooldown(self):
        skill = DisparoDeBalin()
        skill.last_used = 1
        self.assertEqual(skill.get_status_label(3, DummyCharacter()), "1 turno restante")


if __name__ == "__main__":
    unittest.main()
