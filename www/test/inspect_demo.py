import inspect

def foo(a, *, b:int, **kw):
    print(a, b)
    # pass

foo(1, b=3, c=666)

sig = inspect.signature(foo)
params = sig.parameters
# print(inspect.Parameter.KEYWORD_ONLY, inspect.Parameter.VAR_KEYWORD)
for name, param in params.items():
    print(name, param.kind, param.default is param.empty)
# print(params, params.items())