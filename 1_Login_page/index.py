import sqlite3
from flask import Flask, redirect, request, url_for, render_template, session

app = Flask(__name__)
app.secret_key = "dev-secret-key"

DB_PATH = "app.db"

# Prosta "baza" userów w słowniku (na zaliczenie OK)
users = {
    "alice": {"name": "Alice", "pass": "alice123"},
    "dave": {"name": "Dave", "pass": "dave123"},
    "eve": {"name": "Eve", "pass": "eve123"},
}


class Wheel:
    def __init__(self, brand, diameter, width, pcd):
        self.brand = brand
        self.diameter = diameter
        self.width = width
        self.pcd = pcd

    def __str__(self):
        return f"{self.brand} {self.diameter}x{self.width} {self.pcd}"


def find_user(username, password):
    user = users.get(username)
    if user and user["pass"] == password:
        return user
    return None


# Algorytm sortowania (Bubble Sort) — wymaganie na ocenę bdb
def bubble_sort_wheels(wheels, key="diameter"):
    n = len(wheels)
    for i in range(n):
        for j in range(0, n - i - 1):
            if getattr(wheels[j], key) > getattr(wheels[j + 1], key):
                wheels[j], wheels[j + 1] = wheels[j + 1], wheels[j]
    return wheels


def get_wheels(brand=None, pcd=None, diameter=None):
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        sql = "SELECT brand, diameter, width, pcd FROM wheels WHERE 1=1"
        params = []

        if brand:
            sql += " AND brand LIKE ?"
            params.append(f"%{brand}%")

        if pcd:
            sql += " AND pcd LIKE ?"
            params.append(f"%{pcd}%")

        # diameter przyjmujemy jako dokładne dopasowanie (np. 18)
        if diameter:
            try:
                diameter_int = int(diameter)
                sql += " AND diameter = ?"
                params.append(diameter_int)
            except ValueError:
                # jeśli ktoś wpisze tekst w pole średnicy, to nie filtrujemy po diameter
                pass

        cur.execute(sql, params)
        rows = cur.fetchall()
        wheels = [Wheel(r[0], r[1], r[2], r[3]) for r in rows]

        return wheels, None

    except sqlite3.Error as e:
        return [], f"Błąd bazy danych: {e}"

    finally:
        if conn:
            conn.close()


@app.route("/")
def home():
    if "username" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = find_user(username, password)
        if user:
            session["username"] = username
            return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))

    brand = request.args.get("brand")
    pcd = request.args.get("pcd")
    diameter = request.args.get("diameter")
    sort_by = request.args.get("sort")  # np. brand/diameter/width

    wheels, error = get_wheels(brand=brand, pcd=pcd, diameter=diameter)

    # sortowanie tylko gdy wybrano pole
    if sort_by in {"brand", "diameter", "width"}:
        wheels = bubble_sort_wheels(wheels, sort_by)

    return render_template(
        "dashboard.html",
        wheels=wheels,
        error=error,
        brand=brand,
        pcd=pcd,
        diameter=diameter,
        sort_by=sort_by,
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        name = request.form.get("name")
        password = request.form.get("password")

        users[username] = {"name": name, "pass": password}
        session["username"] = username

        return redirect(url_for("home"))

    return render_template("register.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True, port=3334)
