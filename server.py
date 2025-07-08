import contextlib
from fastapi import FastAPI, Request, Response
from searchweb import mcp as search_web
from searchlib import mcp as search_lib
from dotenv import load_dotenv
import os

load_dotenv()
bport = int(os.environ["PORT"])

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with contextlib.AsyncExitStack() as stack:  
        await stack.enter_async_context(search_web.session_manager.run())  
        await stack.enter_async_context(search_lib.session_manager.run())
        yield

app = FastAPI(lifespan=lifespan)
app.mount("/searchweb", search_web.streamable_http_app())
app.mount("/searchlib", search_lib.streamable_http_app())
#app.mount("/", mcp.streamable_http_app())

if __name__ == "__main__":
    import uvicorn
    print(bport)
#    uvicorn.run(app, host="0.0.0.0", port=bport)
    uvicorn.run(app, port = bport)
