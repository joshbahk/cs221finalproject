from cambio.actions import Action


def test_action_creation():
    action = Action.make("replace_self", slot=2)
    assert action.kind == "replace_self"
    assert action.get("slot") == 2
    assert action.to_json() == {
        "kind": "replace_self",
        "params": {"slot": 2},
    }