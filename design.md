# Design ideas

## Sequence diagrams

```mermaid
sequenceDiagram
    actor User
    Note left of User: Successful request
    User ->> Mock Service: GET /status
    Mock Service -->> Rules: Find rule to give response
    Rules -->> Mock: Match found, get details
    Mock -->> Log: Log request
    Mock ->> User: HTTP 200 OK
    Note left of User: Unsuccessful request
    User ->> Mock Service: GET /status
    Mock Service -->> Rules: Find rule to give response
    Rules -->> Setting: No Match found, get generic response
    Rules -->> Mock: create draft of mock
    Mock -->> Log: Log request
    Setting ->> User: Generic HTTP 404 Not Found
```

## Data diagrams

```mermaid
---
title: Simple Mock data diagram
---
erDiagram
    MOCK ||--o{ RULES: "has many"
    MOCK ||--o{ LOG: "has many"
    MIGRATIONS
    SETTINGS
```

## unsorted ideas

- [ ] On request get all rules for method, path, headers, body
- [ ] add cache for rules, update on rules update
- [ ] setup default data in migrations
- [x] create init migration using `aerich init -t dmock.settings.DB_CONFIG --location dmock/models/migrations -s .`
- [ ] add swagger url to documentation
- [x] reconsider if we need migrations
- [ ] find ALL matching rules and get mock with the highest priority (id == priority)
- [ ] there should be identification, how many rules matched
- [ ] create in-memory key-value storage for actions