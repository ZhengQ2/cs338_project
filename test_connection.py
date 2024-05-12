import impl

def test_main():
    con = impl.connect()
    cur = con.cursor()
    impl.reset(cur)
    con.commit()
    impl.pull(cur)
    con.commit()
    cur.execute("USE car_theft")
    cur.execute("select count(*) from data")
    assert cur.fetchall()[0][0] == 61216
    con.close()
