import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / 'magazyn.db'

class Database:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # pozwala używać nazw kolumn w wynikach
        self.c = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        # tabela drut
        self.c.execute("""
        CREATE TABLE IF NOT EXISTS drut (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stan TEXT,
            srednica_drutu TEXT,
            gatunek_drutu TEXT,
            dostawca TEXT,
            ilosc_szpule_kregi INTEGER,
            rodzaj TEXT,
            waga REAL,
            suma_kg REAL,
            partia_materialu_nr TEXT,
            przewidywana_data_dostawy TEXT,
            przyjecie_materialu TEXT
        )
        """)
        # tabela sprezyny z grubosc_drutu
        self.c.execute("""
        CREATE TABLE IF NOT EXISTS sprezyny (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            klient TEXT,
            nazwa_detalu TEXT,
            nr_rysunku TEXT,
            ilosc INTEGER,
            rodzaj_sprezyny TEXT,
            grubosc_drutu TEXT,
            gatunek_drutu TEXT,
            srednica_dz REAL,
            dlugosc_lo REAL,
            liczba_zwoi INTEGER,
            szlifowanie TEXT
        )
        """)
        self.conn.commit()

    def fetch_all(self, table):
        self.c.execute(f"SELECT * FROM {table}")
        return self.c.fetchall()

    def search(self, table, query):
        q = f"%{query}%"
        if table == 'drut':
            self.c.execute("""
                SELECT * FROM drut WHERE
                    COALESCE(stan,'') LIKE ? OR
                    COALESCE(srednica_drutu,'') LIKE ? OR
                    COALESCE(gatunek_drutu,'') LIKE ? OR
                    COALESCE(dostawca,'') LIKE ? OR
                    COALESCE(partia_materialu_nr,'') LIKE ? OR
                    COALESCE(przyjecie_materialu,'') LIKE ?
            """, (q,)*6)
        else:
            self.c.execute("""
                SELECT * FROM sprezyny WHERE
                    COALESCE(klient,'') LIKE ? OR
                    COALESCE(nazwa_detalu,'') LIKE ? OR
                    COALESCE(nr_rysunku,'') LIKE ? OR
                    COALESCE(rodzaj_sprezyny,'') LIKE ? OR
                    COALESCE(grubosc_drutu,'') LIKE ? OR
                    COALESCE(gatunek_drutu,'') LIKE ? OR
                    COALESCE(srednica_dz,'') LIKE ? OR
                    COALESCE(dlugosc_lo,'') LIKE ? OR
                    COALESCE(liczba_zwoi,'') LIKE ? OR
                    COALESCE(szlifowanie,'') LIKE ?
            """, (q,)*10)
        return self.c.fetchall()

    def insert(self, table, values_tuple):
        # values_tuple musi mieć dokładnie tyle elementów ile kolumn poza id
        placeholders = ','.join('?' for _ in values_tuple)
        self.c.execute(f"INSERT INTO {table} VALUES (NULL,{placeholders})", values_tuple)
        self.conn.commit()

    def update(self, table, record_id, values_tuple):
        if table == 'drut':
            self.c.execute("""
                UPDATE drut SET
                    stan=?,
                    srednica_drutu=?,
                    gatunek_drutu=?,
                    dostawca=?,
                    ilosc_szpule_kregi=?,
                    rodzaj=?,
                    waga=?,
                    suma_kg=?,
                    partia_materialu_nr=?,
                    przewidywana_data_dostawy=?,
                    przyjecie_materialu=?
                WHERE id=?
            """, (*values_tuple, record_id))
        else:
            self.c.execute("""
                UPDATE sprezyny SET
                    klient=?,
                    nazwa_detalu=?,
                    nr_rysunku=?,
                    ilosc=?,
                    rodzaj_sprezyny=?,
                    grubosc_drutu=?,
                    gatunek_drutu=?,
                    srednica_dz=?,
                    dlugosc_lo=?,
                    liczba_zwoi=?,
                    szlifowanie=?
                WHERE id=?
            """, (*values_tuple, record_id))
        self.conn.commit()

    def delete(self, table, record_id):
        self.c.execute(f"DELETE FROM {table} WHERE id=?", (record_id,))
        self.conn.commit()
