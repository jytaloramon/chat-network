from framework.router import Router, RouterManager
from server.controllers import user_auth

router_use = Router(10, 'user')
router_use.auth(user_auth)

router_manager = RouterManager()
router_manager.add_router(router_use)