import asyncio
import base64

import aio_pika
import gino
from gino.ext.sanic import Gino
from sanic import Sanic, response
from sanic.response import json
from sanic_openapi import swagger_blueprint

app = Sanic("Image")


app.config.DB_HOST = 'localhost'
app.config.DB_DATABASE = 'gino'
db = Gino()
db.init_app(app)



def code_base64():
    jpgtxt = base64.encodebytes(open("py.jpeg", "rb").read())
    f = open("jpg1_b64.txt", "wb")
    f.write(jpgtxt)
    f.close()
    return jpgtxt.decode()
    # return str(jpgtxt)[:-3].replace("'","").replace("b","",1).replace(" ","")


""" Работа с бд """
class User(db.Model):
    __tablename__ = 'image'
    id = db.Column(db.Integer(), primary_key=True)
    picture = db.Column(db.Text())


async def main():
    await db.set_bind('postgresql://localhost/gino')
    await db.gino.create_all()
    img_code = code_base64()
    user = await User.create(picture = img_code)


async def no_main(loop):
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@127.0.0.1/", loop=loop
    )
    str_image = code_base64()
    async with connection:
        routing_key = "images"

        channel = await connection.channel()

        await channel.default_exchange.publish(
            aio_pika.Message(str_image.encode()),
            routing_key=routing_key,
        )

@app.route("/api/image_ch")
async def image_get(request):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(no_main(loop))
    loop.close()
    return response.text('Изображение отправлено на обработку')
    # code_image = code_base64()
    # return response.text(code_image)

""" Картинка до изменений """
@app.route("/api/image_old", methods=['GET', 'POST'])
async def image_post(request):
    return await response.file('/home/alekseit/MyApp/py.jpeg')
    

""" Картинка после изменений """
@app.route("/api/image_new", methods=['GET', 'POST'])
async def image_post1(request):
    return await response.file('/home/alekseit/MyApp/py.png')

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
    app.run(host="0.0.0.0", port=8000)
