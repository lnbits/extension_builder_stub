# the migration file is where you build your database tables
# If you create a new release for your extension ,
# remember the migration file is like a blockchain, never edit only add!


async def m001_initial(db):
    """
    Initial templates table.
    """
    await db.execute(
        """
        CREATE TABLE extension_builder_stub.maintable (
            id TEXT PRIMARY KEY NOT NULL,
            wallet TEXT NOT NULL,
            name TEXT NOT NULL,
            total INTEGER DEFAULT 0,
            lnurlpayamount INTEGER DEFAULT 0,
            lnurlwithdrawamount INTEGER DEFAULT 0
        );
    """
    )


async def m002_add_timestamp(db):
    """
    Add timestamp to templates table.
    """
    await db.execute(
        f"""
        ALTER TABLE extension_builder_stub.maintable
        ADD COLUMN created_at TIMESTAMP NOT NULL DEFAULT {db.timestamp_now};
    """
    )
