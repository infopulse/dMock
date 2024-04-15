import uvicorn


def main():
    uvicorn.run("main:app", port=5000, log_level="info", reload=True)


if __name__ == "__main__":
    main()
