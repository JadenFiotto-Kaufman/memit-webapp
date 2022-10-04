<template>
    <b-container fluid>
        <b-row>
            <b-col>
                <b-navbar toggleable type="dark" variant="dark">
                    <b-navbar-brand href="#" style="margin-left: 20px">Options</b-navbar-brand>
                    <b-navbar-toggle target="navbar-toggle-collapse" style="margin-right: 20px">
                        <template #default="{ expanded }">
                            <b-icon v-if="expanded" icon="chevron-bar-up"></b-icon>
                            <b-icon v-else icon="chevron-bar-down"></b-icon>
                        </template>
                    </b-navbar-toggle>
                    <b-collapse visible id="navbar-toggle-collapse" is-nav>
                        <b-navbar-nav class="ml-auto" style="margin-left: 20px" id="nav_options">
                            <b-nav-item-dropdown text="Hidden State" right>
                                <b-form-group class=" bg-dark">
                                    <b-form-checkbox-group stacked buttons v-model="hidden_state_functions"
                                        :options="hidden_state_options">
                                    </b-form-checkbox-group>
                                </b-form-group>
                            </b-nav-item-dropdown>
                        </b-navbar-nav>
                    </b-collapse>
                </b-navbar>
            </b-col>
            <b-col cols="10">
                <b-row style="margin: 0 15% 20px 15%">
                    <b-form-input v-model="prompt" placeholder="Enter prompt" @keydown.enter="logitlens"></b-form-input>
                </b-row>
                <b-row style="margin-bottom: 20px" class="text-center" align-v="center">
                    <b-col align-self="center">
                        <b-button :pressed.sync="rewrite_toggle">Rewrite</b-button>
                    </b-col>
                </b-row>
                <b-row>
                    <b-tabs>
                        <b-tab title="Logit Lens" key="tab-logitlens">
                            <b-tabs content-class="mt-3" lazy>
                                <b-tab :title="logitlens_data.name" v-for="logitlens_data in logitlens_items"
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
                        </b-tab>
                        <b-tab title="Playground" key="tab-playground">
                            
                        </b-tab>
                    </b-tabs>
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
            rewrite_toggle: false,
            rewrite_layers: {},
            prompt: '',
            hidden_state_functions: [],
            hidden_state_options: [],
            logitlens_items: [],
        };
    },
    methods: {

        on_layer_click(layer) {
            layer in this.rewrite_layers ? Vue.delete(this.rewrite_layers, layer) : Vue.set(this.rewrite_layers, layer, true)
        },

        initialize() {
            const path = 'http://localhost:5000/init';

            axios.post(path)
                .then((response) => {
                    var initialization_data = response.data;

                    for (const option of initialization_data.hidden_state_options) {
                        this.hidden_state_options.push({ value: { color: option.color, index: option.index, name: option.name }, text: option.name, checked: true })
                    }

                    this.hidden_state_functions.push(this.hidden_state_options[0].value)

                })
                .catch((error) => {
                    console.error(error)
                });
        },
        logitlens() {

            this.rewrite_token_index = undefined
            this.rewrite_toggle = false
            this.rewrite_layers = {}

            const path = 'http://localhost:5000/logitlens';
            var params = { indicies: this.hidden_state_functions.map(function (option) {return option.index}), prompt: this.prompt }

            axios.get(path, { params: params })
                .then((response) => {

                    var tokenized_prompt = response.data.prompt

                    var fields = ['Layer']

                    for (let token_idx = 0; token_idx < tokenized_prompt.length; token_idx++) {
                        fields.push({ key: tokenized_prompt[token_idx], label: tokenized_prompt[token_idx], index: token_idx})
                    }

                    var items = []

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

            var items = []
           
            for (let layer = 0; layer < words.length; layer++) {
                var item = { Layer: layer, colors: [] }
                for (let token_idx = 0; token_idx < tokenized_prompt.length; token_idx++) {
                    item[tokenized_prompt[token_idx]] = words[layer][token_idx][0]
                    var probability = probabilities[layer][token_idx][0]
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