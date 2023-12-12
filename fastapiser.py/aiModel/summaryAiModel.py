from transformers import PreTrainedTokenizerFast, BartForConditionalGeneration
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import nltk
nltk.download('punkt')

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import logging
import uvicorn
from pydantic import BaseModel, Field
from datetime import datetime, time

tokenizer = None
model = None
def modelSetup(): 
    #  Load Model and Tokenize
    global tokenizer
    global model
    # model_dir = "lcw99/t5-large-korean-text-summary"
    # model_dir = "digit82/kobart-summarization"
    model_dir = "gogamza/kobart-summarization"
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_dir)
    
async def onStartUp():
    log.info('Initializing API ...')
    modelSetup()
    
async def onShutDown():
    log.info('Shutting down API')
    
app = FastAPI(on_startup=[onStartUp], on_shutdown=[onShutDown])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# initialize logger
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
log = logging.getLogger(__name__)

class DataInput(BaseModel):
    inputText: str
class SummaryOut(BaseModel):
    summary: str

max_input_length = 512 + 256

@app.post("/summary")
async def websocket_endpoint(data_request: DataInput):
    returnSummary: SummaryOut = None
    try:
        print(f"[{datetime.now()}] data_request =>", data_request[0:100])
        text: str =  data_request.inputText
        # print(f'[Question] => {text}')      


        raw_input_ids = tokenizer.encode(text)
        input_ids = [tokenizer.bos_token_id] + raw_input_ids + [tokenizer.eos_token_id]

        summary_ids = model.generate(torch.tensor([input_ids]),  num_beams=4,  max_length=4000,  eos_token_id=1)
        predicted_title = tokenizer.decode(summary_ids.squeeze().tolist(), skip_special_tokens=True)


        # inputs = ["summarize: " + data_request.inputText]

        # inputs = tokenizer(inputs, max_length=max_input_length, truncation=True, return_tensors="pt")
        # output = model.generate(**inputs, num_beams=8, do_sample=True, min_length=100, max_length=250)
        # decoded_output = tokenizer.batch_decode(output, skip_special_tokens=True)[0]
        # predicted_title = nltk.sent_tokenize(decoded_output.strip())[0]

        # print(f'[summary] => {predicted_title}')
        
        returnSummary: SummaryOut = predicted_title
        print(f"[{datetime.now()}] data response =>", returnSummary)
    except Exception as e:
        print(f'websocket_endpoint EXCEPTION => {e}')
    print(f"[{datetime.now()}] News Summary Ai Model Wait...........")
    return returnSummary

if __name__ == "__main__":
    # TODO 로컬 배포
    #uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
    # TODO 실서버 배포
    uvicorn.run(app, host="0.0.0.0", port=8010)