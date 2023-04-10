from functools import wraps

class UserMock:
    def __init__(self, user_id="12345"):
        self.id = user_id

class ApplicationContextMock:
    def __init__(self):
        self.user = UserMock()

class SelectMock:
    def __init__(self, value):
        self.values = [value]

def mock_decorator(*args, **kwargs):
    """Decorate by doing nothing."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            return f(*args, **kwargs)
        return decorated_function
    return decorator

class LoopMock:
    def __init__(self, coro):
        self.coro = coro

    def before_loop(self, coro):
        return
    
    def after_loop(self, coro):
        return
    
    def start(self):
        return

def mock_tasks_loop_decorator(*args, **kwargs):
    def decorator(f):
        return LoopMock(f)
    return decorator

class TimerMock:
    def start(self):
        return
    
def roulette_roll_mock():
    return {"color": "red", "number": 1}
