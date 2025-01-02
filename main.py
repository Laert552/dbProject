from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3

# Database settings
DB_NAME = "resources_mining.db"

# Initialize FastAPI app
app = FastAPI(title="Resources Mining API", description="CRUD API for managing resources mining data", version="1.0.0")

# Pydantic models
class Mestorozhdenie(BaseModel):
    name: str
    sposob_razrabotki: str
    zapasy: float
    stoimost_dobychi_ed: float
    punkt_id: int
    poleznoe_iskopaemoe_id: int

class Punkt(BaseModel):
    name: str
    kolichestvo_personala: int
    propusknaya_sposobnost: float
    godovaya_dobycha: float

class PoleznoeIskopaemoe(BaseModel):
    name: str
    tip: str
    edinitsa_izmereniya: str
    rynochnaya_tsena: float

# Database utility functions
def execute_query(query: str, params: tuple = ()):  # For INSERT, UPDATE, DELETE
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor.lastrowid

def fetch_query(query: str, params: tuple = ()):  # For SELECT
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

# CRUD for Mestorozhdenie
@app.get("/mestorozhdenie", response_model=List[Mestorozhdenie])
def get_mestorozhdeniya():
    rows = fetch_query("SELECT * FROM Mestorozhdenie")
    return [Mestorozhdenie(id=row[0], name=row[1], sposob_razrabotki=row[2], zapasy=row[3], stoimost_dobychi_ed=row[4], punkt_id=row[5], poleznoe_iskopaemoe_id=row[6]) for row in rows]

@app.get("/mestorozhdenie/{id}", response_model=Mestorozhdenie)
def get_mestorozhdenie(id: int):
    rows = fetch_query("SELECT * FROM Mestorozhdenie WHERE id = ?", (id,))
    if not rows:
        raise HTTPException(status_code=404, detail="Mestorozhdenie not found")
    row = rows[0]
    return Mestorozhdenie(id=row[0], name=row[1], sposob_razrabotki=row[2], zapasy=row[3], stoimost_dobychi_ed=row[4], punkt_id=row[5], poleznoe_iskopaemoe_id=row[6])

@app.post("/mestorozhdenie", response_model=Mestorozhdenie, status_code=201)
def create_mestorozhdenie(mestorozhdenie: Mestorozhdenie):
    id = execute_query(
        """INSERT INTO Mestorozhdenie (name, sposob_razrabotki, zapasy, stoimost_dobychi_ed, punkt_id, poleznoe_iskopaemoe_id) \
            VALUES (?, ?, ?, ?, ?, ?)""",
        (mestorozhdenie.name, mestorozhdenie.sposob_razrabotki, mestorozhdenie.zapasy, mestorozhdenie.stoimost_dobychi_ed, mestorozhdenie.punkt_id, mestorozhdenie.poleznoe_iskopaemoe_id)
    )
    return {"id": id, **mestorozhdenie.dict()}

@app.put("/mestorozhdenie/{id}", response_model=Mestorozhdenie)
def update_mestorozhdenie(id: int, mestorozhdenie: Mestorozhdenie):
    rows = fetch_query("SELECT * FROM Mestorozhdenie WHERE id = ?", (id,))
    if not rows:
        raise HTTPException(status_code=404, detail="Mestorozhdenie not found")
    execute_query(
        """UPDATE Mestorozhdenie SET name = ?, sposob_razrabotki = ?, zapasy = ?, stoimost_dobychi_ed = ?, punkt_id = ?, poleznoe_iskopaemoe_id = ? \
            WHERE id = ?""",
        (mestorozhdenie.name, mestorozhdenie.sposob_razrabotki, mestorozhdenie.zapasy, mestorozhdenie.stoimost_dobychi_ed, mestorozhdenie.punkt_id, mestorozhdenie.poleznoe_iskopaemoe_id, id)
    )
    return {"id": id, **mestorozhdenie.dict()}

@app.delete("/mestorozhdenie/{id}", status_code=204)
def delete_mestorozhdenie(id: int):
    rows = fetch_query("SELECT * FROM Mestorozhdenie WHERE id = ?", (id,))
    if not rows:
        raise HTTPException(status_code=404, detail="Mestorozhdenie not found")
    execute_query("DELETE FROM Mestorozhdenie WHERE id = ?", (id,))
    return {"message": "Mestorozhdenie deleted successfully"}

# CRUD for Punkt
@app.get("/punkt", response_model=List[Punkt])
def get_punkty():
    rows = fetch_query("SELECT * FROM Punkt")
    return [Punkt(id=row[0], name=row[1], kolichestvo_personala=row[2], propusknaya_sposobnost=row[3], godovaya_dobycha=row[4]) for row in rows]

@app.get("/punkt/{id}", response_model=Punkt)
def get_punkt(id: int):
    rows = fetch_query("SELECT * FROM Punkt WHERE id = ?", (id,))
    if not rows:
        raise HTTPException(status_code=404, detail="Punkt not found")
    row = rows[0]
    return Punkt(id=row[0], name=row[1], kolichestvo_personala=row[2], propusknaya_sposobnost=row[3], godovaya_dobycha=row[4])

@app.post("/punkt", response_model=Punkt, status_code=201)
def create_punkt(punkt: Punkt):
    id = execute_query(
        """INSERT INTO Punkt (name, kolichestvo_personala, propusknaya_sposobnost, godovaya_dobycha) \
            VALUES (?, ?, ?, ?)""",
        (punkt.name, punkt.kolichestvo_personala, punkt.propusknaya_sposobnost, punkt.godovaya_dobycha)
    )
    return {"id": id, **punkt.dict()}

@app.put("/punkt/{id}", response_model=Punkt)
def update_punkt(id: int, punkt: Punkt):
    rows = fetch_query("SELECT * FROM Punkt WHERE id = ?", (id,))
    if not rows:
        raise HTTPException(status_code=404, detail="Punkt not found")
    execute_query(
        """UPDATE Punkt SET name = ?, kolichestvo_personala = ?, propusknaya_sposobnost = ?, godovaya_dobycha = ? \
            WHERE id = ?""",
        (punkt.name, punkt.kolichestvo_personala, punkt.propusknaya_sposobnost, punkt.godovaya_dobycha, id)
    )
    return {"id": id, **punkt.dict()}

@app.delete("/punkt/{id}", status_code=204)
def delete_punkt(id: int):
    rows = fetch_query("SELECT * FROM Punkt WHERE id = ?", (id,))
    if not rows:
        raise HTTPException(status_code=404, detail="Punkt not found")
    execute_query("DELETE FROM Punkt WHERE id = ?", (id,))
    return {"message": "Punkt deleted successfully"}

# CRUD for PoleznoeIskopaemoe
@app.get("/poleznoe_iskopaemoe", response_model=List[PoleznoeIskopaemoe])
def get_poleznye_iskopaemye():
    rows = fetch_query("SELECT * FROM Poleznoe_iskopaemoe")
    return [PoleznoeIskopaemoe(id=row[0], name=row[1], tip=row[2], edinitsa_izmereniya=row[3], rynochnaya_tsena=row[4]) for row in rows]

@app.get("/poleznoe_iskopaemoe/{id}", response_model=PoleznoeIskopaemoe)
def get_poleznoe_iskopaemoe(id: int):
    rows = fetch_query("SELECT * FROM Poleznoe_iskopaemoe WHERE id = ?", (id,))
    if not rows:
        raise HTTPException(status_code=404, detail="PoleznoeIskopaemoe not found")
    row = rows[0]
    return PoleznoeIskopaemoe(id=row[0], name=row[1], tip=row[2], edinitsa_izmereniya=row[3], rynochnaya_tsena=row[4])

@app.post("/poleznoe_iskopaemoe", response_model=PoleznoeIskopaemoe, status_code=201)
def create_poleznoe_iskopaemoe(poleznoe_iskopaemoe: PoleznoeIskopaemoe):
    id = execute_query(
        """INSERT INTO Poleznoe_iskopaemoe (name, tip, edinitsa_izmereniya, rynochnaya_tsena) \
            VALUES (?, ?, ?, ?)""",
        (poleznoe_iskopaemoe.name, poleznoe_iskopaemoe.tip, poleznoe_iskopaemoe.edinitsa_izmereniya, poleznoe_iskopaemoe.rynichnaya_tsena)
    )
    return {"id": id, **poleznoe_iskopaemoe.dict()}

@app.put("/poleznoe_iskopaemoe/{id}", response_model=PoleznoeIskopaemoe)
def update_poleznoe_iskopaemoe(id: int, poleznoe_iskopaemoe: PoleznoeIskopaemoe):
    rows = fetch_query("SELECT * FROM Poleznoe_iskopaemoe WHERE id = ?", (id,))
    if not rows:
        raise HTTPException(status_code=404, detail="PoleznoeIskopaemoe not found")
    execute_query(
        """UPDATE Poleznoe_iskopaemoe SET name = ?, tip = ?, edinitsa_izmereniya = ?, rynochnaya_tsena = ? \
            WHERE id = ?""",
        (poleznoe_iskopaemoe.name, poleznoe_iskopaemoe.tip, poleznoe_iskopaemoe.edinitsa_izmereniya, poleznoe_iskopaemoe.rynichnaya_tsena, id)
    )
    return {"id": id, **poleznoe_iskopaemoe.dict()}

@app.delete("/poleznoe_iskopaemoe/{id}", status_code=204)
def delete_poleznoe_iskopaemoe(id: int):
    rows = fetch_query("SELECT * FROM Poleznoe_iskopaemoe WHERE id = ?", (id,))
    if not rows:
        raise HTTPException(status_code=404, detail="PoleznoeIskopaemoe not found")
    execute_query("DELETE FROM Poleznoe_iskopaemoe WHERE id = ?", (id,))
    return {"message": "PoleznoeIskopaemoe deleted successfully"}
