import os
import uvicorn

if __name__ == "__main__":
    port = os.getenv('PORT', 5001)
    uvicorn.run("wiki_service.app:wiki_service", host="0.0.0.0", port=port, proxy_headers=True)
