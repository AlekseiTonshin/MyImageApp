import asyncio
import base64
import sys

import aio_pika
import PIL
from PIL import Image


async def no_main(loop):
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@127.0.0.1/", loop=loop
    )
    queue_name = "images"

    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(queue_name, auto_delete=True)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    image_code = message.body
                    # image_code =(message.body).replace("'","").replace("b","",1).replace(" ","")
                    print(image_code)
                    newjpgtxt = image_code
                    g = open("py1.jpeg", "wb")
                    g.write(base64.decodebytes(newjpgtxt))
                    g.close()
                    resize_image(input_image_path='py1.jpeg',
                    output_image_path='py1.jpeg',
                    size=(100, 50))
                    save()
                    # return image_code.encode()


# def uncode_image():
#     newjpgtxt = no_main(loop)
#     g = open("py1.jpeg", "wb")
#     g.write(base64.decodebytes(newjpgtxt))
#     g.close()

def resize_image(input_image_path,
                 output_image_path,
                 size):
    original_image = Image.open(input_image_path)
    width, height = original_image.size
    # print('The original image size is {wide} wide x {height} '
    #       'high'.format(wide=width, height=height))
 
    resized_image = original_image.resize(size)
    width, height = resized_image.size
    # print('The resized image size is {wide} wide x {height} '
    #       'high'.format(wide=width, 2=height))
    # resized_image.show()
    resized_image.save(output_image_path)

def save():
    try:
        pyt = Image.open("py.jpeg")
    except IOError:
        print("Unable to load image")
        sys.exit(1)
    pyt.save('py.png', 'png')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(no_main(loop))
    loop.close()
    # resize_image(input_image_path='py1.jpeg',
    #              output_image_path='py2.jpeg',
    #              size=(100, 50))
    # save()
