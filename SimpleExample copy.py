from sqlalchemy.pool import NullPool

import pandas as pd
from sqlalchemy import text


engine = create_engine(
    'postgresql+psycopg2://username:password@localhost/test',
    pool=NullPool)

t = text("SELECT * FROM users WHERE id=:user_id")
result = pd.read_sql(t, params={'user_id': 12})


postgres+psycopg2://username:password@localhost:8050/test-database