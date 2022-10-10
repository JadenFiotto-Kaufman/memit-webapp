<template>
    <b-col>
        <b-row style="margin-bottom: 20px" align-v="center">
            <b-col cols="1">
                <b-button :pressed.sync="rewrite_toggle" variant="primary">Rewrite
                </b-button>
            </b-col>
            <b-col v-if="rewrite_toggle" cols="2">
                <b-form-input v-model="rewrite_target" placeholder="Enter rewrite" @keydown.enter="rewrite">
                </b-form-input>
            </b-col>
        </b-row>
        <b-row>
            <b-tabs fill>
                <b-tab v-for="logitlens_data in logitlens_items" :title="logitlens_data.name"
                    :key="'tab-logitlens-' + logitlens_data.name">
                    <b-tabs content-class="mt-3" fill class="mt-3">
                        <b-tab :title="_logitlens_data.name" v-for="_logitlens_data in logitlens_data.data"
                            :key="'tab-logitlens-' + logitlens_data.name + '-' + _logitlens_data.name">
                            <b-table :items="_logitlens_data.data" :fields="_logitlens_data.fields"
                                table-class="logitlens_table" class="text-center">
                                <template #head()="data">
                                    <b-button v-if="'index' in data.field" @click="rewrite_token_index=data.field.index"
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
            </b-tabs>
        </b-row>
    </b-col>
</template>

<style>

</style>



<script>
import Vue from 'vue'
import axios from 'axios'
export default {
    name: 'LLME_LogitLens',
    props: {
        prompt: {
            type: String,
            required: true
        }
    },
    data() {
        return {

            rewrite_token_index: undefined,
            rewrite_target: '',
            rewrite_toggle: false,
            rewrite_layers: {},
            logitlens_items: []
        };
    },
    methods: {

        on_layer_click(layer) {
            layer in this.rewrite_layers ? Vue.delete(this.rewrite_layers, layer) : Vue.set(this.rewrite_layers, layer, true)
        },
        rewrite() {

            let alert_message = ''

            if (this.rewrite_target == '') {

                alert_message += 'Empty prompt. '
            }
            if (Object.keys(this.rewrite_layers).length == 0) {

                alert_message += 'Select at least one layer. '
                
            }
            if ( typeof this.rewrite_token_index == "undefined" ) {


                alert_message += 'Select a token. '
            }

            if (alert_message != ''){

                this.$emit('alert', alert_message, 2)

                return 
            }

            this.$emit('toggle_loading')

            const path = 'http://localhost:5000/rewrite';
            let params = { layers: Object.keys(this.rewrite_layers), token_idx: this.rewrite_token_index, prompt: this.prompt, target: this.rewrite_target }

            axios.get(path, { params: params })
                .then((response) => {

                    console.log(response)

                    this.show_loading = false

                })
                .catch((error) => {
                    console.error(error)
                }).finally(() => {
                    this.$emit('toggle_loading')
                });


        },
        logitlens(hidden_state_options, hidden_state_functions) {

            this.$emit('toggle_loading')

            this.rewrite_token_index = undefined
            this.rewrite_toggle = false
            this.rewrite_layers = {}

            const path = 'http://localhost:5000/logitlens';
            let params = { indicies: hidden_state_functions.map(function (option) { return option.index }), prompt: this.prompt }

            axios.get(path, { params: params })
                .then((response) => {

                    let tokenized_prompt = response.data.prompt

                    let fields = ['Layer']

                    for (let token_idx = 0; token_idx < tokenized_prompt.length; token_idx++) {
                        fields.push({ key: tokenized_prompt[token_idx], label: tokenized_prompt[token_idx], index: token_idx })
                    }

                    let items = []

                    let original_items = []

                    for (const [key, value] of Object.entries(response.data.data)) {

                        original_items.push({ data: this._logitlens(value.words, value.probabilities, tokenized_prompt, hidden_state_options[key].value.color), name: hidden_state_options[key].text, fields: fields })
                    }

                    items.push({ data: original_items, name: 'Original' })

                    if (response.data.rewrite_data) {

                        let rewrite_items = []

                        for (const [key, value] of Object.entries(response.data.rewrite_data)) {

                            rewrite_items.push({ data: this._logitlens(value.words, value.probabilities, tokenized_prompt, hidden_state_options[key].value.color), name: hidden_state_options[key].text, fields: fields })
                        }

                        items.push({ data: rewrite_items, name: 'Rewritten' })

                    }

                    this.logitlens_items = items

                    this.show_loading = false

                })
                .catch((error) => {
                    console.error(error)
                }).finally(() => {
                    this.$emit('toggle_loading')
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
    }

};
</script>