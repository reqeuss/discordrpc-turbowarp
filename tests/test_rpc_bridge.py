import unittest

from resources.rpc.rpc_bridge import (
    build_party_size,
    make_presence_kwargs,
    optional_int,
    parse_bool,
)


class PresencePayloadTests(unittest.TestCase):
    def test_empty_optional_integer(self):
        self.assertIsNone(optional_int({}, "start"))
        self.assertIsNone(optional_int({"start": ""}, "start"))
        self.assertIsNone(optional_int({"start": "not-a-number"}, "start"))

    def test_integer_is_converted(self):
        self.assertEqual(optional_int({"start": "123"}, "start"), 123)

    def test_party_size_valid(self):
        self.assertEqual(build_party_size({"partySize": "2", "partyMax": "5"}), [2, 5])

    def test_party_size_rejects_invalid_values(self):
        self.assertIsNone(build_party_size({"partySize": "6", "partyMax": "5"}))
        self.assertIsNone(build_party_size({"partySize": "1", "partyMax": "0"}))
        self.assertIsNone(build_party_size({"partySize": "x", "partyMax": "5"}))

    def test_boolean_parsing(self):
        self.assertTrue(parse_bool(True))
        self.assertTrue(parse_bool("true"))
        self.assertFalse(parse_bool(False))
        self.assertFalse(parse_bool("false"))
        self.assertTrue(parse_bool(None, default=True))

    def test_payload_uses_pypresence_argument_names(self):
        payload = make_presence_kwargs({
            "details": "In a test",
            "state": "Testing",
            "start": "100",
            "end": "200",
            "largeImage": "game_icon",
            "partySize": "1",
            "partyMax": "4",
            "joinSecret": "join-value",
            "spectateSecret": "spectate-value",
            "instance": "false",
        })
        self.assertEqual(payload["details"], "In a test")
        self.assertEqual(payload["start"], 100)
        self.assertEqual(payload["large_image"], "game_icon")
        self.assertEqual(payload["party_size"], [1, 4])
        self.assertEqual(payload["join"], "join-value")
        self.assertEqual(payload["spectate"], "spectate-value")
        self.assertFalse(payload["instance"])
        self.assertNotIn("secrets", payload)


if __name__ == "__main__":
    unittest.main()
