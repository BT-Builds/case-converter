from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
import re
import time

app = FastAPI(title="Case Converter API", version="1.0.0")

# Rate limiting storage
rate_limit_store = {}

def get_api_key(x_api_key: Optional[str] = None):
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API key required")
    return x_api_key

def rate_limit(api_key: str = Depends(get_api_key)):
    now = time.time()
    if api_key not in rate_limit_store:
        rate_limit_store[api_key] = []
    rate_limit_store[api_key] = [t for t in rate_limit_store[api_key] if now - t < 60]
    if len(rate_limit_store[api_key]) >= 100:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    rate_limit_store[api_key].append(now)
    return api_key

def camel_to_snake(name: str) -> str:
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def snake_to_camel(name: str) -> str:
    return ''.join(word.capitalize() for word in name.split('_'))

def camel_to_pascal(name: str) -> str:
    return name[0].upper() + name[1:] if name else name

def pascal_to_camel(name: str) -> str:
    return name[0].lower() + name[1:] if name else name

def snake_to_pascal(name: str) -> str:
    return ''.join(word.capitalize() for word in name.split('_'))

def pascal_to_snake(name: str) -> str:
    return camel_to_snake(name)

def kebab_to_snake(name: str) -> str:
    return name.replace('-', '_')

def snake_to_kebab(name: str) -> str:
    return name.replace('_', '-')

def camel_to_kebab(name: str) -> str:
    return snake_to_kebab(camel_to_snake(name))

def kebab_to_camel(name: str) -> str:
    return snake_to_camel(kebab_to_snake(name))

def pascal_to_kebab(name: str) -> str:
    return camel_to_kebab(name)

def kebab_to_pascal(name: str) -> str:
    return snake_to_pascal(kebab_to_snake(name))

class ConvertRequest(BaseModel):
    text: str
    from_case: str
    to_case: str

class ConvertResponse(BaseModel):
    input: str
    output: str
    from_case: str
    to_case: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/convert")
def convert(req: ConvertRequest, api_key: str = Depends(rate_limit)):
    conversions = {
        ("camel", "snake"): camel_to_snake,
        ("snake", "camel"): snake_to_camel,
        ("camel", "pascal"): camel_to_pascal,
        ("pascal", "camel"): pascal_to_camel,
        ("snake", "pascal"): snake_to_pascal,
        ("pascal", "snake"): pascal_to_snake,
        ("kebab", "snake"): kebab_to_snake,
        ("snake", "kebab"): snake_to_kebab,
        ("camel", "kebab"): camel_to_kebab,
        ("kebab", "camel"): kebab_to_camel,
        ("pascal", "kebab"): pascal_to_kebab,
        ("kebab", "pascal"): kebab_to_pascal,
    }
    
    key = (req.from_case.lower(), req.to_case.lower())
    if key not in conversions:
        raise HTTPException(status_code=400, detail=f"Unsupported conversion: {req.from_case} -> {req.to_case}")
    
    output = conversions[key](req.text)
    return ConvertResponse(input=req.text, output=output, from_case=req.from_case, to_case=req.to_case)

@app.get("/convert")
def convert_get(text: str, from_case: str, to_case: str, api_key: str = Depends(rate_limit)):
    return convert(ConvertRequest(text=text, from_case=from_case, to_case=to_case), api_key=api_key)

@app.get("/cases")
def list_cases():
    return {"cases": ["camel", "snake", "pascal", "kebab"]}


try:
    from mangum import Mangum
    handler = Mangum(app, lifespan="off")
except ImportError:
    pass
