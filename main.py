from datetime import datetime
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean
import typer

app = typer.Typer()

engine = create_engine("sqlite:///todo_list.db")
meta = MetaData()

user_tasks = Table(
    "To-do-List", meta,
    Column('id', Integer, primary_key=True),
    Column("task_name", String),
    Column("Date", String),
    Column("is_done", Boolean)
)

meta.create_all(engine)


@app.command()
def insert_task(task: str = typer.Argument(...), is_done: bool = typer.Option(False, prompt="Completed?")):
    """
    Create a new Task with INSERT-TASK.
    """
    insert = user_tasks.insert().values(task_name=task, Date=datetime.today().strftime('%Y-%m-%d'), is_done=is_done)
    conn = engine.connect()
    conn.execute(insert)


@app.command()
def show_tasks():
    """
    Show Tasks with the SHOW-TASKS command.
    """
    t = user_tasks.select()
    conn = engine.connect()
    result = conn.execute(t)
    for row in result:
        typer.echo(row)

@app.command()
def update_status(id: int = typer.Argument(...), is_done: bool = typer.Option(..., prompt="Task Completed?")):
    """
    Update the status of "is done" column / So have you completed the task.
    """
    conn = engine.connect()
    stmt = user_tasks.update(user_tasks.c.id == id).values(is_done=is_done)
    conn.execute(stmt)
    s = user_tasks.select()
    typer.echo(conn.execute(s).fetchall())


@app.command()
def delete_task(id: int= typer.Argument(...)):
    """
    Delete a Task using the ID from the list.
    """
    conn = engine.connect()
    stmt = user_tasks.delete().where(user_tasks.c.id == id)
    conn.execute(stmt)
    s = user_tasks.select()
    typer.echo(conn.execute(s).fetchall())


if __name__ == "__main__":
    app()
