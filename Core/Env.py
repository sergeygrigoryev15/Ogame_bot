from typing import Optional, Any, Callable

from environs import Env

BLANK_ENV_VALUE = 'NOT_SET'


env = Env()
env.read_env()


class Environ:

    def __call__(self,
                 name: str, env_type: Callable = env.str,
                 default: Optional[Any] = BLANK_ENV_VALUE,
                 validate: Optional[Callable] = None):
        return env_type(name, default, validate)


environ = Environ()
