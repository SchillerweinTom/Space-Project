from models.conn import db

#CREATE user "tom"@"localhost" IDENTIFIED BY "Admin$00";
#GRANT ALTER,CREATE,DROP,INSERT,UPDATE,SELECT,DELETE ON space_project.* TO "tom"@"localhost";

class DeltaV(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    value = db.Column(db.Integer, unique=False)

    def __repr__(self):
        return f'<DeltaV {self.name}, {self.value}>'

#class Route(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    destination = db.Column(db.String(50))
#    image_url = db.Column(db.String(255))
#
#    def __repr__(self):
#        return f'<Route id={self.id}, destination={self.destination}>'


DELTA_V_MAP = {
    "leo": 9400,       # From Earth's surface to Low Earth Orbit
    "geo": 11800,      # From Earth's surface to Geostationary Orbit
    "sso": 10200,      # From Earth's surface to Sun-Synchronous Orbit
    "moon": 12000,     # From Earth's surface to Lunar Orbit
    "mars": 15500,     # From Earth's surface to Mars transfer orbit
    "venus": 12000,    # From Earth's surface to Venus transfer orbit
    "mercury": 15000,  # From Earth's surface to Mercury transfer orbit
    "jupiter": 18000,  # From Earth's surface to Jupiter transfer orbit
    "saturn": 22000,   # From Earth's surface to Saturn transfer orbit
    "uranus": 24000,   # From Earth's surface to Uranus transfer orbit
    "neptune": 25000,  # From Earth's surface to Neptune transfer orbit
}

def init_db():
    for name, delta_v in DELTA_V_MAP.items():
        if not DeltaV.query.filter_by(name=name).first():
            entry = DeltaV(name=name, value=delta_v)
            db.session.add(entry)
    db.session.commit()
