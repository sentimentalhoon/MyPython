import openai

openai.api_key = "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"
# get API key from top-right dropdown on OpenAI website

# print(openai.Engine.list())  # check we have authenticated

MODEL = "text-embedding-ada-002"

res = openai.Embedding.create(
    input=[
        "Sample document text goes here",
        "there will be several phrases in each batch"
    ], engine=MODEL
)
print(res)

