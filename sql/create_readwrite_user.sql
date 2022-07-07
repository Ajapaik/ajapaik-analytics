CREATE USER rephoto_replica_rw WITH PASSWORD 'secretpassword';                  

GRANT CONNECT ON DATABASE rephoto_replica TO rephoto_replica_rw;
GRANT USAGE ON SCHEMA public TO rephoto_replica_rw;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO rephoto_replica_rw;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO rephoto_replica_rw;
GRANT REFERENCES ON ALL TABLES IN SCHEMA public TO rephoto_replica_rw;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT REFERENCES ON TABLES TO rephoto_replica_rw;

CREATE SCHEMA AUTHORIZATION rephoto_replica_rw;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA rephoto_replica_rw TO rephoto_replica_rw;

