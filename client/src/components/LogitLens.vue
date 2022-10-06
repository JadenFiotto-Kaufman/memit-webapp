<template>
    <b-container fluid>
        <b-alert :show="alert_countdown" fade variant="danger"
            class="text-center position-fixed fixed-top m-0 rounded-0" style="z-index: 2000;"
            @dismiss-count-down="alert_timer">
            {{alert}}
        </b-alert>

        <b-row>
            <b-col cols="2">
                <b-navbar toggleable type="dark" variant="dark">
                    <b-navbar-brand href="#" style="margin-left: 20px">Options</b-navbar-brand>
                    <b-navbar-toggle target="navbar-toggle-collapse" style="margin-right: 20px">
                        <template #default="{ expanded }">
                            <b-icon v-if="expanded" icon="chevron-bar-up"></b-icon>
                            <b-icon v-else icon="chevron-bar-down"></b-icon>
                        </template>
                    </b-navbar-toggle>
                    <b-collapse visible id="navbar-toggle-collapse" is-nav>
                        <b-navbar-nav class="ml-auto" style="margin-left: 20px; margin-right:15px" id="nav_options">
                            <div v-if="main_tab_index == 0">
                                <b-nav-item-dropdown text="Hidden State" right>
                                    <b-form-group class=" bg-dark">
                                        <b-form-checkbox-group stacked buttons v-model="hidden_state_functions"
                                            :options="hidden_state_options">
                                        </b-form-checkbox-group>
                                    </b-form-group>
                                </b-nav-item-dropdown>
                            </div>
                            <div v-else-if="main_tab_index == 1">
                                <b-nav-item-dropdown text="Number Generated" class="text-white" right>
                                    <b-container class="bg-secondary rounded-pill" fluid>
                                        <b-row>
                                            <b-col col="1">
                                                <b-form-input v-model="number_generated" type="range" min="1" max="50"
                                                    align-self="center" class="h-100"></b-form-input>
                                            </b-col>
                                            <b-col col="1">
                                                <div>{{ number_generated }}</div>
                                            </b-col>
                                        </b-row>
                                    </b-container>
                                </b-nav-item-dropdown>
                            </div>
                        </b-navbar-nav>
                    </b-collapse>
                </b-navbar>
            </b-col>
            <b-col cols="10">
                <b-row style="margin: 0 15% 20px 15%">
                    <b-form-input v-model="prompt" placeholder="Enter prompt" @keydown.enter="on_prompt_enter">
                    </b-form-input>
                </b-row>

                <b-row>
                    <b-card no-body>
                        <b-tabs card v-model="main_tab_index">
                            <b-tab title="Logit Lens" key="tab-logitlens">
                                <b-col>
                                    <b-row style="margin-bottom: 20px" align-v="center">
                                        <b-col cols="1">
                                            <b-button :pressed.sync="rewrite_toggle" variant="success">Rewrite
                                            </b-button>
                                        </b-col>
                                        <b-col v-if="rewrite_toggle" cols="2">
                                            <b-form-input v-model="rewrite" placeholder="Enter rewrite" @keydown.enter="on_rewrite_enter">
                                            </b-form-input>
                                        </b-col>
                                    </b-row>
                                    <b-row>
                                        <b-tabs content-class="mt-3" lazy pills fill>
                                            <b-tab :title="logitlens_data.name"
                                                v-for="logitlens_data in logitlens_items"
                                                :key="'tab-logitlens-' + logitlens_data.name">
                                                <b-table :items="logitlens_data.data" :fields="logitlens_data.fields"
                                                    table-class="logitlens_table" class="text-center">
                                                    <template #head()="data">
                                                        <b-button v-if="'index' in data.field"
                                                            @click="rewrite_token_index=data.field.index"
                                                            :variant="rewrite_token_index==data.field.index ? 'warning': 'outline-dark'"
                                                            :disabled="!rewrite_toggle">
                                                            {{data.label}}
                                                        </b-button>
                                                        <span v-else>{{data.label}}</span>
                                                    </template>
                                                    <template #cell()="data">

                                                        <b-button v-if="data.field.label == 'Layer'"
                                                            @click="on_layer_click(data.item.Layer)"
                                                            :variant="data.item.Layer in rewrite_layers ? 'warning': 'outline-dark'"
                                                            :disabled="!rewrite_toggle">
                                                            {{data.value}}
                                                        </b-button>

                                                        <span v-else class="d-block"
                                                            :style="{'background': 'rgb(' + data.item.colors[data.field.index]?.join(',') + ')'}">{{
                                                            data.value }}</span>
                                                    </template>
                                                </b-table>
                                            </b-tab>
                                        </b-tabs>
                                    </b-row>
                                </b-col>
                            </b-tab>
                            <b-tab title="Playground" key="tab-playground">
                                <b-col>
                                    <b-row style="margin-bottom: 20px" align-v="center">
                                        <b-col>
                                            <b-button @click="normal_generated = []" variant="success">Clear
                                            </b-button>
                                        </b-col>
                                    </b-row>
                                    <b-row>
                                        <b-card-group deck>
                                            <b-card bg-variant="light" v-for="(generated, index) in normal_generated"
                                                :key="'normal-generated-' + index" :header="index + 1">
                                                <p style="font-family:Times;font-size:20px">{{generated.input}}</p>
                                                <p
                                                    style="margin-left:5%; font-style:italic;font-family:Times;font-size:20px">
                                                    {{generated.output}}</p>
                                            </b-card>
                                        </b-card-group>
                                    </b-row>
                                </b-col>
                            </b-tab>
                        </b-tabs>
                    </b-card>
                </b-row>
            </b-col>
        </b-row>
    </b-container>
</template>

<style>
#nav_options ul {
    padding: 0
}
</style>
    
    
<script>

import axios from 'axios'
import Vue from 'vue'
export default {
    name: 'LogitLens',
    data() {
        return {
            rewrite_token_index: undefined,
            rewrite: '',
            rewrite_toggle: false,
            rewrite_layers: {},
            prompt: '',
            hidden_state_functions: [],
            hidden_state_options: [],
            logitlens_items: [],
            main_tab_index: 0,
            number_generated: 1,
            normal_generated: [],
            alert: '',
            alert_countdown: 0,
        };
    },
    methods: {

        on_layer_click(layer) {
            layer in this.rewrite_layers ? Vue.delete(this.rewrite_layers, layer) : Vue.set(this.rewrite_layers, layer, true)
        },
        alert_timer(count_down) {
            this.alert_countdown = count_down
        },

        initialize() {
            const path = 'http://localhost:5000/init';

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
        }, 
        on_rewrite_enter(){

            const path = 'http://localhost:5000/rewrite';
            let params = { layers: this.rewrite_layers, token_idx: this.rewrite_token_index, prompt: this.prompt, target: this.rewrite}

            axios.get(path, { params: params, responseType: 'blob'})
                .then((response) => {

                    console.log('woohoo')
                    let blob = new Blob([response.data], {type: 'application/octet-stream'})
                    console.log(blob)
                })
                .catch((error) => {
                    console.error(error)
                });

        },
        on_prompt_enter() {

            if (this.prompt == '') {
                this.alert = 'Empty prompt'
                this.alert_countdown = 2

            }
            else if (this.main_tab_index == 0) {
                this.logitlens()
            }
            else if (this.main_tab_index == 1) {
                this.generate()
            }
        },
        generate() {

            const path = 'http://localhost:5000/generate';
            let prompt = this.prompt
            let params = { number_generated: this.number_generated, prompt: prompt }

            axios.get(path, { params: params })
                .then((response) => {

                    this.normal_generated.push({ input: prompt, output: response.data.normal_generated })

                })
                .catch((error) => {
                    console.error(error)
                });

        },
        logitlens() {

            if (this.hidden_state_functions.length == 0) {

                this.alert = 'Select at least one hidden state'
                this.alert_countdown = 2

                return
            }

            this.rewrite_token_index = undefined
            this.rewrite_toggle = false
            this.rewrite_layers = {}

            const path = 'http://localhost:5000/logitlens';
            let params = { indicies: this.hidden_state_functions.map(function (option) { return option.index }), prompt: this.prompt }

            axios.get(path, { params: params })
                .then((response) => {

                    let tokenized_prompt = response.data.prompt

                    let fields = ['Layer']

                    for (let token_idx = 0; token_idx < tokenized_prompt.length; token_idx++) {
                        fields.push({ key: tokenized_prompt[token_idx], label: tokenized_prompt[token_idx], index: token_idx })
                    }

                    let items = []

                    for (const [key, value] of Object.entries(response.data.data)) {

                        items.push({ data: this._logitlens(value.words, value.probabilities, tokenized_prompt, this.hidden_state_options[key].value.color), name: this.hidden_state_options[key], fields: fields })
                    }

                    this.logitlens_items = items
                })
                .catch((error) => {
                    console.error(error)
                });
        },
        _logitlens(words, probabilities, tokenized_prompt, color) {

            let items = []

            for (let layer = 0; layer < words.length; layer++) {
                let item = { Layer: layer, colors: [] }
                for (let token_idx = 0; token_idx < tokenized_prompt.length; token_idx++) {
                    item[tokenized_prompt[token_idx]] = words[layer][token_idx][0]
                    let probability = probabilities[layer][token_idx][0]
                    item.colors.push(color.map(function (x) { return parseInt(255 * (1 - probability) + x * probability) }))
                }
                items.push(item)
            }

            return items

        },
    },
    created() {
        this.initialize()
    },
};
</script>