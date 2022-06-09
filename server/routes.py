from framework.router import Router, RouterManager
from server.controllers import chat_create, chat_list, user_auth

router_use = Router(10, 'user')
router_use.auth(user_auth)

router_chat = Router(11, 'chat')
router_chat.create(chat_create)
router_chat.list(chat_list)


router_message = Router(12, 'message')

router_manager = RouterManager()
router_manager.add_router(router_use)
router_manager.add_router(router_chat)
router_manager.add_router(router_message)
