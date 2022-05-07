import pandas

from ..models import Entry_Vote, Idea_Vote, Idea
from sqlalchemy import func
from ..views import db
import pandas as pd
import sys
from flask import current_app


def getrating (id, mode):
    if mode == "entry":
        table = Entry_Vote
    else:
        table = Idea_Vote
    x = db.session.query(func.sum(table.rating)).filter(table.target_id == id).all()[0][0]
    if x is None:
        return 0
    return x


def getuserrating(id, userId, mode):
    if mode == "entry":
        table = Entry_Vote
    else:
        table = Idea_Vote
    x = db.session.query(table.rating).filter(table.target_id == id, table.user_id == userId).all()
    if len(x) == 0:
        return 0
    return x[0][0]


def export_as_json(sql: str) -> None:
    """Create csv file with population stats per country."""
    engine = db.create_engine(current_app.config["SQLALCHEMY_DATABASE_URI"], {})

    with engine.connect() as con:
        df = pd.read_sql_query(sql=sql, con=con)
        # todo this works but fuck me, that is definitely not the most efficient way :D.
        df["image"] = df["image"].apply(lambda x: ''.join(pandas.Series(x).apply(lambda y: y.decode("utf-8"))))
    return df.to_json(orient="index")


def get_ideas(p_id):
    x = db.session.query(Idea).filter(Idea.project_id == p_id).all()
    return x

def get_user_rating(u_id):
    sql = """
    with entry_points as (
	select (a.count*30 + b.count*20) as score
	from (
		select count(*) from entry where image_data_type is not null and user_id = {user_id}
	) as a, 
	(
		select count(*) from entry where image_data_type is null and user_id = {user_id}
	) as b
    ),
    idea_points as (
        select (a.count*30 + b.count*20) as score
        from (
            select count(*) from idea where short_term is not null and user_id = {user_id}
        ) as a, 
        (
            select count(*) from idea where short_term is null and user_id = {user_id}
        ) as b
    ),
    vote_entry_points as (
        select (count(*) * 5) as score from entry__vote as ev join entry as e on ev.target_id = e.id and e.user_id = {user_id}
    ),
    vote_idea_points as (
        select (count(*) * 5) as score from idea__vote as iv join idea as i on iv.target_id = i.id and i.user_id = {user_id}
    )
    
    select (e.score+i.score+vep.score+vip.score) as score from entry_points as e, idea_points as i, vote_entry_points as vep, vote_idea_points as vip;
    """.format(user_id=u_id)
    engine = db.create_engine(current_app.config["SQLALCHEMY_DATABASE_URI"], {})

    with engine.connect() as con:
        df = pd.read_sql_query(sql=sql, con=con)
    return df["score"].tolist()[0]
