import json

import aiofiles


async def read_provider_response(
        file_path: str,
) -> list[dict]:
    async with aiofiles.open(file_path, mode='r') as f:
        contents = await f.read()
    return json.loads(contents)
