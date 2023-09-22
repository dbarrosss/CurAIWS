import asyncio
import websockets
import questions
import signal


async def websocket_handler(websocket):
    current_node = 0
    X = questions.carregar_csv()
    modelo_carregado = questions.carregar_ia()
    visited_nodes = []
    
    while True:
        pergunta = questions.fazer_perguntas(modelo_carregado, current_node, X.columns)

        if type(pergunta) == list:
            await websocket.send(pergunta[0])
            await websocket.close()
            break

        await websocket.send(pergunta)

        resposta = await websocket.recv()

        if resposta.lower() == 'sim':
            current_node = modelo_carregado.tree_.children_right[current_node]
        elif resposta.lower() == 'voltar':
            current_node = visited_nodes.pop()
        else:
            current_node = modelo_carregado.tree_.children_left[current_node]


async def main():
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)
    async with websockets.serve(websocket_handler, host='', port=8765):
        await stop


if __name__ == "__main__":
    asyncio.run(main())
