import structlog
import asyncio
import time

structlog.configure(
    processors=[
        structlog.processors.CallsiteParameterAdder([structlog.processors.CallsiteParameter.FUNC_NAME, structlog.processors.CallsiteParameter.THREAD_NAME]),
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt='%H:%M:%S.%f', utc=False),
        structlog.dev.ConsoleRenderer(),
    ]
)
log: structlog.stdlib.BoundLogger = structlog.get_logger()

async def f():
    log.info("starting f")
    await asyncio.sleep(1)
    log.info("f")

def g():
    log.info("starting g")
    time.sleep(3)
    log.info("g")

async def m():
    t1 = asyncio.create_task(f())
    t2 = asyncio.create_task(asyncio.to_thread(g))
    await t1
    await t2

    # t1, t2 = await asyncio.gather(f(), asyncio.to_thread(g))
                            
asyncio.run(m())
