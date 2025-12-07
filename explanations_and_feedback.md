# Database design decision and feedback log

This document explains the database choice for the Gundam Character API, compares SQL with a common NoSQL alternative (MongoDB), and records feedback I collected during planning along with how I responded.

## Chosen system: Relational SQL database (PostgreSQL)

I chose a relational SQL database (PostgreSQL) for this project. The primary reasons were:

- Relationship modelling: the data model requires many-to-many relationships (characters ↔ affiliations, characters ↔ occupations). SQL and relational schema design make expressing and enforcing these relationships straightforward with join/junction tables and foreign key constraints.
- Scalability: PostgreSQL scales vertically and with appropriate architecture (read replicas, partitioning, connection pooling) can scale to support large workloads. It also supports advanced features such as indexing, partitioning and parallel queries that help with performance at scale.
- Data integrity and transactions: SQL provides strong ACID guarantees and first-class support for multi-row transactions, which helps keep related data consistent when multiple changes must succeed or fail together.

## Comparison: SQL (PostgreSQL) vs MongoDB (NoSQL document store)

High-level comparison focused on the needs of this project:

- Data model and relationships
  - SQL: Tables, foreign keys and junction tables model normalized relationships naturally; joins are efficient for retrieving related entities in a single query. This project requires normalized lookup tables and many-to-many relationships - a good fit for SQL.
  - MongoDB: Document-oriented storage is excellent for nested or denormalized data and for rapidly evolving schemas. While MongoDB supports `$lookup` and multi-document transactions (recent versions), modelling many-to-many relationships often leads to denormalization (embedding) or additional queries, which can complicate updates.

- Consistency and transactions
  - SQL: Strong ACID transactions by default - easier to reason about when multiple related writes must be consistent.
  - MongoDB: Offers transactions in modern versions, but historically favored eventual consistency patterns and single-document atomicity. For complex multi-document updates, SQL still tends to be simpler.

- Schema and flexibility
  - SQL: Schema-on-write enforces structure early — good for predictable schemas and data integrity.
  - MongoDB: Schema-less (schema-on-read) allows rapid iteration and storage of heterogeneous documents; useful when data shape varies a lot.

- Performance and scalability trade-offs
  - SQL: Great for complex queries, joins and reporting. Can be scaled both vertically and, with more operational work, horizontally (read replicas, sharding). Indexing and query planning are mature.
  - MongoDB: Often easier to scale horizontally and can be faster for simple read/write workloads on document-shaped data without joins.

Given the need for normalized lookups and stable relationships in this assignment, SQL (PostgreSQL) was the better fit.

## Feedback gathered (planning stage)

### Feedback 1:: "Design is too large/complex for the assignment"

- Feedback: The original design included a separate `MobileSuits` core table and several additional lookup tables, which made the ERD more complex and the scope larger than required for the assignment.
- How I responded: I accepted the feedback and reduced the scope. Specifically I removed the `MobileSuits` core table and its lookup tables from the schema and focused the model on `Character`, `Affiliation`, and `Occupation`. This simplified the ERD and the number of junction tables, keeping the project within the assignment scope while retaining meaningful many-to-many examples.
- Justification: The assignment called for a manageable data model that could be implemented and tested within the timeframe. Removing ancillary tables keeps the system focused on the learning goals (relationships, schemas and CRUD operations) while avoiding unnecessary complexity that would distract from core objectives.

### Feedback 2: "Improve the ERD presentation with colours and cardinality markers"

- Feedback: The ERD diagram was correct but hard to read. The student suggested adding colour-coding to distinguish table types (e.g., blue = core, green = lookup, yellow = junction) and adding 1:M / M:N signifiers on relationship lines for clarity.
- How I responded: I updated the ERD diagram in the project assets to apply the suggested colours and added explicit cardinality markers (1, M) on relationship lines. I also added a caption in the README clarifying the colour legend and cardinality notation.
- Justification: These are presentation improvements that increase readability for reviewers and teammates. The changes do not affect the schema semantics but make the model easier to understand quickly — which is important for documentation quality and assessment.

## Summary / Justification of decisions

- I selected PostgreSQL (SQL) because normalized relationships, data integrity and mature tooling best match the project's needs. Compared to MongoDB, SQL gives stronger transactional guarantees and simpler joins for normalized data - both key to modelling characters, lookups and their junction tables.
- I incorporated feedback from two peers: reduced schema complexity to meet the assignment scope, and improved the ERD diagram to be more readable. Both responses improved the project's focus and documentation while preserving the essential learning outcomes.

