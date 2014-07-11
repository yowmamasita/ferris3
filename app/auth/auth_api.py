import endpoints
from protopigeon.types import UserMessage
from ferris3 import auto_class, auto_method, Service


@auto_class   
class AuthInfoApi(Service):

    @auto_method(returns=UserMessage)
    def info(self, request):    
        user = endpoints.get_current_user()
        if user:
            return UserMessage(
                email=user.email(),
                user_id=user.user_id(),
                nickname=user.nickname())
        return UserMessage()
