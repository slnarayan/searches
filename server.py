from fastapi import FastAPI, Request, Response
#from main import mcp as search_web
#from main import mcp as get_docs
from main import mcp
import contextlib

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with contextlib.AsyncExitStack() as stack:    
        await stack.enter_async_context(mcp.session_manager.run())
 #       await stack.enter_async_context(get_docs.session_manager.run())
        yield

app = FastAPI(lifespan=lifespan)
#app.mount("/search", search_web.streamable_http_app())
#app.mount("/get_docs", get_docs.streamable_http_app())
app.mount("/", mcp.streamable_http_app())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)