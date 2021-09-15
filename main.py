import asyncio

from internal.build import Builder
from internal.configs import default


if __name__ == "__main__":
    builder = Builder(default)
    program_core = builder.build()
    asyncio.run(program_core.run())