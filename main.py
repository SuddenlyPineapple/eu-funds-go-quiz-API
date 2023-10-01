import json
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from fastapi import Response
from fastapi.encoders import jsonable_encoder

from get_regions_helper import get_regions_helper

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

df = pd.read_csv('csv_Lista_projektow_FE_2014_2020_030923.csv', sep=';')
df.columns = df.columns.str.replace(' ', '')
# df = df['Miejscerealizacjiprojektu/Projectlocation'].str.split(' | ').explode().reset_index(drop=True)
# df[['WOJ', 'POW']] = df['Miejscerealizacjiprojektu/Projectlocation'].str.extract(r'WOJ\.: (.*), POW\.: (.*)')


# get root logger
logger = logging.getLogger(__name__)

def createQuestion(id, question, correct_answer_id, answers):
    return {
        "id": id,
        "question": question,
        "correct_answer_id": correct_answer_id,
        "answers": answers
    }

@app.get("/")
async def root():
    health = {"status": "ok"}
    return health


@app.get("/regions")
async def get_regions():
    # df_regions = df['Region'].unique()
    result = get_regions_helper(df)
    return result

@app.get("/questions")
async def get_questions(region = 'Cały Kraj', powiat = None):
    # df_regions = df['Region'].unique()

    df_copy = df.copy()

    payload = [
        createQuestion(1, "Czy wiesz ile jest projektów w wybranym obszarze?",3,[
                { "id": 1, "answer": "10" },
                { "id": 2, "answer": "12"},
                { "id": 3, "answer": "16"},
                { "id": 4, "answer": "20"},
        ],),
        createQuestion(2, "Czy wiesz jaka jest łączna zainwestowana wartość projektów w mln zł?", 2, [
            {"id": 1, "answer": "15 mln zł"},
            {"id": 2, "answer": "40 mln zł"},
            {"id": 3, "answer": "60 mln zł"},
            {"id": 4, "answer": "20 mln zł"},
        ],),
        createQuestion(3, "Czy wiesz jaka jest łączna kwota dofinansowania z EU w mln zł?", 4, [
            {"id": 1, "answer": "7 mln zł"},
            {"id": 2, "answer": "20 mln zł"},
            {"id": 3, "answer": "1 mln zł"},
            {"id": 4, "answer": "30 mln zł"},
        ], ),
        createQuestion(4, "Jaki projekt zdobył największą kwotę dofinansowania?", 1, [
            {"id": 1, "answer": "Działania informacyjne dotyczące skutków brexitu skierowane do przedsiębiorców i obywateli."},
            {"id": 2, "answer": "Wdrożenie nowych produktów do oferty w celu złagodzenia skutków brexit"},
            {"id": 3, "answer": "Inwestycja w środki trwałe w celu zmniejszenia negatywnych skutków brexit w przedsiębiorstwie Borcox"},
            {"id": 4, "answer": "Uruchomienie linii do produkcji lamp i kloszy do lamp w celu niwelowania negatywnych skutków brexitu"},
        ], ),
        createQuestion(5, "Jaki pryiorytet miał największy udział w liczbie projektów w wybranym obszarze?", 2, [
            {"id": 1, "answer": "Rynek pracy otwarty dla wszystkich"},
            {"id": 2, "answer": "Wsparcie innowacji w przedsiębiorstwach"},
            {"id": 3, "answer": "Ochrona środowiska i dziedzictwa kulturowego"},
            {"id": 4, "answer": "Rozwój infrastruktury społecznej"},
        ], ),
    ]

    return payload

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)