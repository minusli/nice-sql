from nicesql.utils import getvalue, parsesql


def test_parsesql():
    sql = """
        select * from a, b, c
        where a=1 and b = {user.name} and c = {user.id} and d = { user.a }
        limit 1
    """

    sql, params = parsesql(sql)
    assert sql == """
        select * from a, b, c
        where a=1 and b = ? and c = ? and d = ?
        limit 1
    """
    assert params[0] == 'user.name'
    assert params[1] == 'user.id'
    assert params[2] == 'user.a'


def test_getvalue():
    data = {
        "a": {
            "b": "b1"
        },
        "c": "c1",
        "d": [
            {"e": "e1"},
            {"e": "e2"}
        ]
    }
    assert getvalue(data, "a") == {"b": "b1"}
    assert getvalue(data, "a.b") == "b1"
    assert getvalue(data, "a.b") != "b2"
    assert getvalue(data, "c") == "c1"
    assert getvalue(data, "d") == [{"e": "e1"}, {"e": "e2"}]
    assert getvalue(data, "d.e") == ["e1", "e2"]
    assert getvalue(data, "d.e") != ["e2", "e1"]
