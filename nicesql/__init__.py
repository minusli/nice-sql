import types

from nicesql.engine.sqlite import Sqlite
from nicesql.sqlengine import execute, select, update, insert, delete, ddl, register, close
from nicesql.sqlmodel import SqlModel
from nicesql.sqlresult import SqlResult

if __name__ == '__main__':
    class A:
        @classmethod
        def a(cls):
            pass

        @staticmethod
        def b():
            pass

        def c(self):
            pass


    def d():
        pass


    a = A()
    print("[A.a]", A.a, isinstance(A.a, types.FunctionType), isinstance(A.a, types.MethodType))
    print("[A.b]", A.b, isinstance(A.b, types.FunctionType), isinstance(A.b, types.MethodType))
    print("[A.c]", A.c, isinstance(A.c, types.FunctionType), isinstance(A.c, types.MethodType))
    print("[a.a]", a.a, isinstance(a.a, types.FunctionType), isinstance(a.a, types.MethodType))
    print("[a.b]", a.b, isinstance(a.b, types.FunctionType), isinstance(a.b, types.MethodType))
    print("[a.c]", a.c, isinstance(a.c, types.FunctionType), isinstance(a.c, types.MethodType))
    print("[d]", d, isinstance(d, types.FunctionType), isinstance(d, types.MethodType))
