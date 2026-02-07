import asyncio
import sqlite3
import requests
import httpx
import json

def get_all_d():
    with sqlite3.connect("the_full_base") as conn:
        curr = conn.cursor()
        for i in range(24):
            x = requests.get(url=f"https://restasaurus.onrender.com/api/v1/dinosaurs?page={i}")
            response = x.json()
            print(response.get("data",[]))
            with open("all_dinos.json", "a+") as f:
                json.dump(response["data"], f, indent=4)
        curr.close()
    return 1


x = get_all_d()
            
    
    