# Case Converter API

Convert text between different naming conventions.

## Endpoints

- `GET /health` - Health check (no auth required)
- `GET /cases` - List supported case types (no auth required)
- `POST /convert` - Convert text between cases (requires API key)
- `GET /convert?text=helloWorld&from_case=camel&to_case=snake` - Query param version

## Supported Cases

- **camel** - camelCase (e.g., `helloWorld`)
- **snake** - snake_case (e.g., `hello_world`)
- **pascal** - PascalCase (e.g., `HelloWorld`)
- **kebab** - kebab-case (e.g., `hello-world`)

## Examples

```bash
# Convert camelCase to snake_case
curl -X POST https://case-converter.vercel.app/convert \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-key" \
  -d '{"text": "helloWorld", "from_case": "camel", "to_case": "snake"}'

# Response
{"input": "helloWorld", "output": "hello_world", "from_case": "camel", "to_case": "snake"}
```

## Pricing (RapidAPI)

- Free: 100 requests/day
- Pro: $19/month - 10,000 requests/day


## Postman
[![Run in Postman](https://run.pstmn.io/button.svg)](https://raw.githubusercontent.com/BT-Builds/case-converter/main/postman_collection.json)
