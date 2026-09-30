import unittest

from game.assets import SOUND_DIR, SOUND_FILES
from game.content import GOAL_SAVINGS, HOUSING
from game.state import GameState


class GameStateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.state = GameState()

    def test_required_sound_files_exist(self) -> None:
        for filename in SOUND_FILES.values():
            self.assertTrue((SOUND_DIR / filename).is_file(), filename)

    def test_initial_outfit_only_unlocks_entry_job(self) -> None:
        self.assertIsNone(self.state.work_blocker("harbor_assistant"))
        self.assertIn("Kjøp", self.state.work_blocker("store_assistant") or "")

    def test_buying_outfit_equips_it(self) -> None:
        self.state.money = 500
        bought, message = self.state.buy_outfit("casual")
        self.assertTrue(bought)
        self.assertIn("kjøpt", message)
        self.assertEqual(self.state.current_outfit, "casual")
        self.assertEqual(self.state.money, 200)
        self.assertIsNone(self.state.work_blocker("store_assistant"))
        self.assertIsNone(self.state.work_blocker("clothing_sales"))

    def test_school_grades_follow_norwegian_levels(self) -> None:
        for expected_grade in range(2, 8):
            self.state.money = 500
            changed, _ = self.state.study(university=False)
            self.assertTrue(changed)
            self.assertEqual(self.state.education_grade, expected_grade)
        self.assertEqual(self.state.education_label, "Barneskole")
        self.state.owned_outfits.add("hoodie")
        self.state.education_grade = 8
        self.assertIsNone(self.state.work_blocker("warehouse"))

    def test_university_requires_fagskole(self) -> None:
        changed, message = self.state.study(university=True)
        self.assertFalse(changed)
        self.assertIn("Fagskole", message)

    def test_school_stops_before_university_grade(self) -> None:
        self.state.education_grade = 15
        self.state.money = 1000
        changed, message = self.state.study(university=False)
        self.assertFalse(changed)
        self.assertIn("universitetet", message.lower())

    def test_university_grades_follow_bachelor_master_doctorate(self) -> None:
        self.state.education_grade = 15
        self.state.money = 1000
        changed, _ = self.state.study(university=True)
        self.assertTrue(changed)
        self.assertEqual(self.state.education_grade, 16)
        self.assertEqual(self.state.education_label, "Bachelor")

    def test_completed_shift_pays_wage(self) -> None:
        self.state.money = 500
        started, _ = self.state.start_shift("harbor_assistant")
        self.assertTrue(started)
        message = self.state.update_shift(10)
        self.assertIn("120", message or "")
        self.assertEqual(self.state.money, 620)
        self.assertIn("harbor_assistant", self.state.completed_jobs)

    def test_cheap_house_and_sleep(self) -> None:
        self.state.money = HOUSING["freeway_house"].price + 100
        changed, _ = self.state.buy_home("freeway_house")
        self.assertTrue(changed)
        self.assertTrue(self.state.apartment)
        self.assertEqual(self.state.home_id, "freeway_house")
        self.state.energy = 10
        rested, _ = self.state.sleep()
        self.assertTrue(rested)
        self.assertAlmostEqual(self.state.energy, 41.5)

    def test_middle_house_uses_65_percent_rest(self) -> None:
        self.state.money = HOUSING["middle_house"].price + 100
        changed, _ = self.state.buy_home("middle_house")
        self.assertTrue(changed)
        self.state.energy = 0
        rested, _ = self.state.sleep()
        self.assertTrue(rested)
        self.assertAlmostEqual(self.state.energy, 65.0)

    def test_exclusive_house_is_more_expensive_and_upgrades(self) -> None:
        self.state.money = HOUSING["exclusive_house"].price + 100
        changed, _ = self.state.buy_home("exclusive_house")
        self.assertTrue(changed)
        self.assertEqual(self.state.home_id, "exclusive_house")
        self.assertEqual(self.state.money, 100)
        self.state.energy = 0
        rested, _ = self.state.sleep()
        self.assertTrue(rested)
        self.assertEqual(self.state.energy, 100.0)
        self.assertEqual(self.state.daily_housing_cost, HOUSING["exclusive_house"].rent)

    def test_clothing_levels_must_be_bought_in_order(self) -> None:
        self.state.money = 10_000
        blocked, message = self.state.buy_outfit("suit")
        self.assertFalse(blocked)
        self.assertIn("Casual", message)
        self.assertTrue(self.state.buy_outfit("casual")[0])
        self.assertTrue(self.state.buy_outfit("hoodie")[0])
        self.assertTrue(self.state.buy_outfit("boilersuit")[0])
        self.assertTrue(self.state.buy_outfit("looser")[0])
        self.assertTrue(self.state.buy_outfit("suit")[0])

    def test_pharmacy_food_restores_needs(self) -> None:
        self.state.money = 100
        self.state.hunger = 20
        self.state.energy = 20
        changed, _ = self.state.buy_pharmacy_food()
        self.assertTrue(changed)
        self.assertEqual(self.state.hunger, 50)
        self.assertEqual(self.state.energy, 30)

    def test_church_rest_restores_ten_percent_once_per_day(self) -> None:
        self.state.energy = 20
        changed, _ = self.state.sleep_church()
        self.assertTrue(changed)
        self.assertAlmostEqual(self.state.energy, 28.0)
        changed_again, message = self.state.sleep_church()
        self.assertFalse(changed_again)
        self.assertIn("allerede", message)

    def test_xp_progress_and_career_level(self) -> None:
        self.state.add_xp(120)
        self.assertEqual(self.state.xp, 120)
        self.assertEqual(self.state.career_level, 2)
        self.assertAlmostEqual(self.state.xp_progress, 0.2)

    def test_goal_requires_exclusive_house_and_consultant_shift(self) -> None:
        self.state.education_grade = 21
        self.state.home_id = "exclusive_house"
        self.state.apartment = True
        self.state.money = GOAL_SAVINGS
        self.state.owned_outfits.add("suit")
        self.state.completed_jobs.add("consultant")
        self.assertTrue(self.state.update_goal())
        self.assertFalse(self.state.update_goal())

    def test_cheap_house_does_not_complete_goal(self) -> None:
        self.state.education_grade = 21
        self.state.home_id = "freeway_house"
        self.state.apartment = True
        self.state.money = GOAL_SAVINGS
        self.state.completed_jobs.add("consultant")
        self.assertFalse(self.state.update_goal())


if __name__ == "__main__":
    unittest.main()
