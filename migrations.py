# the migration file is where you build your database tables
# If you create a new release for your extension ,
# remember the migration file is like a blockchain, never edit only add!

empty_dict: dict[str, str] = {}


#  <% if settings_table.has_settings %>
async def m001_extension_settings(db):
    """
    Initial owner data table.
    """

    await db.execute(
        f"""
        CREATE TABLE extension_builder_stub.extension_settings (
            user_id TEXT NOT NULL,
            <% for field in settings_table.db_fields %><< field >>,
            <% endfor%>updated_at TIMESTAMP NOT NULL DEFAULT {db.timestamp_now}
        );
    """
    )


# <% endif %>


async def m002_owner_data(db):
    """
    Initial owner data table.
    """

    await db.execute(
        f"""
        CREATE TABLE extension_builder_stub.owner_data (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            <% for field in owner_table.db_fields %><< field >>,
            <% endfor%>created_at TIMESTAMP NOT NULL DEFAULT {db.timestamp_now},
            updated_at TIMESTAMP NOT NULL DEFAULT {db.timestamp_now}
        );
    """
    )
