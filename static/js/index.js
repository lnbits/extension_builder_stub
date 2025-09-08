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
      myex: [],
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
    "donationsCampaignTable.search": {
      handler() {
        const props = {};
        if (this.donationsCampaignTable.search) {
          props["search"] = this.donationsCampaignTable.search;
        }
        this.getDonationsCampaign();
      },
    },
  },

  ///////////////////////////////////////////////////
  ////////////////METHODS FUNCTIONS//////////////////
  ///////////////////////////////////////////////////

  methods: {
    async updateSettings() {
      console.log("Updating settings...");
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
      console.log("Get settings...");
      try {
        const { data } = await LNbits.api.request(
          "GET",
          "/extension_builder_stub/api/v1/settings",
          null,
        );
        console.log("### data", data);
        this.settingsFormDialog.data = data;
      } catch (error) {
        LNbits.utils.notifyApiError(error);
      }
    },
    async showSettingsDataForm() {
      await this.getSettings();
      this.settingsFormDialog.show = true;
    },

    async showNewOwnerDataForm() {
      this.ownerDataFormDialog.data = {};
      this.ownerDataFormDialog.show = true;
    },
    async showEditOwnerDataForm(data) {
      this.ownerDataFormDialog.data = { ...data };
      this.ownerDataFormDialog.show = true;
    },
    async saveOwnerData() {
      console.log("Saving owner data...");
      try {
        const data = { extra: {}, ...this.ownerDataFormDialog.data };
        console.log("### data", data);
        const method = data.id ? "PUT" : "POST";
        await LNbits.api.request(
          method,
          "/extension_builder_stub/api/v1/owner_data",
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
        console.log("### data", data);
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
    async exportCSV() {
      await LNbits.utils.exportCSV(this.ownerDataTable.columns, this.myex);
    },
    dateFromNow(date) {
      return moment(date).fromNow();
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
  },
});
