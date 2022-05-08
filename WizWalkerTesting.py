import asyncio

import wizwalker.utils
from wizwalker import WizWalker

wizwalker.utils.override_wiz_install_location("E:\Wizard101")


async def main():
    # walker = WizWalker()
    # client = walker.get_new_clients()[0]
    wizwalker.WizWalker.start_wiz_client()
    # await client.activate_hooks()
    # await client.camera_elastic()
    # print(await client.backpack_space())
    # await walker.close()

asyncio.run(main())
