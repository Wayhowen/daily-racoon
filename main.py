import asyncio

from build import Builder
from configs import default


if __name__ == "__main__":
    builder = Builder(default)
    program_core = builder.build()
    asyncio.run(program_core.run())