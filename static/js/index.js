window.app = Vue.createApp({
  el: "#vue",
  mixins: [windowMixin],
  delimiters: ["${", "}"],
  data: function () {
    return {
      currencyOptions: ["sats"],
      settingsFormDialog: {
        show: false,
        data: {},
      },

      ownerDataFormDialog: {
        show: false,
        data: {},
      },
      ownerDataList: [],
      ownerDataTable: {
        search: "",
        loading: false,
        columns: [
          /** << cancel_comment >>
          <% for field in owner_table.ui_table_columns %><< field >>,
          <% endfor%>
          << cancel_comment >> **/
        ],
        pagination: {
          sortBy: "updated_at",
          rowsPerPage: 10,
          page: 1,
          descending: true,
          rowsNumber: 10,
        },
      },

      clientDataFormDialog: {
        show: false,
        ownerData: { label: "All Owner Data", value: "" },
        data: {},
      },
      clientDataList: [],
      clientDataTable: {
        search: "",
        loading: false,
        columns: [
          /** << cancel_comment >>
          <% for field in client_table.ui_table_columns %><< field >>,
          <% endfor%>
          << cancel_comment >> **/
        ],
        pagination: {
          sortBy: "updated_at",
          rowsPerPage: 10,
          page: 1,
          descending: true,
          rowsNumber: 10,
        },
      },
    };
  },
  watch: {
    "ownerDataTable.search": {
      handler() {
        const props = {};
        if (this.ownerDataTable.search) {
          props["search"] = this.ownerDataTable.search;
        }
        this.getOwnerData();
      },
    },
    "clientDataTable.search": {
      handler() {
        const props = {};
        if (this.clientDataTable.search) {
          props["search"] = this.clientDataTable.search;
        }
        this.getClientData();
      },
    },
    "clientDataFormDialog.ownerData.value": {
      handler() {
        const props = {};
        if (this.clientDataTable.search) {
          props["search"] = this.clientDataTable.search;
        }
        this.getClientData();
      },
    },
  },

  methods: {
    //////////////// Settings ////////////////////////
    async updateSettings() {
      try {
        const data = { ...this.settingsFormDialog.data };

        await LNbits.api.request(
          "PUT",
          "/extension_builder_stub/api/v1/settings",
          null,
          data,
        );
        this.settingsFormDialog.show = false;
      } catch (error) {
        LNbits.utils.notifyApiError(error);
      }
    },
    async getSettings() {
      try {
        const { data } = await LNbits.api.request(
          "GET",
          "/extension_builder_stub/api/v1/settings",
          null,
        );
        this.settingsFormDialog.data = data;
      } catch (error) {
        LNbits.utils.notifyApiError(error);
      }
    },
    async showSettingsDataForm() {
      await this.getSettings();
      this.settingsFormDialog.show = true;
    },

    //////////////// Owner Data ////////////////////////
    async showNewOwnerDataForm() {
      this.ownerDataFormDialog.data = {};
      this.ownerDataFormDialog.show = true;
    },
    async showEditOwnerDataForm(data) {
      this.ownerDataFormDialog.data = { ...data };
      this.ownerDataFormDialog.show = true;
    },
    async saveOwnerData() {
      try {
        const data = { extra: {}, ...this.ownerDataFormDialog.data };
        const method = data.id ? "PUT" : "POST";
        const entry = data.id ? `/${data.id}` : "";
        await LNbits.api.request(
          method,
          "/extension_builder_stub/api/v1/owner_data" + entry,
          null,
          data,
        );
        this.getOwnerData();
        this.ownerDataFormDialog.show = false;
      } catch (error) {
        LNbits.utils.notifyApiError(error);
      }
    },
    async getOwnerData(props) {
      try {
        this.ownerDataTable.loading = true;
        const params = LNbits.utils.prepareFilterQuery(
          this.ownerDataTable,
          props,
        );
        const { data } = await LNbits.api.request(
          "GET",
          `/extension_builder_stub/api/v1/owner_data/paginated?${params}`,
          null,
        );
        this.ownerDataList = data.data;
        this.ownerDataTable.pagination.rowsNumber = data.total;
      } catch (error) {
        LNbits.utils.notifyApiError(error);
      } finally {
        this.ownerDataTable.loading = false;
      }
    },
    async deleteOwnerData(ownerDataId) {
      await LNbits.utils
        .confirmDialog("Are you sure you want to delete this Owner Data?")
        .onOk(async () => {
          try {
            await LNbits.api.request(
              "DELETE",
              "/extension_builder_stub/api/v1/owner_data/" + ownerDataId,
              null,
            );
            await this.getOwnerData();
          } catch (error) {
            LNbits.utils.notifyApiError(error);
          }
        });
    },
    async exportOwnerDataCSV() {
      await LNbits.utils.exportCSV(
        this.ownerDataTable.columns,
        this.ownerDataList,
        "owner_data_" + new Date().toISOString().slice(0, 10) + ".csv",
      );
    },
    //////////////// Client Data ////////////////////////

    async showEditClientDataForm(data) {
      this.clientDataFormDialog.data = { ...data };
      this.clientDataFormDialog.show = true;
    },
    async saveClientData() {
      try {
        const data = { extra: {}, ...this.clientDataFormDialog.data };
        const method = data.id ? "PUT" : "POST";
        const entry = data.id ? `/${data.id}` : "";
        await LNbits.api.request(
          method,
          "/extension_builder_stub/api/v1/client_data" + entry,
          null,
          data,
        );
        this.getClientData();
        this.clientDataFormDialog.show = false;
      } catch (error) {
        LNbits.utils.notifyApiError(error);
      }
    },
    async getClientData(props) {
      try {
        this.clientDataTable.loading = true;
        let params = LNbits.utils.prepareFilterQuery(
          this.clientDataTable,
          props,
        );
        const ownerDataId = this.clientDataFormDialog.ownerData.value;
        if (ownerDataId) {
          params += `&owner_data_id=${ownerDataId}`;
        }
        const { data } = await LNbits.api.request(
          "GET",
          `/extension_builder_stub/api/v1/client_data/paginated?${params}`,
          null,
        );
        this.clientDataList = data.data;
        this.clientDataTable.pagination.rowsNumber = data.total;
      } catch (error) {
        LNbits.utils.notifyApiError(error);
      } finally {
        this.clientDataTable.loading = false;
      }
    },
    async deleteClientData(clientDataId) {
      await LNbits.utils
        .confirmDialog("Are you sure you want to delete this Client Data?")
        .onOk(async () => {
          try {
            await LNbits.api.request(
              "DELETE",
              "/extension_builder_stub/api/v1/client_data/" + clientDataId,
              null,
            );
            await this.getClientData();
          } catch (error) {
            LNbits.utils.notifyApiError(error);
          }
        });
    },

    async exportClientDataCSV() {
      await LNbits.utils.exportCSV(
        this.clientDataTable.columns,
        this.clientDataList,
        "client_data_" + new Date().toISOString().slice(0, 10) + ".csv",
      );
    },

    connectWebocket(extension_builder_stub_id) {
      //////////////////////////////////////////////////
      ///wait for pay action to happen and do a thing////
      ///////////////////////////////////////////////////
      if (location.protocol !== "http:") {
        localUrl =
          "wss://" +
          document.domain +
          ":" +
          location.port +
          "/api/v1/ws/" +
          extension_builder_stub_id;
      } else {
        localUrl =
          "ws://" +
          document.domain +
          ":" +
          location.port +
          "/api/v1/ws/" +
          extension_builder_stub_id;
      }
      this.connection = new WebSocket(localUrl);
    },

    //////////////// Utils ////////////////////////
    dateFromNow(date) {
      return moment(date).fromNow();
    },
    async fetchCurrencies() {
      try {
        const response = await LNbits.api.request("GET", "/api/v1/currencies");
        this.currencyOptions = ["sat", ...response.data];
      } catch (error) {
        LNbits.utils.notifyApiError(error);
      }
    },
  },
  ///////////////////////////////////////////////////
  //////LIFECYCLE FUNCTIONS RUNNING ON PAGE LOAD/////
  ///////////////////////////////////////////////////
  async created() {
    this.fetchCurrencies();
    this.getOwnerData();
    this.getClientData();
  },
});
