from langserve import RemoteRunnable

# Initialize the remote chain
translate_chain = RemoteRunnable("http://localhost:8000/translate")

# Example invocation
response = translate_chain.invoke({
    "language": "French",  # Target language
    "text": "Hello world"  # Text to translate
})

print("Translation result:", response)