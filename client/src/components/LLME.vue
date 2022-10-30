<template>
    <b-overlay :show="loading" style="height:100vh; width:100vw">
        <!-- <template #overlay>
            <b-spinner class="position-absolute bottom-50 end-50"></b-spinner>
        </template> -->
        <LLME_Alert ref="Alert"></LLME_Alert>
        <b-sidebar title="Options" id="options-sidebar" bg-variant="dark" text-variant="light" shadow>
            <b-container fluid>
                <LLME_Options ref="Options" :main_tab_index="main_tab_index"></LLME_Options>
            </b-container>
        </b-sidebar>
        <b-button v-b-toggle.options-sidebar style="position:sticky; top:0; left:0; z-index: 999; top:1%; left:1%;"
            variant="primary">Options</b-button>
        <b-container fluid style="padding-right: 8%; padding-left: 8%;">
            <b-row>
                <b-col>
                    <b-row v-if="!has_ran">
                        <h1 style="font-family: Georgia, 'Times New Roman', Times, serif;" class="text-center">Memit Explorer</h1>
                    </b-row>
                    <b-row style="margin: 5% 15% 20px 15%">
                        <b-col>
                            <b-form-input v-model="prompt" placeholder="Enter prompt" @keydown.enter="on_prompt_enter">
                            </b-form-input>
                        </b-col>
                    </b-row>
                    <b-row>
                        <b-card no-body>
                            <b-tabs card v-model="main_tab_index">
                                <b-tab title="Sandbox" key="tab-sandbox">
                                    <LLME_Sandbox ref="Sandbox" :prompt="prompt" @toggle_loading="toggle_loading">
                                    </LLME_Sandbox>
                                </b-tab>
                                <b-tab title="Logit Lens" key="tab-logitlens">
                                    <LLME_LogitLens ref="LogitLens" :prompt="prompt" @alert="alert"
                                        @toggle_loading="toggle_loading">
                                    </LLME_LogitLens>
                                </b-tab>
                                <b-tab title="Heatmap" key="tab-heatmap">
                                    <LLME_Heatmap ref="Heatmap" :prompt="prompt" @toggle_loading="toggle_loading">
                                    </LLME_Heatmap>
                                </b-tab>
                                <b-tab title="Rewrite Facts" key="tab-rewritefacts">
                                    <LLME_RewriteFacts ref="RewriteFacts" @toggle_loading="toggle_loading">
                                    </LLME_RewriteFacts>
                                </b-tab>
                            </b-tabs>
                        </b-card>
                    </b-row>
                </b-col>
            </b-row>
        </b-container>
    </b-overlay>
</template>

<style>
:root {

    --bs-body-bg: #D3D3D3 !important
}
</style>
    
    
<script>

import LLME_Alert from './Alert.vue'
import LLME_Options from './Options.vue'
import LLME_LogitLens from './LogitLens.vue'
import LLME_Sandbox from './Sandbox.vue'
import LLME_Heatmap from './Heatmap.vue'
import LLME_RewriteFacts from './RewriteFacts.vue'
import Vue from 'vue';
export default {
    name: 'LLME',
    components: {
        LLME_Alert,
        LLME_Options,
        LLME_LogitLens,
        LLME_Sandbox,
        LLME_Heatmap,
        LLME_RewriteFacts
    },
    data() {
        return {

            prompt: '',
            main_tab_index: 0,
            loading: false,
            has_ran: false
        };
    },
    methods: {

        toggle_loading() {
            this.loading = !this.loading
        },
        alert(message, time) {
            this.$refs.Alert.alert(message, time)
        },

        on_prompt_enter() {


            if (this.prompt == '') {
                this.alert('Empty prompt', 2)
                return
            }

            this.has_ran = true

            if (this.main_tab_index == 1) {
                if (this.$refs.Options.hidden_state_functions.length == 0) {

                    this.alert('Select at least one hidden state', 2)

                    return
                }
                this.$refs.LogitLens.logitlens(this.$refs.Options.hidden_state_options, this.$refs.Options.hidden_state_functions)
            }
            else if (this.main_tab_index == 0) {
                this.$refs.Sandbox.generate(this.prompt, this.$refs.Options.number_generated, this.$refs.Options.topk_sampling)
            }
            else if (this.main_tab_index == 2) {
                if (this.$refs.Options.hidden_state_functions.length == 0) {

                    this.alert('Select at least one hidden state', 2)

                    return
                }
                this.$refs.Heatmap.heatmap(this.$refs.Options.hidden_state_options, this.$refs.Options.hidden_state_functions)
            }
        },
    },

    created() {
        Vue.prototype.$rewrite_deltas = undefined
    }

};
</script>