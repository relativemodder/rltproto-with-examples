
class RLTProto {

    constructor(ws_adress = `ws://${location.host}/rltproto`) {
        this.ws_adress = ws_adress;
        this.listeners = [];
    }

    addEventListener = (callbackFn) => {
        this.listeners.push(callbackFn)
    }

    listen = () => {
        this.websocket.addEventListener('message', ((event) => {
            this.listeners.forEach((callbackFn) => {
                callbackFn(JSON.parse(event.data))
            })
        }));
    }

    send = (obj) => {
        this.websocket.send(JSON.stringify(obj))
    }

    connect = (user_id, callbackFn) => {
        this.websocket = new WebSocket(`${this.ws_adress}/${user_id}`);
        this.websocket.addEventListener('open', (event) => {
            callbackFn();
        });
    }
}