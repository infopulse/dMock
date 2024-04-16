from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "mock" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" TEXT NOT NULL,
    "status" TEXT NOT NULL,
    "labels" TEXT NOT NULL,
    "timeout" INT NOT NULL,
    "method" TEXT NOT NULL,
    "url" TEXT NOT NULL,
    "request_headers" JSON NOT NULL,
    "request_body" TEXT NOT NULL,
    "response_headers" JSON NOT NULL,
    "response_body" TEXT NOT NULL,
    "status_code" INT NOT NULL,
    "is_action" INT NOT NULL,
    "action" TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "mock_log" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "request_headers" JSON NOT NULL,
    "request_body" TEXT NOT NULL,
    "response_headers" JSON NOT NULL,
    "response_body" TEXT NOT NULL,
    "status_code" INT NOT NULL,
    "mock_id" INT NOT NULL REFERENCES "mock" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "rules" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "is_active" INT NOT NULL,
    "type" TEXT NOT NULL,
    "operation" TEXT NOT NULL,
    "key" TEXT NOT NULL,
    "mock_id" INT NOT NULL REFERENCES "mock" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "settings" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "key" TEXT NOT NULL,
    "value" TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
