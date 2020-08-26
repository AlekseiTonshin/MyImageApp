import asyncio
import io
from io import BytesIO

import aio_pika
from PIL import Image

from models import User, db


async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        # breakpoint()
        img_id = int(message.body)
        print(img_id)
        imgss = await User.select('picture_old').where(User.id == img_id).gino.scalar()
        user = await User.query.where(User.picture_old == imgss).gino.first()
        im = Image.open(BytesIO(imgss)).convert("RGBA")
        size = (50, 50)
        resized_image = im.resize(size)
        imgbytearr = io.BytesIO()
        resized_image.save(imgbytearr, format='PNG')
        imgbytearr = imgbytearr.getvalue()
        await user.update(picture_new=imgbytearr).apply()
        await asyncio.sleep(1)


async def main(loop):
    connection = await aio_pika.connect_robust(
    "amqp://guest:guest@127.0.0.1/", loop=loop)
    queue_name = "imgs"
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=100)
    queue = await channel.declare_queue(queue_name, auto_delete=True)
    await queue.consume(process_message)
    return connection


async def db_image_create():
    await db.set_bind('postgresql://postgres:@0.0.0.0:5432/test')


# async def resize_image(size):

#     imgss = await User.select('picture_old').where(User.id == immg).gino.scalar()
#     print(imgss)
#     original_image = Image.open(io.BytesIO(imgss))
#     # original_image = Image.open(input_image_path)
#     width, height = original_image.size
#     resized_image = original_image.resize(size)
#     image = await User.update(picture_new = resize_image)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(db_image_create())
    loop = asyncio.get_event_loop()
    connection = loop.run_until_complete(main(loop))
    try:
        loop.run_forever()
    finally:
        loop.run_until_complete(connection.close())
