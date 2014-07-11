import endpoints
from protorpc import messages, remote
from protopigeon.types import UserMessage
from ferris3.endpoints import auto_method
from ferris3 import apis

api = apis.default()

@api.api_class(resource_name='info', path='info')   
class AuthInfoApi(remote.Service):

    @auto_method(returns=UserMessage)
    def info(self, request):    
        user = endpoints.get_current_user()
        if user:
            return UserMessage(
                email=user.email(),
                user_id=user.user_id(),
                nickname=user.nickname())
        return UserMessage()
