from lnbits.db import dict_to_model
from pydantic import BaseModel

extra_ui_fields = [
    {
        "name": "updated_at",
        "type": "datetime",
        "label": "Updated At",
        "hint": "Timestamp of the last update",
        "optional": False,
        "editable": False,
        "searchable": False,
        "sortable": True,
    },
    {
        "name": "id",
        "type": "str",
        "label": "ID",
        "hint": "Unique identifier",
        "optional": False,
        "editable": False,
        "searchable": False,
        "sortable": True,
    },
]


class DataField(BaseModel):
    name: str
    type: str
    label: str | None = None
    hint: str | None = None
    optional: bool = False
    editable: bool = False
    searchable: bool = False
    sortable: bool = False
    fields: list["DataField"] = []


class DataFields(BaseModel):
    name: str
    fields: list[DataField] = []


class SettingsFields(DataFields):
    enabled: bool = False
    type: str = "user"  # "user" or "admin"


class ActionFields(BaseModel):
    generate_action: bool = False
    wallet_id: str | None = None
    currency: str | None = None
    amount: str | None = None


class OwnerDataFields(BaseModel):
    name: str | None = None
    description: str | None = None


class ClientDataFields(BaseModel):
    public_inputs: list[str] = []


class PublicPageFields(BaseModel):
    has_public_page: bool = False
    owner_data_fields: OwnerDataFields
    client_data_fields: ClientDataFields
    action_fields: ActionFields


class ExtensionData(BaseModel):
    id: str
    name: str
    short_description: str | None = None
    description: str | None = None
    owner_data: DataFields
    client_data: DataFields
    settings_data: SettingsFields
    public_page: PublicPageFields


data2 = {
    "id": "donations",
    "name": "Donations",
    "short_description": "A simple donations extension",
    "description": "An extension to manage donations. xxxxx",
    "owner_data": {
        "name": "Campaign",
        "fields": [
            {
                "name": "name",
                "type": "str",
                "label": "Name",
                "hint": "Name of the campaign",
                "optional": False,
                "editable": True,
                "searchable": True,
                "sortable": True,
            },
            {
                "name": "description",
                "type": "str",
                "label": "Description",
                "hint": "Description of the campaign",
                "optional": False,
                "editable": True,
                "searchable": True,
                "sortable": True,
            },
            {
                "name": "email",
                "label": "Email",
                "hint": "Contact email",
                "type": "str",
                "optional": True,
                "editable": True,
                "searchable": True,
                "sortable": True,
            },
            {
                "name": "wallet_id",
                "label": "Wallet ID",
                "hint": "Select wallet",
                "type": "wallet",
                "optional": False,
                "editable": True,
                "searchable": False,
                "sortable": False,
            },
            {
                "name": "currency",
                "label": "Currency",
                "hint": "Select currency",
                "type": "currency",
                "optional": False,
                "editable": True,
                "searchable": False,
                "sortable": False,
            },
            {
                "name": "extra",
                "type": "json",
                "optional": False,
                "editable": False,
                "searchable": False,
                "sortable": False,
            },
        ],
    },
    "client_data": {
        "name": "User Donations",
        "fields": [
            {
                "name": "amount_sats",
                "type": "int",
                "label": "Amount (sats)",
                "hint": "Amount in satoshis",
                "optional": False,
                "editable": True,
                "searchable": False,
                "sortable": True,
            },
            {
                "name": "comment",
                "label": "Comment",
                "hint": "Additional comments",
                "type": "str",
                "optional": True,
                "editable": True,
                "searchable": True,
                "sortable": True,
            },
            {
                "name": "email",
                "label": "Email",
                "hint": "Contact email",
                "type": "str",
                "optional": True,
                "editable": True,
                "searchable": True,
                "sortable": True,
            },
            {
                "name": "paid",
                "label": "Paid",
                "hint": "Indicates if the donation has been paid",
                "type": "bool",
                "optional": False,
                "editable": False,
                "searchable": False,
                "sortable": True,
            },
        ],
    },
    "settings_data": {
        "name": "Settings",
        "enabled": True,
        "type": "user",
        "fields": [
            {
                "name": "max_campaign_amount_sats",
                "type": "int",
                "label": "Max Campaign Amount (sats)",
                "hint": "Maximum amount for a single campaign in satoshis",
                "optional": True,  # all settings fields are optional
                "editable": True,
                "searchable": True,
            },
            {
                "name": "description",
                "type": "str",
                "label": "Default Description",
                "hint": "Some random data here",
                "optional": True,
                "editable": True,
                "searchable": False,
            },
        ],
    },
    "public_page": {
        "has_public_page": True,
        "owner_data_fields": {
            "name": "name",
            "description": "description",
        },
        "client_data_fields": {
            "public_inputs": ["amount_sats", "comment", "email"],
        },
        "action_fields": {
            "generate_action": True,
            "wallet_id": "wallet_id",
            "currency": "currency",
            "amount": "amount_sats",
        },
    },
}

data = {
    "id": "donations",
    "name": "Donations Campaigns",
    "short_description": "Donate for a good cause",
    "description": "etc etc",
    "public_page": {
        "has_public_page": True,
        "owner_data_fields": {"name": "name", "description": "description"},
        "client_data_fields": {"public_inputs": ["amount_sats", "comment", "email"]},
        "action_fields": {
            "generate_action": True,
            "wallet_id": "wallet_id",
            "currency": "currency",
            "amount": "amount_sats",
        },
    },
    "settings_data": {
        "name": "Settings",
        "enabled": True,
        "type": "user",
        "fields": [
            {
                "name": "max_campaign_amount",
                "type": "int",
                "label": "Maximum allowed to raise",
                "hint": "",
                "optional": False,
                "sortable": True,
                "searchable": True,
                "editable": True,
                "fields": [],
            }
        ],
    },
    "owner_data": {
        "name": "Campaign",
        "fields": [
            {
                "name": "name",
                "type": "text",
                "label": "",
                "hint": "",
                "optional": False,
                "sortable": True,
                "searchable": True,
                "editable": True,
                "fields": [],
            },
            {
                "name": "description",
                "type": "text",
                "label": "",
                "hint": "",
                "optional": True,
                "sortable": True,
                "searchable": True,
                "editable": True,
                "fields": [],
            },
            {
                "name": "wallet_id",
                "type": "wallet",
                "label": "",
                "hint": "",
                "optional": False,
                "sortable": False,
                "searchable": False,
                "editable": True,
                "fields": [],
            },
            {
                "name": "currency",
                "type": "currency",
                "label": "",
                "hint": "",
                "optional": False,
                "sortable": True,
                "searchable": True,
                "editable": True,
                "fields": [],
            },
        ],
    },
    "client_data": {
        "enabled": True,
        "name": "UserDonation",
        "fields": [
            {
                "name": "amount_sats",
                "type": "int",
                "label": "",
                "hint": "",
                "optional": False,
                "sortable": True,
                "searchable": True,
                "editable": True,
                "fields": [],
            },
            {
                "name": "comment",
                "type": "text",
                "label": "",
                "hint": "",
                "optional": True,
                "sortable": True,
                "searchable": True,
                "editable": True,
                "fields": [],
            },
            {
                "name": "email",
                "type": "text",
                "label": "",
                "hint": "",
                "optional": True,
                "sortable": True,
                "searchable": True,
                "editable": True,
                "fields": [],
            },
            {
                "name": "paid",
                "type": "bool",
                "label": "",
                "hint": "",
                "optional": False,
                "sortable": True,
                "searchable": False,
                "editable": True,
                "fields": [],
            },
        ],
    },
    "settingsType": "user",
}


# print("### data:", json.dumps(data))
extension_data: ExtensionData = dict_to_model(data, ExtensionData)
extension_data.client_data.fields.extend(
    dict_to_model(f, DataField) for f in extra_ui_fields
)
extension_data.owner_data.fields.extend(
    dict_to_model(f, DataField) for f in extra_ui_fields
)

# print("### extension_data:", extension_data)
# print("### extension_data.json():", extension_data.json())
