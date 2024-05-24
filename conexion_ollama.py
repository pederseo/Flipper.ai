from langchain_community.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def conect(pregunta):
    # Configuración del modelo
    MODEL = 'gemma'
    llm = Ollama(model=MODEL, callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]), temperature=0.2)

    # pregunta = input('Has tu pregunta, "Piup"?')
    # El molde de la consulta o pregunta es prompts template y no se muestra
    consulta = PromptTemplate(
        input_variables=['topics'], # Las variables de entrada
        template=(f'''"Create a chatbot, who is an expert in Python and helps users like a cheatsheet.
                   you are humorous and charismatic, often interjecting 'piup!!' between words. Responses should be limited
                   to a maximum of 200 characters,make the answer in spanish."{pregunta}''')
    )

    # La cadena o estructura de respuesta dado la consulta
    chain = LLMChain(llm=llm, prompt=consulta, verbose=False) # Verbose evita alucinaciones

    # Respuesta
    respuesta = chain.invoke({'topics':''})

    # Limitar la respuesta a 150 caracteres
    respuesta_texto = respuesta['text'][:500]
    return respuesta_texto

