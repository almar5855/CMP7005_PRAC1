
#import streamlit as st
#import pandas as pd

#df = pd.read_csv('processed.csv')
#df.head()
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

@app.get("/hello")
def read_root():
    return {"message": "Hello, World!"}
