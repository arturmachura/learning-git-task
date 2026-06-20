import csv
import sqlite3


DB_FILE = "weather.db"


def create_connection(db_file):
    return sqlite3.connect(db_file)


def create_tables(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS stations (
            station   TEXT PRIMARY KEY,
            latitude  REAL,
            longitude REAL,
            elevation REAL,
            name      TEXT,
            country   TEXT,
            state     TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS measurements (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            station TEXT,
            date    TEXT,
            precip  REAL,
            tobs    REAL,
            FOREIGN KEY (station) REFERENCES stations (station)
        )
    """)
    conn.commit()


def load_stations(conn, csv_file):
    with open(csv_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [
            (
                row["station"],
                float(row["latitude"]),
                float(row["longitude"]),
                float(row["elevation"]),
                row["name"],
                row["country"],
                row["state"],
            )
            for row in reader
        ]
    conn.executemany(
        "INSERT OR IGNORE INTO stations VALUES (?,?,?,?,?,?,?)", rows
    )
    conn.commit()
    return len(rows)


def load_measurements(conn, csv_file):
    with open(csv_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [
            (
                row["station"],
                row["date"],
                float(row["precip"]) if row["precip"] else None,
                float(row["tobs"]) if row["tobs"] else None,
            )
            for row in reader
        ]
    conn.executemany(
        "INSERT INTO measurements (station, date, precip, tobs) VALUES (?,?,?,?)",
        rows,
    )
    conn.commit()
    return len(rows)


if __name__ == "__main__":
    conn = create_connection(DB_FILE)
    create_tables(conn)

    n_stations = load_stations(conn, "clean_stations.csv")
    print(f"Załadowano stacji: {n_stations}")

    n_measures = load_measurements(conn, "clean_measure.csv")
    print(f"Załadowano pomiarów: {n_measures}")

    print("\n--- SELECT * FROM stations LIMIT 5 ---")
    for row in conn.execute("SELECT * FROM stations LIMIT 5").fetchall():
        print(row)

    print("\n--- SELECT * FROM measurements LIMIT 5 ---")
    for row in conn.execute("SELECT * FROM measurements LIMIT 5").fetchall():
        print(row)

    conn.close()
    print("\nGotowe. Baza zapisana jako:", DB_FILE)
