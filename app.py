import asyncio
import aio_pika
from sanic import Sanic
from sanic.response import json, raw
from models import User, db


app = Sanic("Image")


app.config.DB_HOST = '0.0.0.0'
app.config.DB_DATABASE = 'test'
db.init_app(app)


async def db_image_create():
    await db.set_bind('postgresql://postgres:@0.0.0.0:5432/test')
    await db.gino.create_all()


async def rabbit(loop, id_imgs):
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@127.0.0.1/", loop=loop)
    async with connection:
        routing_key = "imgs"
        channel = await connection.channel()
        await channel.default_exchange.publish(
            aio_pika.Message(body=id_imgs.encode()),
            routing_key=routing_key, )


@app.route("/api/image_ch", methods=['POST'])
async def image_get(request):
    img_dict = request.files.get('file')
    file_parameters = {
    'body': img_dict.body,
    'name': img_dict.name,
    'type': img_dict.type,
    }
    file_body = file_parameters['body']
    image = await User.create(picture_old=file_body)
    id_imgs = await User.select('id').where(User.picture_old==file_body).gino.scalar()
    id_imgs = str(id_imgs)
    await rabbit(request.app.loop, id_imgs=id_imgs)
    return json({'Изображение сохранено под номером': id_imgs})


""" Картинка до изменений """


@app.route("/api/image_old/<id_img>", methods=['GET'])
async def image_post(request, id_img):
    images = await User.get_or_404(int(id_img))
    img = images.picture_old
    return raw(img)


""" Картинка после изменений """


@app.route("/api/image_new/<id_img1>", methods=['GET'])
async def image_post1(request, id_img1):
    images = await User.get_or_404(int(id_img1))
    img = images.picture_new
    return raw(img)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(db_image_create())
    app.run(host="0.0.0.0", port=8000)
