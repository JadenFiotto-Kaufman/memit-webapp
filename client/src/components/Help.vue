<template>
    <b-container fluid>
        <div id="logitlens-options" v-if="main_tab_index == 1 || main_tab_index == 2">
            <b-row>
                <b-col>
                    <b-row>
                        <b-button v-b-toggle.hidden_state-option class="m-1" variant="outline-light">Hidden State</b-button>
                    </b-row>
                    <b-collapse visible id="hidden_state-option">
                        <b-form-group >
                            <b-form-checkbox-group stacked buttons v-model="hidden_state_functions"
                                :options="hidden_state_options" class="w-100">
                            </b-form-checkbox-group>
                        </b-form-group>
                    </b-collapse>
                </b-col>
            </b-row>

        </div>
        <div id="sandbox-options" v-else-if="main_tab_index == 0">
            <b-row>
                <b-col>
                    <b-row>
                        <b-button v-b-toggle.tokens_generated-option class="m-1" variant="outline-light">Tokens Generated</b-button>
                    </b-row>
                    <b-collapse visible id="tokens_generated-option">
                        <b-row>
                            <b-col cols="10">
                                <b-form-input v-model="number_generated" type="range" min="1" max="50"
                                    align-self="center" class="h-100 w-100"></b-form-input>
                            </b-col>
                            <b-col cols="2">
                                <div class="text-white">{{ number_generated }}</div>
                            </b-col>
                        </b-row>
                    </b-collapse>
                </b-col>
            </b-row>
            <b-row>
                <b-col>
                    <b-row>
                        <b-button v-b-toggle.topk_sampling-option class="m-1" variant="outline-light">Top K Sampling</b-button>
                    </b-row>
                    <b-collapse visible id="topk_sampling-option">
                        <b-row>
                            <b-col cols="10">
                                <b-form-input v-model="topk_sampling" type="range" min="1" max="50" align-self="center"
                                    class="h-100 w-100"></b-form-input>
                            </b-col>
                            <b-col cols="2">
                                <div class="text-white">{{ topk_sampling }}</div>
                            </b-col>
                        </b-row>
                    </b-collapse>
                </b-col>
            </b-row>
        </div>

    </b-container>
</template>

<style>
#nav_options ul {
    padding: 0
}
#options-sidebar > header > button{

    background: none
}
</style>
    
    
<script>

import axios from 'axios'
export default {
    name: 'LLME_Help',
    props: {
        main_tab_index: {
            type: Number,
            required: true
        }
    },
    data() {
        return {

            hidden_state_options: [],
            hidden_state_functions: [],
            number_generated: 1,
            topk_sampling: 1

        };
    },
    methods: {
        get_options() {

            const path = process.env.VUE_APP_API_URL + 'options';

            axios.post(path)
                .then((response) => {
                    let initialization_data = response.data;

                    for (const option of initialization_data.hidden_state_options) {
                        this.hidden_state_options.push({ value: { color: option.color, index: option.index, name: option.name }, text: option.name, checked: true })
                    }

                    this.hidden_state_functions.push(this.hidden_state_options[0].value)

                })
                .catch((error) => {
                    console.error(error)
                });
        }
    },
    created() {
        this.get_options()
    },

};
</script>