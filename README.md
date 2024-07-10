# strange-ioc-container
I dont know what is it. Some kind of IoC-container i think.
Usage:
# services.py

```py
from abc import ABC, abstractmethod

from notify_service import NotifyService


class NotifyService(ABC):

    @abstractmethod
    def notify(self, getter: str):
        raise NotImplementedError


class NotifyServiceImpl(NotifyService):

    def notify(self, getter: str):
        print('Sending email to', getter)
        

class UserService(ABC):

    def __init__(self, notify_service: NotifyService):
        self.notify_service = notify_service

    @abstractmethod
    def change_password(self, user: dict, new_pwd: str):
        raise NotImplementedError


class UserServiceImpl(UserService):

    def change_password(self, user: dict, new_pwd: str):
        user['password'] = new_pwd
        print('Password changed to', user.get('password'))
        self.notify_service.notify(user.get('email'))
        
```
# container.py
```py
from ioc import Container
from notify_service import NotifyService, NotifyServiceImpl
from user_service import UserService, UserServiceImpl

def define_container():
    container = Container()

    container.register(NotifyService, NotifyServiceImpl)
    container.register(UserService, UserServiceImpl)

    container.wire()
```

# main.py
```py
from container import define_container
from ioc import Provide
from user_service import UserService

define_container()


def change_password(
        new_password: str,
        user_service: UserService = Provide[UserService]
):
    user = {
        'password': '123qwerty',
        'email': 'user@example.com',
    }

    user_service.change_password(user=user, new_pwd=new_password)


if __name__ == '__main__':
    change_password('something_hard')

```

