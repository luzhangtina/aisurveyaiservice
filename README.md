# AI Service

There are two solutions provided: [api.py](api.py) and [api2.py](api2.py)

[api.py](api.py) provides the API /conversion to call model [surveyModel1](surveyModel1.py) to get response from LLM.
[surveyModel1](surveyModel1.py) is created based on llama3.2. The conversion API streams the response

[api2.py](api2.py) provides the API /conversion to call model llama3.2 to get response from LLM. 
This solution relies on the input messages to provide system prompt. The response is returned once get full response back from LLM.