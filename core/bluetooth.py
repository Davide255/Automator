import asyncio
from winrt.windows.devices.radios import Radio, RadioState

async def _set_state(state: RadioState):
    
    info = await Radio.get_radios_async()
    bluetooth = info.first().current

    if bluetooth.state != state: #Don't change the status if it's already set 
        await bluetooth.set_state_async(state)
    return True

def set_on():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(_set_state(RadioState.ON))
    loop.close()
    return True

def set_off():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(_set_state(RadioState.OFF))
    loop.close()
    return True