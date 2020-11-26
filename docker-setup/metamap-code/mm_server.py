import asyncio
import websockets
import pickle


async def sentence_handler(websocket, path):
    sentence = await websocket.recv()
    print("Extracting from sentences: {}".format(sentence))
    result = mm.extract_concepts([sentence])
    await websocket.send(pickle.dumps(result))


if __name__ == "__main__":
    from pymetamap import MetaMap
    mm = MetaMap.get_instance('/mm_app/public_mm/bin/metamap20')
    print("python server started")
    start_server = websockets.serve(sentence_handler, "0.0.0.0", 7777)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
