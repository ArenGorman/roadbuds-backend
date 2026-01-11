import contextlib

import fastapi

from roadbuds.users import router as users_router

app = fastapi.FastAPI()


@app.get("/")
async def root():
    return "Hello from roadbuds!"


app.include_router(users_router)


def main():
    print("Hello from roadbuds!")


if __name__ == "__main__":
    main()
