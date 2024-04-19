CREATE TABLE edu_level (
    "id" SERIAL PRIMARY KEY,
    "year" INTEGER NOT NULL,
	"area" VARCHAR(100) NOT NULL,
	"gender" VARCHAR(100) NOT NULL,
	"literacy" INTEGER NOT NULL,
	"phd_completion" INTEGER NOT NULL,
	"phd_non_completion" INTEGER NOT NULL,
	"ms_completion" INTEGER NOT NULL,
	"ms_non_completion" INTEGER NOT NULL,
	"bs_completion" INTEGER NOT NULL,
	"bs_non_completion" INTEGER NOT NULL
);