from flask import Flask, request, Response, make_response, jsonify
from contextlib import suppress
from PIL import Image
from random import randint
from typing import TypedDict, Any

app = Flask(__name__)


class ClientState(TypedDict):
    approved: bool
    authtoken: str
    images: list[str]
    # ip: str
    name: str
    netid: str
    tilesize: int
    url: str
    xdim: int
    ydim: int


CLIENT_STATES: list[ClientState] = []


def init_client(id, client: dict[str, Any]) -> ClientState:
    return ClientState(
        approved=False,
        authtoken=client["token"],
        images=[],
        # ip="",  # TODO
        name=client["author"],
        netid=id,
        tilesize=randint(1, 10),
        url=client["url"],
        xdim=randint(1, 50),
        ydim=randint(1, 50),
    )


@app.route("/")
def index() -> Response:
    return Response()


@app.route("/registerClient/<string:client_id>")
def PUT_registerClient(client_id: str) -> Response:
    if json := request.json:
        with suppress(KeyError):
            client = init_client(client_id, json)
            CLIENT_STATES.append(client)

            return make_response(
                jsonify(
                    {
                        "xdim": client["xdim"],
                        "ydim": client["ydim"],
                        "tilesize": client["tilesize"],
                    }
                ),
                200,
            )

    return make_response("Bad request", 400)
