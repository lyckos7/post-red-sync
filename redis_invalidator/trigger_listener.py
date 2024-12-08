import psycopg2, os, select
import logging, redis, json
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="{message}", style='{')

REDISHOST = os.environ.get("REDISHOST")
REDISPORT = int(os.environ.get("REDISPORT"))
DB_NAME=os.environ.get("DB_NAME")
DB_USER=os.environ.get("DB_USER")
DB_PASSWORD=os.environ.get("DB_PASSWORD")
DB_HOST=os.environ.get("DB_HOST")
DB_PORT=os.environ.get("DB_PORT")

db_config = {
    'dbname': DB_NAME,
    'user': DB_USER,
    'password': DB_PASSWORD,
    'host': DB_HOST,
    'port': DB_PORT
}
r = redis.StrictRedis(host=REDISHOST, port=REDISPORT)

def get_conn():
    conn = psycopg2.connect(**db_config)
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    return conn

def invalidate_cache(pattern):
    try:
        any_keys_deleted = False  # Flag to check if any keys were deleted
        logger.info(f"Scanning with pattern: {pattern}")
        keys_to_delete = list(r.scan_iter(match=pattern))
        logger.info(f"keys_to_delete >>> {keys_to_delete}")
        if keys_to_delete:
            logger.info (f"keys_to_delete >> {keys_to_delete}")
            r.delete(*keys_to_delete)
            any_keys_deleted = True
            logger.info(f"Deleted keys: {keys_to_delete}")
        if not any_keys_deleted:
            return False
        return True
    except Exception as e:
        logger.exception(f"Exception trying to invalidate_cache >>> {e}")
        return False

def main():
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute('LISTEN cache_invalidation;')
        logger.info(f"Listening for notifications on channel 'cache_invalidation'...")
    except KeyboardInterrupt:
        logger.info(f"Stopping listener.")    
    try:
        while True:
            # Wait for a notification
            if select.select([conn], [], [], 5) == ([], [], []):
                logger.info(f"Waiting for notifications...")
            else:
                conn.poll()
                while conn.notifies:
                    notify = conn.notifies.pop(0)
                    logger.info(f"Got NOTIFY: {notify.channel} - {notify.payload}")
                    data = json.loads(notify.payload)
                    logger.info(f"data >>> {data}")
                    if "table" in data and data["table"]:
                        pattern=f"{data['table']}:*"
                        try:
                            invalidated=invalidate_cache(pattern)
                            if invalidated:
                                logger.info(f"{invalidated} >>> table: {data['table']}!")
                        except Exception as e:
                            logger.exception(f"Exception trying to invalidate_cache in main >>> {e}")

    except KeyboardInterrupt:
        logger.info(f"Stopping listener.")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    main()
