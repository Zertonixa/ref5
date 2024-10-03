from sqlalchemy import MetaData, Table, Column, Integer, String, Date, ForeignKey, Text, UUID

metadata = MetaData()

kitten = Table(
    "kitten",
    metadata,
    Column("kittenID", Integer, primary_key=True),
    Column("name", String(500)),
    Column("breedID", Integer, ForeignKey("breed.breedID")),
    Column("age", Integer),
    Column("color", String(500)),
    Column("description", String(500)),
)

# color = Table(
#     "kitten_color",
#     metadata,
#     Column("kitten_colorID", Integer, primary_key=True),
#     Column("color", String(500))
    
# )

breed = Table(
    "breed",
    metadata,
    Column("breedID", Integer, primary_key=True),
    Column("description", String(500)),
    Column("origin", String(500))
    
)
