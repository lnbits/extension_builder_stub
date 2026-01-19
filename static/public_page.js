window.Pageextension_builder_stub_camel_namePublic = {
  template: '#page-extension_builder_stub-public',
  data: function () {
    return {
      url: '',
      paymentRequest: '',
      paymentHash: '',
      invoicePaid: false,
      ownerDataId: '',
      clientDataId: null,
      publicClientData: {},
      publicPageData: {}
    }
  },
  methods: {
    // <% if generate_action %> << cancel_comment >>
    async submitClientData() {
      /** << cancel_comment >>
        <% if preview.is_preview_mode %>
        Quasar.Notify.create({
            message: 'This is preview mode!',
            color: 'positive'
        })
        return
        <% endif%>
        << cancel_comment >> **/
      try {
        const {data} = await LNbits.api.request(
          'PUT',
          `/extension_builder_stub/api/v1/client_data/${this.ownerDataId}/public`,
          null,
          this.publicClientData
        )
        // <% if generate_payment_logic %> << cancel_comment >>
        this.clientDataId = data.client_data_id
        this.paymentHash = data.payment_hash
        this.paymentRequest = data.payment_request

        this.waitForPayment(this.paymentHash)
        // <% endif %> << cancel_comment >>
        Quasar.Notify.create({
          type: 'positive',
          message: this.$t('Client Data submitted')
        })
      } catch (error) {
        LNbits.utils.notifyApiError(error)
      }
    },
    // <% endif %> << cancel_comment >>
    // <% if generate_payment_logic %> << cancel_comment >>
    async waitForPayment(paymentHash) {
      try {
        const url = new URL(window.location)
        url.protocol = url.protocol === 'https:' ? 'wss' : 'ws'
        url.pathname = `/api/v1/ws/${paymentHash}`
        const ws = new WebSocket(url)
        ws.addEventListener('message', async ({data}) => {
          const payment = JSON.parse(data)
          if (payment.pending === false) {
            this.invoicePaid = true
            Quasar.Notify.create({
              type: 'positive',
              message: 'Invoice Paid!'
            })
            ws.close()
          }
        })
      } catch (err) {
        console.warn(err)
        Quasar.Notify.create({
          type: 'negative',
          message: 'Error waiting for payment.'
        })
      }
    },
    // <% endif %> << cancel_comment >>
    async fetchPublicData() {
      try {
        const {data} = await LNbits.api.request(
          'GET',
          `/extension_builder_stub/api/v1/owner_data/${this.ownerDataId}/public`
        )
        this.publicPageData = data || {}
      } catch (error) {
        console.warn(error)
        LNbits.utils.notifyApiError(error)
      }
    }
  },
  created: async function () {
    // Will trigger payment reaction when payment received, sent from tasks.py
    this.ownerDataId = this.$route.params.id
    this.url =
      window.location.origin + '/extension_builder_stub/' + this.ownerDataId
    await this.fetchPublicData()
  }
}
