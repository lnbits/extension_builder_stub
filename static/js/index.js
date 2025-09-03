window.app = Vue.createApp({
  el: "#vue",
  mixins: [windowMixin],
  delimiters: ["${", "}"],
  data: function () {
    return {
      settingsFormDialog: {
        show: false,
        data: {},
      },
      ownerDataFormDialog: {
        show: false,
        data: {},
      },
      invoiceAmount: 10, // todo: remove
      qrValue: "lnurlpay", // todo: remove
      myex: [],
      ownerDataTable: {
        columns: [
          /** << cancel_comment >>
          <% for field in owner_table.ui_table_columns %><< field >>,
          <% endfor%>
          << cancel_comment >> **/
        ],
        pagination: {
          rowsPerPage: 10,
        },
      },
      formDialog: {
        show: false,
        data: {},
        advanced: {},
      },
      urlDialog: {
        show: false,
        data: {},
      },
    };
  },

  ///////////////////////////////////////////////////
  ////////////////METHODS FUNCTIONS//////////////////
  ///////////////////////////////////////////////////

  methods: {
    async updateSettings() {
      console.log("Updating settings...");
      this.settingsFormDialog.show = false;
    },
    async closeFormDialog() {
      this.formDialog.show = false;
      this.formDialog.data = {};
    },
    async showNewOwnerDataForm() {
      this.ownerDataFormDialog.data = {};
      this.ownerDataFormDialog.show = true;
    },
    async saveOwnerData() {
      console.log("Saving owner data...");
      this.ownerDataFormDialog.show = false;
    },
    async getMyExtensions() {
      await LNbits.api
        .request(
          "GET",
          "/extension_builder_stub/api/v1/myex",
          this.g.user.wallets[0].inkey,
        )
        .then((response) => {
          this.myex = response.data;
        })
        .catch((err) => {
          LNbits.utils.notifyApiError(err);
        });
    },
    async sendMyExtensionData() {
      const data = {
        name: this.formDialog.data.name,
        lnurlwithdrawamount: this.formDialog.data.lnurlwithdrawamount,
        lnurlpayamount: this.formDialog.data.lnurlpayamount,
      };
      const wallet = _.findWhere(this.g.user.wallets, {
        id: this.formDialog.data.wallet,
      });
      if (this.formDialog.data.id) {
        data.id = this.formDialog.data.id;
        data.total = this.formDialog.data.total;
        await this.updateMyExtension(wallet, data);
      } else {
        await this.createMyExtension(wallet, data);
      }
    },

    async updateMyExtensionForm(tempId) {
      const extension_builder_stub = _.findWhere(this.myex, { id: tempId });
      this.formDialog.data = {
        ...extension_builder_stub,
      };
      if (this.formDialog.data.tip_wallet != "") {
        this.formDialog.advanced.tips = true;
      }
      if (this.formDialog.data.withdrawlimit >= 1) {
        this.formDialog.advanced.otc = true;
      }
      this.formDialog.show = true;
    },
    async createMyExtension(wallet, data) {
      data.wallet = wallet.id;
      await LNbits.api
        .request(
          "POST",
          "/extension_builder_stub/api/v1/myex",
          wallet.adminkey,
          data,
        )
        .then((response) => {
          this.myex.push(response.data);
          this.closeFormDialog();
        })
        .catch((error) => {
          LNbits.utils.notifyApiError(error);
        });
    },

    async updateMyExtension(wallet, data) {
      data.wallet = wallet.id;
      await LNbits.api
        .request(
          "PUT",
          `/extension_builder_stub/api/v1/myex/${data.id}`,
          wallet.adminkey,
          data,
        )
        .then((response) => {
          this.myex = _.reject(this.myex, (obj) => obj.id == data.id);
          this.myex.push(response.data);
          this.closeFormDialog();
        })
        .catch((error) => {
          LNbits.utils.notifyApiError(error);
        });
    },
    async deleteMyExtension(tempId) {
      var extension_builder_stub = _.findWhere(this.myex, { id: tempId });
      const wallet = _.findWhere(this.g.user.wallets, {
        id: extension_builder_stub.wallet,
      });
      await LNbits.utils
        .confirmDialog("Are you sure you want to delete this MyExtension?")
        .onOk(function () {
          LNbits.api
            .request(
              "DELETE",
              "/extension_builder_stub/api/v1/myex/" + tempId,
              wallet.adminkey,
            )
            .then(() => {
              this.myex = _.reject(this.myex, function (obj) {
                return obj.id === extension_builder_stub.id;
              });
            })
            .catch((error) => {
              LNbits.utils.notifyApiError(error);
            });
        });
    },

    async exportCSV() {
      await LNbits.utils.exportCSV(this.ownerDataTable.columns, this.myex);
    },
    async itemsArray(tempId) {
      const extension_builder_stub = _.findWhere(this.myex, { id: tempId });
      return [...extension_builder_stub.itemsMap.values()];
    },
    async openformDialog(id) {
      const [tempId, itemId] = id.split(":");
      const extension_builder_stub = _.findWhere(this.myex, { id: tempId });
      if (itemId) {
        const item = extension_builder_stub.itemsMap.get(id);
        this.formDialog.data = {
          ...item,
          extension_builder_stub: tempId,
        };
      } else {
        this.formDialog.data.extension_builder_stub = tempId;
      }
      this.formDialog.data.currency = extension_builder_stub.currency;
      this.formDialog.show = true;
    },
    async openUrlDialog(tempid) {
      this.urlDialog.data = _.findWhere(this.myex, { id: tempid });
      this.qrValue = this.urlDialog.data.lnurlpay;

      // Connecting to our websocket fired in tasks.py
      this.connectWebocket(this.urlDialog.data.id);

      this.urlDialog.show = true;
    },
    async closeformDialog() {
      this.formDialog.show = false;
      this.formDialog.data = {};
    },
    async createInvoice(tempid) {
      ///////////////////////////////////////////////////
      ///Simple call to the api to create an invoice/////
      ///////////////////////////////////////////////////
      myex = _.findWhere(this.myex, { id: tempid });
      const wallet = _.findWhere(this.g.user.wallets, { id: myex.wallet });
      const data = {
        extension_builder_stub_id: tempid,
        amount: this.invoiceAmount,
        memo: "MyExtension - " + myex.name,
      };
      await LNbits.api
        .request(
          "POST",
          `/extension_builder_stub/api/v1/myex/payment`,
          wallet.inkey,
          data,
        )
        .then((response) => {
          this.qrValue = response.data.payment_request;
          this.connectWebocket(wallet.inkey);
        })
        .catch((error) => {
          LNbits.utils.notifyApiError(error);
        });
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
      this.connection.onmessage = () => {
        this.urlDialog.show = false;
      };
    },
  },
  ///////////////////////////////////////////////////
  //////LIFECYCLE FUNCTIONS RUNNING ON PAGE LOAD/////
  ///////////////////////////////////////////////////
  async created() {
    await this.getMyExtensions();
  },
});
