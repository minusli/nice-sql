from nicesql import utils
from nicesql.utils import pick_value


def test_pick_value():
    data = {
        "f1": "a",
        "f2": 2,
        "f3": {
            "f4": "b",
            "f5": 3,
            "f6": [
                "l1", "l2", "l3"
            ],
        },
        "f7": [
            {
                "f8": "f8-1",
                "f9": [1, 2, 3]
            },
            {
                "f8": "f8-2",
                "f9": [1, 2, 3]
            },
            {
                "f8": "f8-3",
                "f9": [1, 2, 3]
            }
        ],
        "f10": {
            "f11": [
                [{"f12": [1]}],
                [{"f12": [2]}],
                [{"f12": 3}],
            ]
        },
        "f13": '{"a": 1}',
        "f14": 0.01123,
        "f15": 0.01,
        "f16": 23.79
    }

    assert pick_value(data, "f1") == "a"
    assert pick_value(data, "f2") == 2
    assert pick_value(data, "f2|str") == "2"
    assert pick_value(data, "f3.f4") == "b"
    assert pick_value(data, "f3.f5") == 3
    assert pick_value(data, "f3.f5 | str  ") == "3"
    assert pick_value(data, "f3.f6") == ["l1", "l2", "l3"]
    assert pick_value(data, "f3.f6") == ["l1", "l2", "l3"]
    assert pick_value(data, "f3.f6|jsondump") == '["l1", "l2", "l3"]'
    assert pick_value(data, "f7.f8") == ["f8-1", "f8-2", "f8-3"]
    assert pick_value(data, "f7.f9") == [[1, 2, 3], [1, 2, 3], [1, 2, 3]]
    assert pick_value(data, "f10.f11.f12") == [[[1]], [[2]], [3]]
    assert pick_value(data, "f13 | jsonload") == {"a": 1}
    assert pick_value(data, "f14 | %") == "1.123%"
    assert pick_value(data, "f14 | % 0") == "1%"
    assert pick_value(data, "f14 | % 1") == "1.1%"
    assert pick_value(data, "f14 | % 2") == "1.12%"
    assert pick_value(data, "f14 | % 3") == "1.123%"
    assert pick_value(data, "f14 | % 4") == "1.1230%"
    assert pick_value(data, "f14 | % 5") == "1.12300%"
    assert pick_value(data, "f15 | %") == "1%"
    assert pick_value(data, "f16 | int") == 23
    assert pick_value(data, "f16 | float") == 23.79
    assert pick_value(data, "f16 | ceil") == 24
    assert pick_value(data, "f16 | floor") == 23
    assert pick_value(data, "f16 | round") == 24
    assert pick_value(data, "f16 | round 1") == 23.8


def test_fill_model():
    class A:
        def __init__(self):
            self.a = None
            self.b = None
            self.d = D()

        # noinspection PyMethodMayBeStatic
        def c(self):
            return False

    class D:
        def __call__(self, *args, **kwargs):
            pass

    m = utils.fill_model(A(), a="a", b="b", c="c", d="d")
    assert m.a == "a"
    assert m.b == "b"
    assert m.c != "c"
    assert m.d == "d"


def test_parse_db_url():
    cases = [
        ("mysql://192.168.1.1:3306/test_db?msg=hello world", {
            "type": "mysql",
            "host": "192.168.1.1",
            "port": 3306,
            "database": "test_db",
            "msg": "hello world",
        }),
        (" sqlite:///:memory:?msg=hello world", {
            "type": "sqlite",
            "host": None,
            "port": None,
            "database": ":memory:",
            "msg": "hello world",
        }),
    ]
    for url, result in cases:
        r = utils.parse_db_url(url)
        assert r == result, url
