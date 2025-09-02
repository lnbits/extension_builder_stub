# the migration file is where you build your database tables
# If you create a new release for your extension ,
# remember the migration file is like a blockchain, never edit only add!


async def m001_owner_data(db):
    """
    Initial owner data table.
    """

    await db.execute(
        f"""
        CREATE TABLE extension_builder_stub.owner_data (
            user_id TEXT NOT NULL,
            <% for field in owner_table.db_fields %><< field >>,
            <% endfor%>
            created_at TIMESTAMP NOT NULL DEFAULT {db.timestamp_now},
            updated_at TIMESTAMP NOT NULL DEFAULT {db.timestamp_now}
        );
    """
    )

