import asyncio
import websockets
import pickle
import pymetamap


def _get_concept(sen):
    result = asyncio.get_event_loop().run_until_complete(_send_sentence(sen))
    return result[0]


async def _send_sentence(sen):
    uri = "ws://127.0.0.1:7777"
    async with websockets.connect(uri) as websocket:
        await websocket.send(sen)
        result = await websocket.recv()
        return pickle.loads(result)


def get_concept_dict(triple_dict_input, neg=False):
    sub_str = triple_dict_input['sub']
    obj_str = triple_dict_input['obj']

    concepts = _get_concept(sub_str + "," + obj_str)

    if not concepts:
        print("No mapping found for any of the elements.")
        return None

    try:
        sub = [c for c in concepts if sub_str in c.trigger][0]
        obj = [c for c in concepts if obj_str in c.trigger][0]

    except IndexError:
        print("No mapping found for one of the elements.")
        return None

    return {
        'sub': sub,
        'obj': obj,
        'rel': triple_dict_input['rel'].upper(),
        'neg': neg,
        'sub_extra': triple_dict_input['sub_extra'],
        'obj_extra': triple_dict_input['obj_extra'],
    }


if __name__ == "__main__":

    input_dict = {
        'sub': "diabetes",
        'obj': "heart attack",
        'rel': "causes",
        'sub_extra': {},
        'obj_extra': {},
    }

    triple_dict = get_concept_dict(input_dict)
    print(triple_dict)
