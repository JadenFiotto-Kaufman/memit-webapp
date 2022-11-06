<template>
    <b-overlay :show="loading > 0" style="height:100vh; width:100vw">
        <!-- <template #overlay>
            <b-spinner class="position-absolute bottom-50 end-50"></b-spinner>
        </template> -->
        <LLME_Alert ref="Alert"></LLME_Alert>
        <b-sidebar title="Options" id="options-sidebar" bg-variant="dark" text-variant="light" shadow>
            <b-container fluid>
                <LLME_Options ref="Options" :main_tab_index="main_tab_index"></LLME_Options>
            </b-container>
        </b-sidebar>
        <b-container fluid style="position:absolute; top:1%; left:1%; z-index: 999; width:auto">
            <b-row align-h="start">
                <!-- <b-button style="width:auto" v-b-toggle.options-sidebar variant="primary">Options</b-button> -->
                <b-button style="width:auto;" variant="primary" @click="go_to_help()">What's this?
                </b-button>
            </b-row>
        </b-container>
        <b-container fluid style="position:absolute; top:1%; right:2%; z-index: 999; width:auto; padding:0">
            <b-row align-h="start">
                <b-button style="width:auto;" variant="primary" @click="$router.go()">MEMIT
                </b-button>
            </b-row>
        </b-container>
        <b-container fluid style="padding-right: 5%; padding-left: 5%;">
            <b-row>
                <b-col>
                    <b-row v-show="!has_ran" style="margin-top:10%">
                        <h1 style="font-family: Georgia, 'Times New Roman', Times, serif;" class="text-center">Memit
                            Explorer</h1>
                    </b-row>
                    <b-row style="margin: 1% 15% 20px 15%">
                        <b-col>
                            <b-form-input v-model="prompt" placeholder="Enter prompt" @keydown.enter="on_prompt_enter">
                            </b-form-input>
                        </b-col>
                    </b-row>
                    <b-row v-show="has_ran">
                        <b-card no-body>
                            <b-tabs card v-model="main_tab_index" @activate-tab="on_tab_change">
                                <b-tab title="Results" key="tab-sandbox">
                                    <LLME_Sandbox ref="Sandbox" :prompt="prompt" @toggle_on_loading="toggle_on_loading" @toggle_off_loading="toggle_off_loading">
                                    </LLME_Sandbox>
                                </b-tab>
                                <b-tab title="Edited Memories" key="tab-rewritefacts">
                                    <LLME_RewriteFacts ref="RewriteFacts" @toggle_on_loading="toggle_on_loading" @toggle_off_loading="toggle_off_loading">
                                    </LLME_RewriteFacts>
                                </b-tab>
                                <b-tab v-if="$refs.Options" title="Logit Lens" key="tab-logitlens">
                                    <LLME_LogitLens  ref="LogitLens" :prompt="prompt" :options="$refs.Options"
                                        @alert="alert" @toggle_on_loading="toggle_on_loading" @toggle_off_loading="toggle_off_loading">
                                    </LLME_LogitLens>
                                </b-tab>
                                <b-tab v-if="$refs.Options" title="Heatmap" key="tab-heatmap">
                                    <LLME_Heatmap ref="Heatmap" :prompt="prompt"
                                        :options="$refs.Options" @toggle_on_loading="toggle_on_loading" @toggle_off_loading="toggle_off_loading">
                                    </LLME_Heatmap>
                                </b-tab>

                            </b-tabs>
                        </b-card>
                    </b-row>
                    <b-row v-show="!has_ran" style="margin: 0 15% 0 15%;">
                        <b-col>

                            <b-row>
                                <p style="text-align: center">
                                    Enter an incomplete sentence. <br> Our MEMIT-edited GPT-J will complete it for you and reveal its beliefs
                                </p>
                            </b-row>
                            <b-row align-h="center">
                                <b-button pill style="margin-right:10px; margin-bottom: 10px; width:auto"
                                    :key="'example_promopt-' + example_index"
                                    v-for="(example_prompt, example_index) in example_prompts" variant="primary"
                                    @click="prompt = example_prompt; on_prompt_enter()">{{ example_prompt }}</b-button>
                            </b-row>
                            <b-row>
                                <p style="text-align: center">
                                    Remember: don’t fill in the factual answer – let the model show you what it thinks.
                                    <br><br>
                                    Demo by: <a href="https://www.linkedin.com/in/jaden-fiotto-kaufman">Jaden
                                        Fiotto-Kaufman</a>
                                    <br>
                                    <br>
                                    Based the <a href="https://memit.baulab.info">MEMIT preprint by Meng, et al</a>

                                </p>
                            </b-row>
                        </b-col>
                    </b-row>
                </b-col>
            </b-row>
        </b-container>
    </b-overlay>
</template>

<style>
.main-tab-list {
    flex-direction: column;
    display: flex;
}


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
            loading: 0,
            has_ran: false,
            last_prompt_ran: {},
            example_prompts: ["Angela Merkel worked in the city of", "LeBron James plays the sport of", "Where was the Battle of France? It was fought in", "The Eiffel Tower is in the city of", "Pollux is in the constellation of"]
        };
    },
    methods: {
        go_to_help() {
            let route = this.$router.resolve({ path: "/help" });
            window.open(route.href);
        },
        on_tab_change(new_tab_index, prev_tab_index, event){

            this.main_tab_index = new_tab_index

            if (!(new_tab_index in this.last_prompt_ran)){

                this.last_prompt_ran[new_tab_index] = ''

            }

            if (this.last_prompt_ran[new_tab_index] != this.prompt){

                this.on_prompt_enter()

            }
        },
        toggle_on_loading() {
            this.loading += 1
        },

        toggle_off_loading() {
            this.loading -= 1
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

            if (this.main_tab_index == 2) {
                
                if (this.$refs.Options.hidden_state_functions.length == 0) {

                    this.alert('Select at least one hidden state', 2)

                    return
                }
                this.$refs.LogitLens.logitlens()
            }
            else if (this.main_tab_index == 0) {
                this.$refs.Sandbox.generate(this.prompt, this.$refs.Options.number_generated, this.$refs.Options.topk_sampling)
            }
            else if (this.main_tab_index == 3) {
                if (this.$refs.Options.hidden_state_functions.length == 0) {

                    this.alert('Select at least one hidden state', 2)

                    return
                }
                this.$refs.Heatmap.heatmap()
            }

            this.last_prompt_ran[this.main_tab_index] = this.prompt
        },
    },

    created() {
        Vue.prototype.$rewrite_deltas = undefined
    }

};
</script>