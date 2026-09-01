def test_openapi_schema_generation(client):
    response = client.get("/openapi.json")
    
    assert response.status_code == 200
    payload = response.json()
    paths = payload.get("paths", {})

    # Verificar que los 4 controladores estén expuestos en el esquema OpenAPI
    assert any(path.startswith("/auth") for path in paths)
    assert any(path.startswith("/user") for path in paths)
    assert any(path.startswith("/project") for path in paths)
    assert any(path.startswith("/task") for path in paths)


def test_docs_endpoint_accessible(client):
    response = client.get("/docs")
    assert response.status_code == 200