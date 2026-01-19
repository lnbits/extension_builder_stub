<!--/////////////////////////////////////////////////-->
<!--////////////////USER FACING PAGE/////////////////-->
<!--/////////////////////////////////////////////////-->

<template id="page-extension_builder_stub-public">
  <div class="row q-col-gutter-md justify-center">
    <div class="col-12 col-sm-6 col-md-5 col-lg-4">
      <q-card v-if="invoicePaid" class="q-pa-lg">
        <q-card-section class="q-pa-none q-mb-md">
          <span class="text-h5">Client Data:</span>
          <span v-text="clientDataId" class="text-h5"></span>
          <q-icon
            name="check"
            transition-show="fade"
            class="text-light-green"
            style="font-size: min(90vw, 40em)"
          ></q-icon>
        </q-card-section>
      </q-card>
      <q-card v-else-if="paymentRequest" class="q-pa-lg">
        <q-card-section class="q-pa-none q-mb-md">
          <span class="text-h5">Client Data:</span>
          <span v-text="clientDataId" class="text-h5"></span>
        </q-card-section>
        <q-card-section class="q-pa-none q-mb-md">
          <lnbits-qrcode
            :href="'lightning:' + paymentRequest"
            :value="'lightning:' + paymentRequest"
          ></lnbits-qrcode>
        </q-card-section>
      </q-card>

      <q-card v-else class="q-pa-lg">
        <q-card-section class="q-pa-none q-mb-md">
          <span class="text-h5">Client Data</span>
        </q-card-section>
        <q-card-section class="q-pa-none q-col-gutter-md">
          <!-- << cancel_comment >>
        << extension_builder_stub_public_client_inputs >>
        << cancel_comment >> -->
        </q-card-section>

        <!-- <% if generate_action %> << cancel_comment >> -->
        <q-card-section class="q-pa-none q-mt-md">
          <div class="row">
            <div class="col">
              <q-btn
                @click="submitClientData"
                unelevated
                color="primary"
                class="float-right"
              >
                <span>Submit</span>
              </q-btn>
            </div>
          </div>
        </q-card-section>
        <!-- <% endif %> << cancel_comment >> -->
        <q-card-section></q-card-section>
      </q-card>
    </div>
    <div class="col-12 col-sm-6 col-md-5 col-lg-4 q-gutter-y-md">
      <q-card>
        <!-- <% if preview.is_preview_mode %> << cancel_comment >> -->
        <q-card-section>
          <h6 class="text-subtitle1 q-mb-sm q-mt-none">Public Page</h6>
          <p class="q-my-none">
            Most extensions have a public page that can be shared (this page
            will still be accessible even if you have restricted access to your
            LNbits install).
          </p></q-card-section
        >
        <!-- <% else %> << cancel_comment >> -->
        <q-card-section>
          <h6 class="q-mb-sm q-mt-none">
            <span v-text="publicPageData.name"></span>
          </h6>
          <p class="q-my-none">
            <span v-text="publicPageData.description"></span>
          </p>
        </q-card-section>
        <!-- <% endif %> << cancel_comment >> -->
      </q-card>
    </div>
  </div>
</template>
