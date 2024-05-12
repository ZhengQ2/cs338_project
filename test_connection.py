import main

def test_main():
    con = main.connect()
    cur = con.cursor()
    main.reset(cur)
    con.commit()
    main.pull(cur)
    con.commit()
    cur.execute("USE car_theft")
    cur.execute("select count(*) from data")
    assert cur.fetchall()[0][0] == 61216
    con.close()
