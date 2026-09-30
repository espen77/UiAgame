import unittest

from game.content import GOAL_SAVINGS, HOUSING
from game.state import GameState


class GameStateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.state = GameState()

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

    def test_three_school_weeks_unlock_fagskole(self) -> None:
        for _ in range(3):
            self.state.money = 500
            changed, _ = self.state.study(university=False)
            self.assertTrue(changed)
        self.assertEqual(self.state.education_level, 1)
        self.state.owned_outfits.add("hoodie")
        self.assertIsNone(self.state.work_blocker("warehouse"))

    def test_university_requires_videregaende(self) -> None:
        changed, message = self.state.study(university=True)
        self.assertFalse(changed)
        self.assertIn("videregående", message)

    def test_school_stops_before_university_level(self) -> None:
        self.state.education_progress = 6
        self.state.money = 1000
        changed, message = self.state.study(university=False)
        self.assertFalse(changed)
        self.assertIn("universitetet", message.lower())

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
        self.assertEqual(self.state.energy, HOUSING["freeway_house"].recovery)

    def test_sea_house_is_more_expensive_and_upgrades(self) -> None:
        self.state.money = HOUSING["sea_house"].price + 100
        changed, _ = self.state.buy_home("sea_house")
        self.assertTrue(changed)
        self.assertEqual(self.state.home_id, "sea_house")
        self.assertEqual(self.state.money, 100)
        self.state.energy = 0
        rested, _ = self.state.sleep()
        self.assertTrue(rested)
        self.assertEqual(self.state.energy, HOUSING["sea_house"].recovery)
        self.assertEqual(self.state.daily_housing_cost, HOUSING["sea_house"].rent)

    def test_goal_requires_consultant_shift(self) -> None:
        self.state.education_progress = 9
        self.state.apartment = True
        self.state.money = GOAL_SAVINGS
        self.state.owned_outfits.add("suit")
        self.state.completed_jobs.add("consultant")
        self.assertTrue(self.state.update_goal())
        self.assertFalse(self.state.update_goal())


if __name__ == "__main__":
    unittest.main()
