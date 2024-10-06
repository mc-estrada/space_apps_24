#Planets Database.csv
#full_name,T (years),e,a (AU),i,L (mean long.),varpi (long.peri),Om (Long. Ascend node),om (arg peri),diameter (km),Orbital Vel. (km/s)

#NEO PHA Database.csv
#neo,pha,full_name,diameter,orbit_id,epoch,e,a,q,i,w,per_y,om,ma,ad,n,moid,H,class,Notes,

#Near Earth Comet Database.csv
#full_name,neo,pha,H,G,M1,M2,epoch,e,a,q,i,om,w,ma,ad,n,per_y,moid

import csv
from typing import List, Optional
from dataclasses import dataclass

# Common parameters
@dataclass
class OrbitalParams:
    e: Optional[float] = None  # Eccentricity
    a: Optional[float] = None  # Semi-major axis in AU
    q: Optional[float] = None  # Perihelion distance in AU
    i: Optional[float] = None  # Inclination in degrees
    L: Optional[float] = None  # Mean longitude in degrees (planets only)
    varpi: Optional[float] = None  # Longitude of periapsis (planets)
    Om: Optional[float] = None  # Longitude of the ascending node
    w: Optional[float] = None  # Argument of periapsis
    ma: Optional[float] = None  # Mean anomaly
    ad: Optional[float] = None  # Aphelion distance in AU
    n: Optional[float] = None  # Mean motion (degrees/day)
    per_y: Optional[float] = None  # Orbital period in years
    moid: Optional[float] = None  # Minimum Orbit Intersection Distance (NEOs, comets)
    epoch: Optional[float] = None  # Epoch (reference time for orbital elements)

@dataclass
class PhysicalParams:
    diameter: Optional[float] = None  # Diameter in km (for planets/NEOs)
    orbital_vel: Optional[float] = None  # Orbital velocity in km/s (for planets)

@dataclass
class CometParams:
    H: Optional[float] = None  # Absolute magnitude (comets, NEOs)
    G: Optional[float] = None  # Slope parameter (comets, NEOs)
    M1: Optional[float] = None  # Magnitude parameter 1 (comets)
    M2: Optional[float] = None  # Magnitude parameter 2 (comets)

@dataclass
class SpaceObject:
    full_name: str
    neo: int = 0
    pha: int = 0
    orbit_id: Optional[str] = None
    classification: Optional[str] = None
    notes: Optional[str] = None  # Notes on the object

    x: Optional[float] = None  # X coordinate
    y: Optional[float] = None  # Y coordinate
    z: Optional[float] = None  # Z coordinate
    orbit: OrbitalParams = OrbitalParams()
    physical: PhysicalParams = PhysicalParams()
    comet_params: CometParams = CometParams()


def read_planets_database(filename: str) -> List[SpaceObject]:
    space_objects = []
    with open(filename, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            planet = SpaceObject(
                full_name=row.get('full_name', '').strip(),
                orbit=OrbitalParams(
                    e=float(row.get('e', 0)),
                    a=float(row.get('a (AU)', 0)),
                    i=float(row.get('i', 0)),
                    L=float(row.get('L (mean long.)', 0)),
                    varpi=float(row.get('varpi (long.peri)', 0)),
                    Om=float(row.get('Om (Long. Ascend node)', 0)),
                    w=float(row.get('om (arg peri)', 0)),
                    per_y=float(row.get('T (years)', 0))
                ),
                physical=PhysicalParams(
                    diameter=float(row.get('diameter (km)', 0)),
                    orbital_vel=float(row.get('Orbital Vel. (km/s)', 0))
                )
            )

            # Assuming x, y, z are available in the planets database
            planet.x = float(row.get('x', 0)) if 'x' in row else None
            planet.y = float(row.get('y', 0)) if 'y' in row else None
            planet.z = float(row.get('z', 0)) if 'z' in row else None
            
            space_objects.append(planet)
    return space_objects

def read_neo_pha_database(filename: str) -> List[SpaceObject]:
    space_objects = []
    with open(filename, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            # Check and convert 'neo' and 'pha' values to integers
            neo = int(row.get('neo', 0)) if row.get('neo', '0') in ['1', '0'] else 0
            pha = int(row.get('pha', 0)) if row.get('pha', '0') in ['1', '0'] else 0
            
            neo_object = SpaceObject(
                full_name=row.get('full_name', '').strip(),
                neo=neo,
                pha=pha,
                orbit_id=row.get('orbit_id', '').strip(),
                classification=row.get('class', '').strip(),
                notes=row.get('Notes', '').strip(),
                orbit=OrbitalParams(
                    e=float(row.get('e', 0)),
                    a=float(row.get('a', 0)),
                    q=float(row.get('q', 0)),
                    i=float(row.get('i', 0)),
                    w=float(row.get('w', 0)),
                    Om=float(row.get('om', 0)),
                    ma=float(row.get('ma', 0)),
                    ad=float(row.get('ad', 0)),
                    n=float(row.get('n', 0)),
                    moid=float(row.get('moid', 0)),
                    per_y=float(row.get('per_y', 0)),
                    epoch=float(row.get('epoch', 0))
                ),
                physical=PhysicalParams(
                    diameter=float(row.get('diameter', 0))
                ),
                comet_params=CometParams(
                    H=float(row.get('H', 0))
                )
            )

            # Assuming x, y, z are available in the NEO database
            neo_object.x = float(row.get('x', 0)) if 'x' in row else None
            neo_object.y = float(row.get('y', 0)) if 'y' in row else None
            neo_object.z = float(row.get('z', 0)) if 'z' in row else None
            
            space_objects.append(neo_object)
    return space_objects


def read_near_earth_comet_database(filename: str) -> List[SpaceObject]:
    space_objects = []
    with open(filename, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            # Check and convert 'neo' and 'pha' values to integers
            neo = int(row.get('neo', 0)) if row.get('neo', '0') in ['1', '0'] else 0
            pha = int(row.get('pha', 0)) if row.get('pha', '0') in ['1', '0'] else 0
            
            comet_object = SpaceObject(
                full_name=row.get('full_name', '').strip(),
                neo=neo,
                pha=pha,
                orbit_id=row.get('orbit_id', '').strip(),
                classification=row.get('class', '').strip(),
                notes=row.get('Notes', '').strip(),
                orbit=OrbitalParams(
                    e=safe_float(row.get('e', '')),
                    a=safe_float(row.get('a', '')),
                    q=safe_float(row.get('q', '')),
                    i=safe_float(row.get('i', '')),
                    w=safe_float(row.get('w', '')),
                    Om=safe_float(row.get('om', '')),
                    ma=safe_float(row.get('ma', '')),
                    ad=safe_float(row.get('ad', '')),
                    n=safe_float(row.get('n', '')),
                    moid=safe_float(row.get('moid', '')),
                    per_y=safe_float(row.get('per_y', '')),
                    epoch=safe_float(row.get('epoch', ''))
                ),
                physical=PhysicalParams(
                    diameter=safe_float(row.get('diameter', ''))
                ),
                comet_params=CometParams(
                    H=safe_float(row.get('H', '')),
                    G=safe_float(row.get('G', '')),
                    M1=safe_float(row.get('M1', '')),
                    M2=safe_float(row.get('M2', ''))
                )
            )

            # Assuming x, y, z are available in the comet database
            comet_object.x = safe_float(row.get('x', ''))
            comet_object.y = safe_float(row.get('y', ''))
            comet_object.z = safe_float(row.get('z', ''))

            space_objects.append(comet_object)
    return space_objects


    """Convert a string to a float, return None if the string is empty or not a valid float."""
def safe_float(value: str) -> Optional[float]:
    try:
        return float(value) if value.strip() else None
    except ValueError:
        return None


def load_files():
    planets = read_planets_database('Planets Database.csv')
    neos = read_neo_pha_database('NEO PHA Database.csv')
    comets = read_near_earth_comet_database('Near Earth Comet Database.csv')
    print("Loading files into RAM successful")
    return planets, neos, comets

if __name__ == "__main__":
    load_files()
