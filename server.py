import asyncio
import websockets
import questions


async def websocket_handler(websocket, path):
    await websocket.accept()
    current_node = 0
    
    X = questions.carregar_csv()
    modelo_carregado = questions.carregar_ia()
    
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
        else:
            current_node = modelo_carregado.tree_.children_left[current_node]


async def main():
    async with websockets.serve(websocket_handler, host='', port=8765):
        await asyncio.Future()  # Mantém o servidor WebSocket em execução


if __name__ == "__main__":
    asyncio.run(main())
