from qmltorch import hello


def test_public_smoke_message() -> None:
    assert hello() == "QML Torch: ready to quantum!"
