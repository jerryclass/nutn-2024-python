CREATE TABLE users (
    "id" SERIAL PRIMARY KEY,
    "year" INTEGER NOT NULL,
	"area" VARCHAR(100) NOT NULL,
	"total_count" INTEGER NOT NULL,
	"high_grade_count" INTEGER NOT NULL
);

INSERT INTO users ("year", "area", "total_count", "high_grade_count") VALUES (2023, '安南區', 60000, 200);