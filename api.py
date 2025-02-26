from flask import Flask, request, jsonify, Response
from ollama import chat
from ollama import ChatResponse

app = Flask(__name__)

@app.route('/conversion', methods=['POST'])
def next_question():
    input = request.json.get('input')
    
    # option 1: wait until full response returned
    # response = chat(model='surveymodel1', messages=[input])
    # print(response.message.content)
    # return jsonify({'response': response.message.content})

    # option 2: use steaming to return HTTP chunked transfer encoding
    
    def generate():
        stream = chat(
            model='surveymodel1',
            messages=input,
            stream=True,
        )
        for chunk in stream:
            print(f'the response message chunk is {chunk}')
            yield chunk['message']['content']

    return Response(generate(), content_type='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

