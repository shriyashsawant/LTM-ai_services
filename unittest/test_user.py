import unittest

from main import create_user, UserRequest


class TestUser(unittest.TestCase):

    def test_create_user(self):

        user = UserRequest(
            name="Shriyash",
            age=22
        )

        result = create_user(user)

        self.assertEqual(result["name"], "Shriyash")
        self.assertEqual(result["age"], 22)


if __name__ == "__main__":
    unittest.main()