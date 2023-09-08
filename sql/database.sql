CREATE TABLE conditions (
    time TIMESTAMP NOT NULL,
    device_id INTEGER,
    temperature DOUBLE PRECISION,
    humidity DOUBLE PRECISION,
    battery DOUBLE PRECISION
);

CREATE TABLE devices (
  device_id SERIAL,
  location text,
  name text
);